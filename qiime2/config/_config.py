# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import pathlib
from contextlib import contextmanager
from unittest.mock import patch


class Config:
    def __init__(self, profile_name_or_path=None):
        if profile_name_or_path is not None and os.sep in profile_name_or_path:
            path = pathlib.Path(profile_name_or_path)
            if path.suffix != '.ini':
                raise Exception('Invalid config file path')
            profile_name_or_path = path.stem
        self.profile = profile_name_or_path

    def __repr__(self):
        return 'Config<profile=%s>' % self.profile

    def __getitem__(self, item):
        print('getting item: %s' % item)


active_config = Config()


def get_active_config():
    return active_config


@contextmanager
def activate_profile(profile_name_or_path):
    config = Config(profile_name_or_path)
    with patch('qiime2.config._config.active_config', config):
        yield
