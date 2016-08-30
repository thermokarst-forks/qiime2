# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import qiime.core.path as qpath


class FormatBase:
    def __init__(self, path=None, mode='w'):
        import qiime.plugin.resource as resource
        if path is None:
            assert(mode == 'w')
        else:
            assert(mode == 'r')

        if mode == 'w':
            self.path = qpath.OutPath(
                dir=isinstance(self, resource.DirectoryFormat),
                prefix='q2-%s-' % self.__class__.__name__)
        else:
            self.path = qpath.InPath(path)

        self._mode = mode
