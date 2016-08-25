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
    def __init__(self, view_type):
        self._view_type = view_type
        self._pm = PluginManager()

    def make_transformation(self, other):
        # TODO: perform graph traversal in the future because
        # transformers should be transitive if lossless
        has_trans, key = self.has_transformation(other)
        if not has_trans:
            raise Exception()

        # key is None if no transformation exists, but if has_trans is True
        # then we are dealing with an identity
        if key is None:
            return lambda view: self.coerce(view, other.view_type)

        def transformation(view):
            transformer_lookup = self._pm.transformers[key]

        return transformation

    def has_transformation(self, other):
        if any(a == b for a, b in itertools.combinations(
                    self.view_types, other.view_types)):
            # There is a trivial transformation which does not require a
            # transformer
            return True, None

        if not self.can_coerce(self._pm.transformers.keys()):
            return False

        for key in self.view_types:
            possible_results = self._pm.transformers[key].keys()
            if other.can_coerce(possible_results):
                return True, key
        return False, None

    def can_coerce(self, views):
        return any(key in views for key in self.view_types)

    def coerce(self, view, view_type):
        raise NotImplementedError()


class TempPathResourcePattern(ResourcePattern):
    @property
    def view_types(self):
        yield self._view_type
        yield from self._view_type.__args__

    def coerce(self, view, view_type):
        if view_type == self._view_type:
            return view
        if view_type == self._view_type.__args__[0]:
            return view_type(view, mode='r')
        raise Exception()


class FormatResourcePattern(ResourcePattern):
    @property
    def view_type(self):
        yield self._view_type


    def coerce(self, view, view_type):
        if view_type == self._view_type:
            return view
        if


class ObjectViewResourcePattern(ResourcePattern):
    @property
    def view_types(self):
        yield self._view_type


def interpreter(view_type: type) -> ResourcePattern:
    if type(view_type) is TempPath:
        return TempPathResourcePattern(view_type)
    else:
        return ObjectViewResourcePattern(view_type)
