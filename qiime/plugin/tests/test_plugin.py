# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import collections
import unittest

import qiime.plugin
import qiime.sdk

from qiime.core.testing.type import (IntSequence1, IntSequence2, Mapping,
                                     FourInts)
from qiime.core.testing.util import get_dummy_plugin


class TestPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = get_dummy_plugin()

    def test_name(self):
        self.assertEqual(self.plugin.name, 'dummy-plugin')

    def test_version(self):
        self.assertEqual(self.plugin.version, '0.0.0-dev')

    def test_website(self):
        self.assertEqual(self.plugin.website,
                         'https://github.com/qiime2/qiime2')

    def test_package(self):
        self.assertEqual(self.plugin.package, 'qiime.core.testing')

    def test_citation_text(self):
        self.assertEqual(self.plugin.citation_text, 'No relevant citation.')

    def test_user_support_text(self):
        self.assertEqual(self.plugin.user_support_text,
                         'For help, see http://2.qiime.org')

    def test_citation_text_default(self):
        plugin = qiime.plugin.Plugin(
            name='local-dummy-plugin',
            version='0.0.0-dev',
            website='https://github.com/qiime2/qiime2',
            package='qiime.core.testing')
        self.assertTrue(plugin.citation_text.startswith('No citation'))
        self.assertTrue(plugin.citation_text.endswith(
                            plugin.website))

    def test_user_support_text_default(self):
        plugin = qiime.plugin.Plugin(
            name='local-dummy-plugin',
            version='0.0.0-dev',
            website='https://github.com/qiime2/qiime2',
            package='qiime.core.testing')
        self.assertTrue(plugin.user_support_text.startswith('No user'))
        self.assertTrue(plugin.user_support_text.endswith(
                            plugin.website))

    def test_methods(self):
        methods = self.plugin.methods

        self.assertEqual(methods.keys(),
                         {'merge_mappings', 'concatenate_ints',
                          'concatenate_ints_markdown', 'split_ints',
                          'split_ints_markdown'})
        for method in methods.values():
            self.assertIsInstance(method, qiime.sdk.Method)

    def test_visualizers(self):
        visualizers = self.plugin.visualizers

        self.assertEqual(visualizers.keys(),
                         {'most_common_viz', 'mapping_viz'})
        for viz in visualizers.values():
            self.assertIsInstance(viz, qiime.sdk.Visualizer)

    def test_types(self):
        types = self.plugin.types

        self.assertEqual(
            types,
            {'IntSequence1': IntSequence1, 'IntSequence2': IntSequence2,
             'Mapping': Mapping, 'FourInts': FourInts})


if __name__ == '__main__':
    unittest.main()
