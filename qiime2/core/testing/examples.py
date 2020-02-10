# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2 import Artifact

from qiime2.plugin import UsageAction, UsageInputs, UsageOutputNames

from .type import IntSequence1, IntSequence2, Mapping


def ints1_factory():
    return Artifact.import_data(IntSequence1, [0, 1, 2])


def ints2_factory():
    return Artifact.import_data(IntSequence1, [3, 4, 5])


def ints3_factory():
    return Artifact.import_data(IntSequence2, [6, 7, 8])


def mapping1_factory():
    return Artifact.import_data(Mapping, {'a': 42})


def concatenate_ints_simple(use):
    ints_a = use.init_data('ints_a', ints1_factory)
    ints_b = use.init_data('ints_b', ints2_factory)
    ints_c = use.init_data('ints_c', ints3_factory)

    use.comment('This example demonstrates basic usage.')
    use.action(
        UsageAction(plugin_id='dummy_plugin', action_name='concatenate_ints'),
        UsageInputs(ints1=ints_a, ints2=ints_b, ints3=ints_c, int1=4, int2=2),
        UsageOutputNames(concatenated_ints='ints_d'),
    )


def concatenate_ints_complex(use):
    ints_a = use.init_data('ints_a', ints1_factory)
    ints_b = use.init_data('ints_b', ints2_factory)
    ints_c = use.init_data('ints_c', ints3_factory)

    use.comment('This example demonstrates chained usage (pt 1).')
    use.action(
        UsageAction(plugin_id='dummy_plugin', action_name='concatenate_ints'),
        UsageInputs(ints1=ints_a, ints2=ints_b, ints3=ints_c, int1=4, int2=2),
        UsageOutputNames(concatenated_ints='ints_d'),
    )

    ints_d = use.get_result('ints_d')
    use.comment('This example demonstrates chained usage (pt 2).')
    use.action(
        UsageAction(plugin_id='dummy_plugin', action_name='concatenate_ints'),
        UsageInputs(ints1=ints_d, ints2=ints_b, ints3=ints_c, int1=41, int2=0),
        UsageOutputNames(concatenated_ints='concatenated_ints'),
    )


def typical_pipeline_simple(use):
    ints = use.init_data('ints', ints1_factory)
    mapper = use.init_data('mapper', mapping1_factory)

    use.action(
        UsageAction(plugin_id='dummy_plugin', action_name='typical_pipeline'),
        UsageInputs(int_sequence=ints, mapping=mapper, do_extra_thing=True),
        UsageOutputNames(out_map='out_map', left='left', right='right',
                         left_viz='left_viz', right_viz='right_viz')
    )


def typical_pipeline_complex(use):
    ints1 = use.init_data('ints1', ints1_factory)
    mapper1 = use.init_data('mapper1', mapping1_factory)

    use.action(
        UsageAction(plugin_id='dummy_plugin', action_name='typical_pipeline'),
        UsageInputs(int_sequence=ints1, mapping=mapper1, do_extra_thing=True),
        UsageOutputNames(out_map='out_map1', left='left1', right='right1',
                         left_viz='left_viz1', right_viz='right_viz1')
    )

    ints2 = use.get_result('left1')
    mapper2 = use.get_result('out_map1')

    use.action(
        UsageAction(plugin_id='dummy_plugin', action_name='typical_pipeline'),
        UsageInputs(int_sequence=ints2, mapping=mapper2, do_extra_thing=False),
        # TODO with and without overwriting
        UsageOutputNames(out_map='out_map2', left='left2', right='right2',
                         left_viz='left_viz2', right_viz='right_viz2')
    )

    right2 = use.get_result('right2')
    right2.assert_has_line_matching(
        label='a nice label about this assertion',
        path='.*/data/ints.txt',
        expression='1',
    )


def comments_only(use):
    # TODO
    pass
