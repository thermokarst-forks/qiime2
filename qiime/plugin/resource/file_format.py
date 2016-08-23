# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import abc
import io
import shutil


class FileFormat(metaclass=abc.ABCMeta):
    def __init__(self, path=None, mode='w'):
        if path is None:
            self._path = TempPath(prefix='q2-%r' % self.__class__.__name__)
        else:
            self._path = path
        self.path = str(self._path)
        self.mode = mode

    def move(self, dst):
        """Matches shutil.move"""
        if not os.path.isfile(self.path):
            raise IOError("%r is not bound to a file." % self)
        shutil.move(self.path, dst)
        self.path = dst


class TextFileFormat(FileFormat):
    def open(self):
        return io.open(self.path, mode=self.mode, encoding='utf8')


class BinaryFileFormat(FileFormat):
    def open(self):
        return io.open(self.path, mode=self.mode+'b')
