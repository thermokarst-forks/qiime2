# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

r"""
The Metadata (:mod:`qiime2.metadata`)
=====================================

Foo
"""


from .metadata import (Metadata, MetadataColumn, NumericMetadataColumn,
                       CategoricalMetadataColumn)
from .io import MetadataFileError


__all__ = ['Metadata', 'MetadataColumn', 'NumericMetadataColumn',
           'CategoricalMetadataColumn', 'MetadataFileError']
