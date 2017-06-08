# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2
import qiime2.plugin

from ._tabulate import tabulate


framework_plugin = qiime2.plugin.Plugin(
    name='framework',
    description='Builtin actions',
    short_description='Builtin actions',
    version=qiime2.__version__,
    website='https://github.com/qiime2/qiime2',
    package='qiime2.sdk.framework_plugin',
    citation_text='No relevant citation.',
    user_support_text='For help, see https://qiime2.org',
)


framework_plugin.visualizers.register_function(
    function=tabulate,
    inputs={},
    parameters={'metadata': qiime2.plugin.Metadata},
    name='tabulate',
    description='foo'
)
