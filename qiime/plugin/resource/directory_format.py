# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import re
import pathlib

from qiime.core import transform
from qiime.core import path as qpath
from .base import FormatBase


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
        return self._directory_format._mode

    def __init__(self, name, pathspec, format, directory_format):
        self.name = name
        self.pathspec = pathspec
        self.format = format
        self._directory_format = directory_format
        self._path_maker = lambda s: pathspec

    def view(self, view_type):
        from_pattern = transform.ResourcePattern.from_view_type(
            qpath.InPath[self.format])
        to_pattern = transform.ResourcePattern.from_view_type(view_type)

        transformation = from_pattern.make_transformation(to_pattern)
        return transformation(self.path_maker())

    def set(self, view, view_type, **kwargs):
        if self.mode != 'w':
            raise TypeError("Cannot use `set`/`add` when mode=%r" % self.mode)
        from_pattern = transform.ResourcePattern.from_view_type(view_type)
        to_pattern = transform.ResourcePattern.from_view_type(self.format)

        transformation = from_pattern.make_transformation(to_pattern)
        result = transformation(view)
        result.path.rename(self.path_maker(**kwargs))

    @property
    def path_maker(self):
        def bound_path_maker(**kwargs):
            # Must wrap in a naive Path, otherwise an OutPath would be summoned
            # into this world, and would destroy everything in its path.
            path = pathlib.Path(self._directory_format.path) \
                / self._path_maker(self._directory_format, **kwargs)
            path.parent.mkdir(parents=True, exist_ok=True)
            return path
        return bound_path_maker


class BoundFileCollection(BoundFile):
    def __init__(self, name, pathspec, format, directory_format, path_maker):
        super().__init__(name, pathspec, format, directory_format)
        self._path_maker = path_maker

    def view(self, view_type):
        # Don't want an OutPath, just a Path
        root = pathlib.Path(self._directory_format.path)
        paths = [fp for fp in sorted(root.glob('**/*'))
                 if re.match(self.pathspec, str(fp.relative_to(root)))]
        from_pattern = transform.ResourcePattern.from_view_type(
            qpath.InPath[self.format])
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


class DirectoryFormat(FormatBase, metaclass=_DirectoryMeta):
    pass
