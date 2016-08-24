# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import abc
import io


class _FileFormat(metaclass=abc.ABCMeta):
    def __init__(self, path=None, mode='w'):
        if path is None:
            self._backing_path = path.OutPath(
                prefix='q2-%s-' % self.__class__.__name__
            )
        else:
            self._backing_path = path
        self.path = str(self._backing_path)
        self._mode = mode


class TextFileFormat(_FileFormat):
    def open(self):
        return io.open(self.path, mode=self._mode, encoding='utf8')


class BinaryFileFormat(_FileFormat):
    def open(self):
        return io.open(self.path, mode=self._mode+'b')
