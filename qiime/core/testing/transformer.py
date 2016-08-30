# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------
import collections

from .format import (
    IntSequenceDirectoryFormat,
    FourIntsDirectoryFormat,
    MappingDirectoryFormat,
    IntSequenceFormat,
    SingleIntFormat,
    MappingFormat,
)
from .plugin import dummy_plugin

@dummy_plugin.register_transformer
def _1(view: list) -> FourIntsDirectoryFormat:
    odm = FourIntsDirectoryFormat()
    for i, int_ in enumerate(view, 1):
        odm.single_ints.add(int_, int, num=i)
    return odm

@dummy_plugin.register_transformer
def _2(odm: FourIntsDirectoryFormat) -> list:
    return list(odm.single_ints.view(int))


@dummy_plugin.register_transformer
def _2(data: int) -> SingleIntFormat:
    outfile = SingleIntFormat()
    with outfile.open() as fh:
        fh.write('%d\n' % data)
    return outfile


@dummy_plugin.register_transformer
def _(ff: SingleIntFormat) -> int:
    with ff.open() as fh:
        return int(fh.read())


@dummy_plugin.register_transformer
def _3(view: list) -> IntSequenceDirectoryFormat:
    odm = IntSequenceDirectoryFormat()
    odm.ints.set(view, list)
    return odm


@dummy_plugin.register_transformer
def _(odm: IntSequenceDirectoryFormat) -> list:
    return odm.ints.view(list)


@dummy_plugin.register_transformer
def _4(view: list) -> IntSequenceFormat:
    outfile = IntSequenceFormat()
    with outfile.open() as fh:
        for int_ in view:
            fh.write('%d\n' % int_)
    return outfile


@dummy_plugin.register_transformer
def _(ff: IntSequenceFormat) -> list:
    print(ff)
    with ff.open() as fh:
        return list(map(int, fh.readlines()))


@dummy_plugin.register_transformer
def _(odm: IntSequenceDirectoryFormat) -> collections.Counter:
    return odm.ints.view(collections.Counter)


@dummy_plugin.register_transformer
def _(ff: IntSequenceFormat) -> collections.Counter:
    x = ff.path
    print(x)
    print(x.exists())
    print(ff)
    with ff.open() as fh:
        return collections.Counter(map(int, fh.readlines()))


@dummy_plugin.register_transformer
def _5(view: dict) -> MappingDirectoryFormat:
    odm = MappingDirectoryFormat()
    odm.mapping.set(view, dict)
    return odm


@dummy_plugin.register_transformer
def _6(view: dict) -> MappingFormat:
    outfile = MappingFormat()
    with outfile.open() as fh:
        for key, value in view.items():
            fh.write('%s\t%s\n' % (key, value))
    return outfile
