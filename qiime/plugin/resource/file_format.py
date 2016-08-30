# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import abc

from .base import FormatBase


class _FileFormat(FormatBase, metaclass=abc.ABCMeta):
    pass


class TextFileFormat(_FileFormat):
    def open(self):
        return self.path.open(mode=self._mode, encoding='utf8')


class BinaryFileFormat(_FileFormat):
    def open(self):
        return self.path.open(mode=self._mode+'b')
