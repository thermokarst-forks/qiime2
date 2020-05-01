# ----------------------------------------------------------------------------
# Copyright (c) 2016-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd

from qiime2 import Metadata, CategoricalMetadataColumn

from qiime2.plugin import UsageAction, UsageInputs, UsageOutputNames


def ints1_factory():
    return [0, 1, 2]


def ints2_factory():
    return [3, 4, 5]


def ints3_factory():
    return [6, 7, 8]


def mapping1_factory():
    return {'a': 42}


def md1_factory():
    return Metadata(pd.DataFrame({'a': ['1', '2', '3']},
                                 index=pd.Index(['0', '1', '2'],
                                                name='id')))


def md2_factory():
    return Metadata(pd.DataFrame({'b': ['4', '5', '6']},
                                 index=pd.Index(['0', '1', '2'],
                                                name='id')))


def mdc1_factory():
    return CategoricalMetadataColumn(pd.Series(['1', '2', '3'],
                                     name='a',
                                     index=pd.Index(['0', '1', '2'],
                                                    name='id')))


def concatenate_ints_simple(use):
    ints_a = use.init_data('ints_a', ints1_factory, 'IntSequence1')
    ints_b = use.init_data('ints_b', ints2_factory, 'IntSequence1')
    ints_c = use.init_data('ints_c', ints3_factory, 'IntSequence2')

    use.comment('This example demonstrates basic usage.')
    use.action(
        UsageAction(plugin_id='dummy_plugin', action_id='concatenate_ints'),
        UsageInputs(ints1=ints_a, ints2=ints_b, ints3=ints_c, int1=4, int2=2),
        UsageOutputNames(concatenated_ints='ints_d'),
    )


def concatenate_ints_complex(use):
    ints_a = use.init_data('ints_a', ints1_factory, 'IntSequence1')
    ints_b = use.init_data('ints_b', ints2_factory, 'IntSequence1')
    ints_c = use.init_data('ints_c', ints3_factory, 'IntSequence2')

    use.comment('This example demonstrates chained usage (pt 1).')
    use.action(
        UsageAction(plugin_id='dummy_plugin', action_id='concatenate_ints'),
        UsageInputs(ints1=ints_a, ints2=ints_b, ints3=ints_c, int1=4, int2=2),
        UsageOutputNames(concatenated_ints='ints_d'),
    )

    ints_d = use.get_result('ints_d')
    use.comment('This example demonstrates chained usage (pt 2).')
    use.action(
        UsageAction(plugin_id='dummy_plugin', action_id='concatenate_ints'),
        UsageInputs(ints1=ints_d, ints2=ints_b, ints3=ints_c, int1=41, int2=0),
        UsageOutputNames(concatenated_ints='concatenated_ints'),
    )


def typical_pipeline_simple(use):
    ints = use.init_data('ints', ints1_factory, 'IntSequence1')
    mapper = use.init_data('mapper', mapping1_factory, 'Mapping')

    use.action(
        UsageAction(plugin_id='dummy_plugin', action_id='typical_pipeline'),
        UsageInputs(int_sequence=ints, mapping=mapper, do_extra_thing=True),
        UsageOutputNames(out_map='out_map', left='left', right='right',
                         left_viz='left_viz', right_viz='right_viz')
    )


def typical_pipeline_complex(use):
    ints1 = use.init_data('ints1', ints1_factory, 'IntSequence1')
    mapper1 = use.init_data('mapper1', mapping1_factory, 'Mapping')
    use.action(
        UsageAction(plugin_id='dummy_plugin', action_id='typical_pipeline'),
        UsageInputs(int_sequence=ints1, mapping=mapper1, do_extra_thing=True),
        UsageOutputNames(out_map='out_map1', left='left1', right='right1',
                         left_viz='left_viz1', right_viz='right_viz1')
    )

    ints2 = use.get_result('left1')
    mapper2 = use.get_result('out_map1')

    use.action(
        UsageAction(plugin_id='dummy_plugin', action_id='typical_pipeline'),
        UsageInputs(int_sequence=ints2, mapping=mapper2, do_extra_thing=False),
        UsageOutputNames(out_map='out_map2', left='left2', right='right2',
                         left_viz='left_viz2', right_viz='right_viz2')
    )

    right2 = use.get_result('right2')
    right2.assert_has_line_matching(
        label='a nice label about this assertion',
        path='ints.txt',
        expression='1',
    )


def comments_only(use):
    use.comment('comment 1')
    use.comment('comment 2')


def identity_with_metadata_simple(use):
    ints = use.init_data('ints', ints1_factory, 'IntSequence1')
    md = use.init_data('md', md1_factory, 'Metadata')

    use.action(
        UsageAction(plugin_id='dummy_plugin',
                    action_id='identity_with_metadata'),
        UsageInputs(ints=ints, metadata=md),
        UsageOutputNames(out='out'),
    )


def identity_with_metadata_merging(use):
    ints = use.init_data('ints', ints1_factory, 'IntSequence1')
    md1 = use.init_data('md1', md1_factory, 'Metadata')
    md2 = use.init_data('md2', md2_factory, 'Metadata')

    md3 = use.merge_metadata('md3', md1, md2)

    use.action(
        UsageAction(plugin_id='dummy_plugin',
                    action_id='identity_with_metadata'),
        UsageInputs(ints=ints, metadata=md3),
        UsageOutputNames(out='out'),
    )


def identity_with_metadata_column_get_mdc(use):
    ints = use.init_data('ints', ints1_factory, 'IntSequence1')
    md = use.init_data('md', md1_factory, 'Metadata')

    mdc = use.get_metadata_column('mdc', md, 'a')

    use.action(
        UsageAction(plugin_id='dummy_plugin',
                    action_id='identity_with_metadata_column'),
        UsageInputs(ints=ints, metadata=mdc),
        UsageOutputNames(out='out'),
    )


def identity_with_metadata_column_from_factory(use):
    ints = use.init_data('ints', ints1_factory)
    mdc = use.init_data('mdc', mdc1_factory)

    use.action(
        UsageAction(plugin_id='dummy_plugin',
                    action_id='identity_with_metadata_column'),
        UsageInputs(ints=ints, metadata=mdc),
        UsageOutputNames(out='out'),
    )


def optional_inputs(use):
    ints_a = use.init_data('ints', ints1_factory)

    use.action(
        UsageAction(plugin_id='dummy_plugin',
                    action_id='optional_artifacts_method'),
        UsageInputs(ints=ints_a, num1=1),
        UsageOutputNames(output='output'),
    )

    use.action(
        UsageAction(plugin_id='dummy_plugin',
                    action_id='optional_artifacts_method'),
        UsageInputs(ints=ints_a, num1=1, num2=2),
        UsageOutputNames(output='output'),
    )

    use.action(
        UsageAction(plugin_id='dummy_plugin',
                    action_id='optional_artifacts_method'),
        UsageInputs(ints=ints_a, num1=1, num2=None),
        UsageOutputNames(output='ints_b'),
    )

    ints_b = use.get_result('ints_b')

    use.action(
        UsageAction(plugin_id='dummy_plugin',
                    action_id='optional_artifacts_method'),
        UsageInputs(ints=ints_a, optional1=ints_b, num1=3, num2=4),
        UsageOutputNames(output='output'),
    )
