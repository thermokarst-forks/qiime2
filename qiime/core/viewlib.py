# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from qiime.sdk import PluginManager
from .path import TempPath


class ResourcePattern:
    def __init__(self, expression):
        self.expression = expression
        self._pm = PluginManager()

    def make_transformation(self, other):
        has_trans, key = self.has_transformation(other)
        if not has_trans:
            raise Exception()

        def transformation(view):
            transformer_lookup = self._pm.transformers[key]

        return transformation

    def has_transformation(self, other):
        if not self.can_coerce(self._pm.transformers.keys()):
            return False

        for key in self.transformer_keys():
            possible_results = self._pm.transformers[key].keys()
            if other.can_coerce(possible_results):
                return True, key
        return False, None

    def can_coerce(self, views):
        return any(key in views for key in self.transformer_keys())


class TempPathResourcePattern(ResourcePattern):
    def transformer_keys(self):
        yield self.expression
        yield from self.expression.__args__


class ObjectViewResourcePattern(ResourcePattern):
    def transformer_keys(self):
        yield self.expression


def interpreter(view_type: type) -> ResourcePattern:
    if type(view_type) is TempPath:
        return TempPathResourcePattern(view_type)
    else:
        return ObjectViewResourcePattern(view_type)
