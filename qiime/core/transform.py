# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------
import pathlib

from qiime import sdk
from qiime.plugin import resource
from qiime.core import path


def identity(x):
    return x


class ResourcePattern:
    @staticmethod
    def from_view_type(view_type):
            if issubclass(view_type, (path.InPath, path.OutPath)):
                # HACK: this is necessary because we need to be able to "act"
                # like a FileFormat when looking up transformers, but our
                # input/output coercion still needs to bridge the
                # transformation as we do not have transitivity
                # TODO: redo this when transformers are transitive
                if issubclass(view_type.__args__[0],
                              resource.SingleFileDirectoryFormatBase):
                    return SingleFileDirectoryPathResource(view_type)
                return PathResource(view_type)
            elif issubclass(view_type, (resource.file_format._FileFormat,
                                        resource.DirectoryFormat)):
                # HACK: Same as above
                if issubclass(view_type,
                              resource.SingleFileDirectoryFormatBase):
                    return SingleFileDirectoryResource(view_type)
                return FormatResource(view_type)
            else:
                return ObjectResource(view_type)

    def __init__(self, view_type):
        self._pm = sdk.PluginManager()
        self._view_type = view_type

    def make_transformation(self, other):
        # This really just creates a depth-first traversal of an imaginary
        # tree of depth 3, each generator is a level of the tree.
        # TODO: make this a real graph traversal which can handle transitivity
        components = self._traverse_transformers(other)
        if components is not None:
            input_coercion, transformer, output_coercion = components

            def transformation(view):
                view = self.normalize(view)
                view = input_coercion(view)
                view = transformer(view)
                return output_coercion(view)

            return transformation

        raise Exception("No transformation from %s to %s" %
                        (self._view_type, other._view_type))

    def _traverse_transformers(self, other):
        for input_coercion, vt in self.yield_input_coercion():
            for transformer, out_type in self.yield_transformers(vt):
                for output_coercion in other.yield_output_coercion(out_type):
                    return input_coercion, transformer, output_coercion

    def yield_input_coercion(self):
        yield identity, self._view_type

    def yield_output_coercion(self, view_type):
        if view_type == self._view_type:
            yield identity

    def yield_transformers(self, view_type):
        if view_type == self._view_type:
            yield identity, self._view_type
        for type, record in self._pm.transformers[view_type].items():
            yield record.transformer, type

    def normalize(self, view):
        return view


class PathResource(ResourcePattern):
    @property
    def format(self):
        return self._view_type.__args__[0]

    def yield_input_coercion(self):
        yield identity, self._view_type
        yield lambda x: self.format(x, mode='r'), self.format

    def yield_output_coercion(self, view_type):
        if view_type == path.OutPath[self.format]:
            yield lambda x: path.InPath(x)

        if view_type == self.format:
            yield lambda x: path.InPath(x.path)

    def normalize(self, view):
        if type(view) is str:
            return pathlib.Path(view)

        return view

    def validate(self, view):
        normal_view = self.normalize(view)
        if not isinstance(view, pathlib.PurePath):
            raise TypeError("%r is not a path." % (view,))
        fmt = self.format(normal_view, mode='r')
        fmt.validate()


class FormatResource(ResourcePattern):
    def yield_input_coercion(self):
        yield identity, self._view_type
        yield (lambda x: path.InPath(x.path), path.InPath[self._view_type])

    def yield_output_coercion(self, view_type):
        if view_type == self._view_type:
            yield lambda x: self._view_type(x.path, mode='r')

        if view_type == path.OutPath[self._view_type]:
            yield lambda x: self._view_type(x, mode='r')

    def normalize(self, view):
        if type(view) is str:
            return self._view_type(view, mode='r')

        return view

    def validate(self, view):
        normal_view = self.normalize(view)
        if not isinstance(normal_view, self._view_type):
            raise TypeError("%r is not an instance of %r."
                            % (view, self._view_type))
        normal_view.validate()


class SingleFileDirectoryPathResource(PathResource):
    @property
    def format(self):
        return self._view_type.__args__[0]

    def __init__(self, view_type):
        composed_view_type = \
            view_type.__origin__[view_type.__args__[0].file.format]
        self.pattern = PathResource(composed_view_type)
        super().__init__(view_type)

    def yield_input_coercion(self):
        def wrap(coercion):
            def wrapped_coercion(view):
                fmt = self.format(view, mode='r')
                new_view = path.InPath(fmt.file.path_maker())
                new_view.__backing_fmt = fmt
                return coercion(new_view)

            return wrapped_coercion

        yield identity, self._view_type
        for coercion, vt in self.pattern.yield_input_coercion():
            yield wrap(coercion), vt

    def yield_output_coercion(self, view_type):
        def wrap(coercion):
            def wrapped_coercion(view):
                result = coercion(view)
                odm = self.format()
                odm.file.set(result, self.pattern._view_type)
                return path.InPath(odm.path)

            return wrapped_coercion

        if view_type == path.OutPath[self.format]:
            yield lambda x: path.InPath(x)
        for coercion in self.pattern.yield_output_coercion(view_type):
            yield wrap(coercion)


class SingleFileDirectoryResource(FormatResource):
    def __init__(self, view_type):
        composed_view_type = view_type.file.format
        self.pattern = FormatResource(composed_view_type)
        super().__init__(view_type)

    def yield_input_coercion(self):
        def wrap(coercion):
            def wrapped_coercion(fmt):
                new_view = fmt.file.view(self.pattern._view_type)
                new_view.__backing_fmt = fmt
                return coercion(new_view)

            return wrapped_coercion

        yield identity, self._view_type
        for coercion, vt in self.pattern.yield_input_coercion():
            yield wrap(coercion), vt

    def yield_output_coercion(self, view_type):
        def wrap(coercion):
            def wrapped_coercion(view):
                result = coercion(view)
                odm = self._view_type()
                odm.file.set(result, self.pattern._view_type)
                return self._view_type(odm.path, mode='r')

            return wrapped_coercion

        if view_type == self._view_type:
            yield lambda x: self._view_type(x.path, mode='r')
        for coercion in self.pattern.yield_output_coercion(view_type):
            yield wrap(coercion)


class ObjectResource(ResourcePattern):

    def validate(self, view):
        if not isinstance(view, self._view_type):
            raise TypeError("%r is not of type %r, cannot transform further."
                            % (view, self._view_type))
