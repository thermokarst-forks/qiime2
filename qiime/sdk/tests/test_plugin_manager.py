# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import unittest

import qiime.plugin
import qiime.sdk

from qiime.core.testing.type import (IntSequence1, IntSequence2, Mapping,
                                     FourInts)
from qiime.core.testing.util import get_dummy_plugin


# These tests are written to pass regardless of other plugins that may be
# installed. This is accomplished by only testing pieces we know are defined by
# the dummy plugin.
class TestPluginManager(unittest.TestCase):
    def setUp(self):
        # Ignore the returned dummy plugin object, just run this to verify the
        # plugin exists as the tests rely on it being loaded. PluginManager is
        # a singleton so there's no issue creating it again.
        get_dummy_plugin()
        self.pm = qiime.sdk.PluginManager()

    def test_plugins(self):
        plugins = self.pm.plugins

        self.assertIsInstance(plugins['dummy-plugin'], qiime.plugin.Plugin)

    def test_semantic_types(self):
        types = self.pm.semantic_types

        self.assertEqual(types['IntSequence1'], ('dummy-plugin', IntSequence1))
        self.assertEqual(types['IntSequence2'], ('dummy-plugin', IntSequence2))
        self.assertEqual(types['Mapping'], ('dummy-plugin', Mapping))
        self.assertEqual(types['FourInts'], ('dummy-plugin', FourInts))

if __name__ == '__main__':
    unittest.main()
