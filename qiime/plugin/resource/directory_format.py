# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import os
import re

from qiime.core import transform
from qiime.core import path


class ValidationError(Exception):
    pass


class PathMakerDescriptor:
    def __init__(self, file):
        self.file = file

    def __get__(self, obj, cls=None):
        if obj is None:
            raise Exception()
        return getattr(obj, self.file.name).path_maker


class File:
    def __init__(self, pathspec, *, format=None):
        if format is None:
            raise TypeError()
        self.pathspec = pathspec
        self.format = format

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        return BoundFile(self.name, self.pathspec, self.format, obj)


class FileCollection(File):
    def __init__(self, pathspec, *, format=None):
        super().__init__(pathspec, format=format)
        self._path_maker = None

    def set_path_maker(self, function):
        self._path_maker = function
            return PathMakerDescriptor(self)

    def __get__(self, obj, cls=None):
        if obj is None:
            return self

        if self._path_maker is None:
            raise NotImplementedError()

        return BoundFileCollection(self.name, self.pathspec, self.format,
                                   obj, path_maker=self._path_maker)


class BoundFile:
    @property
    def mode(self):
        return self._directory_format.mode

    def __init__(self, name, pathspec, format, directory_format):
        self.name = name
        self.pathspec = pathspec
        self.format = format
        self._directory_format = directory_format
        self._path_maker = lambda: os.path.join(self._directory_format.path,
                                                self.pathspec)

    def view(self, view_type):
        from_pattern = transform.ResourcePattern.from_view_type(
            path.InPath[self.format])
        to_pattern = transform.ResourcePattern.from_view_type(view_type)

        transformation = from_pattern.make_transformation(to_pattern)
        return transformation(self._path_maker())

    def set(self, view, view_type, **kwargs):
        if self.mode != 'w':
            raise TypeError("Cannot use `set`/`add` when mode=%r" % self.mode)
        from_pattern = transform.ResourcePattern.from_view_type(view_type)
        to_pattern = transform.ResourcePattern.from_view_type(self.format)

        transformation = from_pattern.make_transformation(to_pattern)
        result = transformation(view)
        result.move(self._path_maker(self, **kwargs))

    @property
    def path_maker(self):
        def bound_path_maker(**kwargs):
            return self._path_maker(self._directory_format, **kwargs)
        return bound_path_maker


class BoundFileCollection(BoundFile):
    def __init__(self, name, pathspec, format, directory_format, path_maker):
        super().__init__(name, pathspec, format, directory_format)
        self._path_maker = path_maker

    def view(self, view_type):
        root = self._directory_format.path
        paths = [os.path.join(root, fp) for fp in os.listdir(root)
                 if re.match(self.pathspec, fp)]
        from_pattern = transform.ResourcePattern.from_view_type(
            path.InPath[self.format])
        to_pattern = transform.ResourcePattern.from_view_type(view_type)

        transformation = from_pattern.make_transformation(to_pattern)
        for fp in paths:
            yield transformation(fp)

    def set(self, view, view_type, **kwargs):
        raise TypeError("Cannot set an entire file collection, use `add`.")

    def add(self, view, view_type, **kwargs):
        super().set(view, view_type, **kwargs)


class _DirectoryMeta(type):
    def __init__(self, name, bases, dct):
        super().__init__(name, bases, dct)
        for key, value in dct.items():
            if isinstance(value, File):
                value.name = key


class DirectoryFormat(metaclass=_DirectoryMeta):
    def __init__(self, path=None, mode='w'):
        if path is None:
            self._backing_path = path.OutPath(
                dir=True,
                prefix='q2-%s-' % self.__class__.__name__
            )
        else:
            self._backing_path = path
        self.path = str(self._backing_path)
        self._mode = mode
