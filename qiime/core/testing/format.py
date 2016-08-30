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
    def sniff(self):
        with self.open() as fh:
            for line, _ in zip(fh, range(5)):
                try:
                    int(line.rstrip('\n'))
                except (TypeError, ValueError):
                    return False
            return True


class MappingFormat(TextFileFormat):
    def sniff(self):
        with self.open() as fh:
            for line, _ in zip(fh, range(5)):
                cells = line.rstrip('\n').split('\t')
                if len(cells) != 2:
                    return False
            return True


class SingleIntFormat(TextFileFormat):
    def sniff(self):
        with self.open() as fh:
            try:
                int(fh.readline().rstrip('\n'))
            except (TypeError, ValueError):
                return False
        return True


IntSequenceDirectoryFormat = resource.SingleFileDirectoryFormat(
    'IntSequenceDirectoryFormat', 'ints.txt', IntSequenceFormat)


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
