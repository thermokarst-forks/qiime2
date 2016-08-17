# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import collections

from .resource_type import ResourceMeta


ResourcePattern = collections.namedtuple('ResourcePattern',
                                         ['resource_type', 'pattern'])


def view_interpreter(view_type: type) -> ResourcePattern:
    if type(view_type) is ResourceMeta:
        return ResourcePattern(view_type.__name__, view_type.__pattern__)
    else:
        return ResourcePattern('Object', view_type)
