# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import os
import pkg_resources

import qiime.core.type


class PluginManager:
    __instance = None

    # This class is a singleton as it is slow to create, represents the
    # state of a qiime installation, and is needed *everywhere*
    def __new__(cls):
        if cls.__instance is None:
            self = super().__new__(cls)
            self._init()
            cls.__instance = self
        return cls.__instance

    def _init(self):
        self.plugins = {}
        self.data_layouts = {}
        self.semantic_types = {}
        self.transformers = collections.defaultdict(dict)
        self._semantic_type_to_data_layouts = {}

        plugins = []
        for entry_point in pkg_resources.iter_entry_points(
                group='qiime.plugins'):
            if entry_point.name != 'dummy-plugin' or 'QIIMETEST' in os.environ:
                plugins.append(entry_point.load())

        # These are all dependent loops, each requires the loop above it to
        # be completed.
        for plugin in plugins:
            self.plugins[plugin.name] = plugin

        for plugin in plugins:
            self._integrate_plugin(plugin)

        for plugin in plugins:
            self._finalize_plugin(plugin)

    def _integrate_plugin(self, plugin):
        for id_, data_layout in plugin.data_layouts.items():
            if id_ in self.data_layouts:
                conflicting_plugin, _ = self.data_layouts[id_]
                raise ValueError(
                    "Duplicate data layout defined in plugins "
                    "%r and %r: %r, %r" % (conflicting_plugin, plugin.name,
                                           id_[0], id_[1]))
            # TODO rethink the structure for mapping data layout to plugin
            # (also applies to type system and workflows).
            self.data_layouts[id_] = (plugin.name, data_layout)

        for type_name, type_expr in plugin.types.items():
            if type_name in self.semantic_types:
                conflicting_plugin, _ = self.semantic_types[type_name]
                raise ValueError("Duplicate semantic type (%r) defined in"
                                 " plugins: %r and %r"
                                 % (type_expr, plugin.name,
                                    conflicting_plugin.name))

            self.semantic_types[type_name] = (plugin.name, type_expr)

    def _finalize_plugin(self, plugin):
        for semantic_type, data_layout_id in \
                plugin.type_to_data_layouts.items():
            if data_layout_id not in self.data_layouts:
                raise ValueError("Data layout %r does not exist, cannot"
                                 " register semantic type (%r) to it."
                                 % (data_layout_id, semantic_type))
            self._semantic_type_to_data_layouts[semantic_type] = \
                self.data_layouts[data_layout_id][1]


        for (input, output), transformer in plugin.transformers.items():
            if output in self.transformers[input]:
                raise ValueError("Transformer from %r to %r already exists."
                                 % transformation)
            self.transformers[input][output] = transformer

    # TODO: Should plugin loading be transactional? i.e. if there's
    # something wrong, the entire plugin fails to load any piece, like a
    # databases rollback/commit

    def get_data_layout(self, type):
        if not qiime.core.type.is_semantic_type(type):
            raise TypeError(
                "Must provide a semantic type via `type`, not %r" % type)

        data_layout = None
        for semantic_type, datalayout in \
                self._semantic_type_to_data_layouts.items():
            if type <= semantic_type:
                data_layout = datalayout
                break

        if data_layout is None:
            raise TypeError(
                "Semantic type %r does not have a compatible data layout."
                % type)

        return data_layout
