# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os


class Profile:
    SYSTEM_PATH = '/etc/qiime2/'
    HOME_PATH = os.path.expanduser('.config/qiime2/')

    def __init__(self, config):
        config_sections = config.sections()
        if 'dev' in config_sections:
            # TODO: This isn't going to work as-is, need to do something
            # smarter, like a `ProfileValue` object (or namedtuple).
            dev = config['dev']
            self.is_this_working = dev.get('is_this_working', None)

            dev_mode = dev.get('dev_mode')
            self.dev_mode = bool(dev_mode) if dev_mode else False

    @classmethod
    def read(self, filepath=None, profile=None, system=False):
        if not filepath and not profile:
            raise Exception
        if filepath and profile:
            raise Exception
        if filepath:
            pass
        if profile:
            pass

    @classmethod
    def write(self, filepath=None, profile=None, system=False):
        pass

    @classmethod
    def list(self):
        pass
