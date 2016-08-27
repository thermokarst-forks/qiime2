# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import typing

from .format import (
    IntSequenceDirectoryFormat,
    FourIntsDirectoryFormat,
    MappingDirectoryFormat,
    IntSequenceFormat,
    SingleIntFormat,
    MappingFormat,
)


def _1(view: typing.List[int]) -> FourIntsDirectoryFormat:
    odm = FourIntsDirectoryFormat()
    for i, int_ in enumerate(view, 1):
        odm.single_ints.add(int_, int, num=i)
    return odm


def _2(data: int) -> SingleIntFormat:
    outfile = SingleIntFormat()
    with outfile.open() as fh:
        fh.write('%d\n' % data)
    return outfile


def _3(view: typing.List[int]) -> IntSequenceDirectoryFormat:
    odm = IntSequenceDirectoryFormat()
    odm.IntSequence.set(view, typing.List[int])
    return odm


def _4(view: typing.List[int]) -> IntSequenceFormat:
    outfile = IntSequenceFormat()
    with outfile.open() as fh:
        for int_ in view:
            fh.write('%d\n' % int_)
    return outfile


def _5(view: typing.Dict[str, str]) -> MappingDirectoryFormat:
    odm = MappingDirectoryFormat()
    odm.Mapping.set(view, dict)
    return odm


def _6(view: typing.Dict[str, str]) -> MappingFormat:
    outfile = MappingFormat()
    with outfile.open() as fh:
        for key, value in view.items():
            fh.write('%s\t%s\n' % (key, value))
    return outfile


def _7(df: FourIntsDirectoryFormat) -> typing.List[int]:
    return df.single_ints.view(typing.List[int])
