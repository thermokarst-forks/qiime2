# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------


class _DirectoryMeta(type):
    def __init__(self, name, bases, dct):
        super().__init__(self, name, bases, dct)
        for key, value in dct.items():
            if isinstance(value, File):
                value.name = key


class DirectoryFormat(metaclass=_DirectoryMeta):
    pass


class File:
    def __init__(self, pathspec, *, format=None):
        if format is None:
            raise TypeError()
        self.pathspec = pathspec
        self.format = format


class FileCollection(File):
    def __init__(self, pathspec, *, format=None):
        super().__init__(pathspec, format=format)
        self._path_maker = None

    def set_path_maker(self, function):
        self._path_maker = function
        return PathMakerDescriptor(self.name)

    def __get__(self, obj, cls=None):
        if obj is None:
            return self

        if self._path_maker is None:
            raise NotImplementedError()

        return BoundFileCollection(obj, self.name, self.pathspec, self.format,
                                   pathmaker=self._path_maker)


class PathMakerDescriptor:
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls=None):
        if obj is None:
            raise Exception()
        return getattr(obj, self.name).path_maker



class BoundFile:
    pass


class BoundFileCollection(BoundFile):
    def __init__(self, name, directory_format, pathspec, format, path_maker):
        self.name = name
        self.pathspec = pathspec
        self.format = format

        self._directory_format = directory_format
        self._path_maker = path_maker

    def view(self, view_type):
        pass

    def inject(self, filepath, view_type):
        pass

    @property
    def path_maker(self):
        def bound_path_maker(**kwargs):
            return self._path_maker(self._directory_format, self, **kwargs)
        return bound_path_maker


class ExampleDirectoryFormat(resource.DirectoryFormat):
    something = resource.FileCollection("[0-9]*\.fastq", format=FASTQFileFormat)

    other = resource.File('example.txt', format=ExampleFormat)

    def __init__(self):
        self._curr_id = 0

    @something.set_path_maker
    def something_path_maker(self, collection):
        path = "%d.fastq" % self._curr_id
        self._curr_id += 1
        return path


class ExampleFormat(resource.FileFormat):
    def sniff(file):
        return True

dirfmt.something.path_maker(foo='bar')
