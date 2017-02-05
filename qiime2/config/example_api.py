from qiime2 import config


cfg = config.get_active_config()

cfg.profile_name
cfg.is_modified
cfg.diffs()
cfg.diffs(pretty=True)

config.from_ini('/path/to/foo')

with config.activate_profile('foo'):
    print(config.get_current_config())

Custom_Config = config.from_dict({'dev': {'is_this_working': True,
                                          'dev_mode': False}})
print(config.get_current_config())
with config.use_custom_config(Custom_Config):
    print(config.get_current_config())

config.add_profile('bar')
config.delete_profile('~/bar')
config.copy_profile('foo', 'bar')
config.backup_profile('bar')
config.list_profiles()
config.list_profiles(valid=True)

config.current_profile()

config.save_config_to_profile(Custom_Config, 'custom_profile')
