# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import abc
import collections
import contextlib

import qiime2


ScopeRecord = collections.namedtuple('ScopeRecord',
                                     ['name', 'type', 'factory'])


class Scope:
    def __init__(self, records=None):
        if records is None:
            self.records = dict()
        else:
            self.records = dict(records)

    def _add_record(self, name, factory, type):
        # TODO: do i need this?
        # if name in self.records:
        #     raise ValueError

        self.records[name] = ScopeRecord(name=name, type=type, factory=factory)

    def add_artifact(self, name, factory):
        self._add_record(name, factory, 'artifact')

    def add_visualization(self, name, factory):
        self._add_record(name, factory, 'visualization')

    def add_file(self, name, factory):
        self._add_record(name, factory, 'file')

    def add_metadata(self, name, factory):
        self._add_record(name, factory, 'metadata')

    def keys(self):
        return self.records.keys()

    def __len__(self):
        return len(self.records)

    def __str__(self):
        return str(self.records)

    def __iter__(self):
        yield from self.records.values()

    def __getitem__(self, key):
        return self.records[key]

    def __contains__(self, key):
        return key in self.records


class Usage(metaclass=abc.ABCMeta):
    def __init__(self):
        self.scope = None
        self.plugin_manager = None

    @contextlib.contextmanager
    def bind(self, scope):
        self.scope = scope
        yield self
        self.scope = None

    def get_action(self, plugin, action):
        if self.plugin_manager is None:
            self.plugin_manager = qiime2.sdk.PluginManager()

        plugin = self.plugin_manager.plugins[plugin]
        return plugin.actions[action]

    @abc.abstractmethod
    def comment(self, text):
        raise NotImplementedError

    @abc.abstractmethod
    def action(self, action, inputs, outputs=None):
        raise NotImplementedError

    @abc.abstractmethod
    def import_file(self, type, input_name, output_name=None, format=None):
        raise NotImplementedError

    @abc.abstractmethod
    def export_file(self, input_name, output_name, format=None):
        raise NotImplementedError


class NoOpUsage(Usage):
    def get_action(self, plugin, action):
        return None

    def comment(self, text):
        return None

    def action(self, action, inputs, outputs=None):
        return None

    def import_file(self, type, input_name, output_name=None, format=None):
        return None

    def export_file(self, input_name, output_name, format=None):
        return None


class ExecutionUsage(Usage):
    def comment(self, text):
        return None

    def import_file(self, type, input_name, output_name=None, format=None):
        return None

    def export_file(self, input_name, output_name, format=None):
        return None

    def action(self, action, inputs, outputs=None):
        sig = action.signature
        opts = {}

        for name, signature in sig.signature_order.items():
            if name in inputs:
                if signature.qiime_type.name == 'MetadataColumn':
                    ref, col = inputs[name]
                    value = self.scope[ref].factory()
                    value = value.get_column(col)
                elif inputs[name] in self.scope:
                    value = self.scope[inputs[name]].factory()
                else:
                    value = inputs[name]
                opts[name] = value

        results = action(**opts)

        for output in sig.outputs.keys():
            scope_name = outputs[output] if output in outputs else output
            result = getattr(results, output)
            if isinstance(result, qiime2.Artifact):
                self.scope.add_artifact(scope_name, lambda: result)
            else:
                self.scope.add_visualization(scope_name, lambda: result)
