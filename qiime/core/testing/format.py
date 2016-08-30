# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from qiime.plugin import TextFileFormat
import qiime.plugin.resource as resource


class IntSequenceFormat(TextFileFormat):
    pass


class MappingFormat(TextFileFormat):
    pass


class SingleIntFormat(TextFileFormat):
    pass


class IntSequenceDirectoryFormat(resource.DirectoryFormat):
    ints = resource.File('ints.txt', format=IntSequenceFormat)


class MappingDirectoryFormat(resource.DirectoryFormat):
    mapping = resource.File('mapping.tsv', format=MappingFormat)


class FourIntsDirectoryFormat(resource.DirectoryFormat):
    single_ints = resource.FileCollection('(nested/)?file[1-4]\.txt',
                                          format=SingleIntFormat)

    @single_ints.set_path_maker
    def single_ints_path_maker(self, num):
        if num > 2:
            return 'nested/file%d.txt' % num
        else:
            return 'file%d.txt' % num
