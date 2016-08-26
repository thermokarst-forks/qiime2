# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

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
        pass

    def can_coerce_input(self):
        pass

    def can_coerce_output(self):
        pass

class PathResource(ResourcePattern):
    @property
    def view_types(self):
        yield self._view_type


class FormatResource(ResourcePattern):
    pass


class ObjectResource(ResourcePattern):
    pass
