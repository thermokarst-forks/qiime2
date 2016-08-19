# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import qiime.sdk as sdk
from .resource_type import ResourceMeta


class ResourcePattern:
    def __init__(self, expression):
        self.expression = expression
        self._pm = sdk.PluginManager()

    def make_transformation(self, other):
        has_trans, key = self.has_transformation(other)
        if not has_trans:
            raise Exception()

        def transform(view):
            transformer_lookup = self._pm.transformers[key]

        return transform


    def has_transformation(self, other):
        if not self.can_coerce(self._pm.transformers.keys())
            return False

        for key in self.transformer_keys():
            possible_results = self._pm.transformers[key].keys()
            if other.can_coerce(possible_results)
                return True, key
        return False, None

    def can_coerce(self, views):
        return any(key in views for key in self.transformer_keys())


class FilePathResourcePattern(ResourcePattern):

    def transformer_keys(self):
        yield self.expression
        yield self.expression.__pattern__


class DirectoryPathResourcePattern(ResourcePattern):

    def transformer_keys(self):
        yield self.expression
        yield self.expression.__pattern__


class ObjectViewResourcePattern(ResourcePattern):

    def transformer_keys(self):
        yield self.expression


def interpreter(view_type: type) -> ResourcePattern:
    if type(view_type) is ResourceMeta:
        name = view_type.__name__
        if name == "FilePath":
            return FilePathResourcePattern(view_type)
        elif name == "DirectoryPath":
            return DirectoryPathResourcePattern(view_type)
        else:
            raise TypeError()
    else:
        return ObjectViewResourcePattern(view_type)
