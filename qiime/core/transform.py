# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------
import qiime.core.path as path
import qiime.plugin.resource as resource


def identity(x):
    return x


class ResourcePattern:
    @staticmethod
    def from_view_type(view_type):
        if isinstance(view_type, (path.InPath, path.OutPath)):
            return PathResource(view_type)
        elif isinstance(view_type, (resource.FileFormat,
                                    resource.DirectoryFormat)):
            return FormatResource(view_type)
        else:
            return ObjectResource(view_type)

    def __init__(self, view_type):
        self._pm = sdk.PluginManager()
        self._view_type = view_type

    def make_transformation(self, other):
        has_transformation = False
        for input_coercion, vt in self.yield_input_coercion():
            for transformer, tv in self.yield_transformers(vt):
                for output_coercion in other.yield_output_coercion(tv):
                    has_transformation = True
                    break

        def transformation(view):
            view = input_coercion(view)
            view = transformer(view)
            return output_coercion(view)

        if has_transformation:
            return transformation
        raise Exception()

    def yield_input_coercion(self):
        yield identity, self._view_type

    def yield_output_coercion(self, view_type):
        if view_types == self._view_type:
            yield identity

    def yield_transformers(self, view_type):
        if view_type == self._view_type:
            yield identity
        for record in self._pm.transformers[view_type].values()
            yield record.transformer


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
            yield lambda x: path.InPath(x._backing_path)


class FormatResource(ResourcePattern):
    def yield_input_coercion(self):
        yield identity, self._view_type
        yield (lambda x: path.InPath(x._backing_path),
               path.InPath[self._view_type])

    def yield_output_coercion(self, view_type):
        if view_type == self._view_type
            yield self._view_type(view_type._backing_path, mode='r')

        if view_type == path.OutPath[self._view_type]:
            yield lambda x: self._view_type(x, mode='r')


class ObjectResource(ResourcePattern):
    pass
