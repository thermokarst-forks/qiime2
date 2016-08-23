# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import abc


class FileFormat(metaclass=abc.ABCMeta):
    name = NotImplemented

    @classmethod
    @abc.abstractmethod
    def sniff(cls, filepath):
        raise NotImplementedError
