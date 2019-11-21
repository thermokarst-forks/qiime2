# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import collections
import os
import pkg_resources
import qiime2.core.type

import enum


class FormatFilters(enum.Flag):
    EXPORTABLE = enum.auto()
    IMPORTABLE = enum.auto()


class PluginManager:
    entry_point_group = 'qiime2.plugins'
    __instance = None

    @classmethod
    def iter_entry_points(cls):
        """Yield QIIME 2 plugin entry points.

        If the QIIMETEST environment variable is set, only the framework
        testing plugin entry point (`dummy-plugin`) will be yielded. Otherwise,
        all available plugin entry points (excluding `dummy-plugin`) will be
        yielded.

        """
        for entry_point in pkg_resources.iter_entry_points(
                group=cls.entry_point_group):
            if 'QIIMETEST' in os.environ:
                if entry_point.name == 'dummy-plugin':
                    yield entry_point
            else:
                if entry_point.name != 'dummy-plugin':
                    yield entry_point

    # This class is a singleton as it is slow to create, represents the
    # state of a qiime2 installation, and is needed *everywhere*
    def __new__(cls):
        if cls.__instance is None:
            self = super().__new__(cls)
            self._init()
            cls.__instance = self
        return cls.__instance

    def _init(self):
        self.plugins = {}
        self.type_fragments = {}
        self.transformers = collections.defaultdict(dict)
        self._reverse_transformers = collections.defaultdict(dict)
        self.formats = {}
        self.views = {}
        self.type_formats = []
        self._ff_to_sfdf = {}
        self._importable = set()
        self._exportable = set()
        self._canonical_formats = set()

        # These are all dependent loops, each requires the loop above it to
        # be completed.
        for entry_point in self.iter_entry_points():
            plugin = entry_point.load()
            self.plugins[plugin.name] = plugin

        for plugin in self.plugins.values():
            self._integrate_plugin(plugin)

        for canonical_format in self._canonical_formats:
            self._importable.update(
                                self._reverse_transformers[canonical_format])
            self._exportable.update(self.transformers[canonical_format])

        for importable_format in self._importable:
            if(isinstance(importable_format,
                          qiime2.plugin.model.file_format._FileFormat)):
                self._importable.add(self._ff_to_sfdf[importable_format])

        for exportable_format in self._exportable:
            if(isinstance(exportable_format,
                          qiime2.plugin.model.file_format._FileFormat)):
                self._exportable.add(self._ff_to_sfdf[exportable_format])

    def _integrate_plugin(self, plugin):
        for type_name, type_record in plugin.type_fragments.items():
            if type_name in self.type_fragments:
                conflicting_type_record = \
                    self.type_fragments[type_name]
                raise ValueError("Duplicate semantic type (%r) defined in"
                                 " plugins: %r and %r"
                                 % (type_name, type_record.plugin.name,
                                    conflicting_type_record.plugin.name))

            self.type_fragments[type_name] = type_record

        for (input, output), transformer_record in plugin.transformers.items():
            if output in self.transformers[input]:
                raise ValueError("Transformer from %r to %r already exists."
                                 % transformer_record)
            self.transformers[input][output] = transformer_record
            self._reverse_transformers[output][input] = transformer_record

        for name, record in plugin.views.items():
            if name in self.views:
                raise NameError(
                    "Duplicate view registration (%r) defined in plugins: %r"
                    " and %r" %
                    (name, record.plugin.name, self.formats[name].plugin.name)
                )
            self.views[name] = record

        for name, record in plugin.formats.items():
            fmt = record.format

            if issubclass(
                    fmt, qiime2.plugin.model.SingleFileDirectoryFormatBase):
                self._ff_to_sfdf[fmt.file.format] = fmt

            # TODO: remove this when `sniff` is removed
            if hasattr(fmt, 'sniff') and hasattr(fmt, '_validate_'):
                raise RuntimeError(
                    'Format %r registered in plugin %r defines sniff and'
                    '_validate_ methods - only one is permitted.' %
                    (name, record.plugin.name)
                )

            self.formats[name] = record
        self.type_formats.extend(plugin.type_formats)

        for type_format in plugin.type_formats:
            self._canonical_formats.add(type_format.format)
            if isinstance(type_format.format,
                          qiime2.plugin.model.SingleFileDirectoryFormatBase):
                self._canonical_formats.add(type_format.format.file.format)

    def get_semantic_types(self):
        types = set()

        for plugin in self.plugins.values():
            for type_record in plugin.types:
                types.add(type_record.semantic_type)

        return types

    # TODO: Should plugin loading be transactional? i.e. if there's
    # something wrong, the entire plugin fails to load any piece, like a
    # databases rollback/commit

    def get_formats(self, *, filter=None, semantic_type=None):
        if semantic_type is not None and semantic_type not in self.get_semantic_types():
            raise ValueError()

        if filter is not None and filter not in FormatFilters:
            raise ValueError()

        if semantic_type is None:
            formats = self.formats
        else:
            formats = {}
            for type_format in self.type_formats:
                if semantic_type <= type_format.type_expression:
                    formats[type_format.format] = type_format

        importable_formats = self._get_importable_formats(formats)
        exportable_formats = self._get_exportable_formats(formats)

        if filter is None:
            formats = {**formats, **importable_formats, **exportable_formats}
        elif filter is FormatFilters.IMPORTABLE:
            formats = importable_formats
        elif filter is FormatFilters.EXPORTABLE:
            formats = exportable_formats
        elif filter is FormatFilters.IMPORTABLE | FormatFilters.EXPORTABLE:
            formats = {**importable_formats, **exportable_formats}

        return formats

    def _get_importable_formats(self, formats):
        importable_formats = {}
        for format_ in formats:
            if format_ in self._reverse_transformers:
                for imp_fmt, rec in self._reverse_transformers[format_].items():
                    importable_formats[imp_fmt] = rec
        return importable_formats

    def _get_exportable_formats(self, formats):
        exportable_formats = {}
        for format_ in formats:
            if format_ in self.transformers:
                for imp_fmt, rec in self.transformers[format_].items():
                    exportable_formats[imp_fmt] = rec
        return exportable_formats

    def get_directory_format(self, semantic_type):
        if not qiime2.core.type.is_semantic_type(semantic_type):
            raise TypeError(
                "Must provide a semantic type via `semantic_type`, not %r" %
                semantic_type)

        dir_fmt = None
        for type_format_record in self.type_formats:
            if semantic_type <= type_format_record.type_expression:
                dir_fmt = type_format_record.format
                break

        if dir_fmt is None:
            raise TypeError(
                "Semantic type %r does not have a compatible directory format."
                % semantic_type)

        return dir_fmt
