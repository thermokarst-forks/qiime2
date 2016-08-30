# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from qiime import sdk
from qiime.plugin import resource
from qiime.core import path


def identity(x):
    return x


class ResourcePattern:
    @staticmethod
    def from_view_type(view_type):
            if issubclass(view_type, (path.InPath, path.OutPath)):
                return PathResource(view_type)
            elif issubclass(view_type, (resource.file_format._FileFormat,
                                        resource.DirectoryFormat)):
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


class FormatResource(ResourcePattern):
    def yield_input_coercion(self):
        yield identity, self._view_type
        yield (lambda x: path.InPath(x.path),
               path.InPath[self._view_type])

    def yield_output_coercion(self, view_type):
        if view_type == self._view_type:
            yield lambda x: self._view_type(x.path, mode='r')

        if view_type == path.OutPath[self._view_type]:
            yield lambda x: self._view_type(x, mode='r')


class ObjectResource(ResourcePattern):
    pass
