from qiime2 import config


Config = config.get_active_config()

Config.profile_name()
Config.is_modified()
Config.diffs()
Config.diffs(pretty=True)

Config['dev']['is_this_working']
Config['dev']['is_this_working'].is_modified()
Config['dev']['is_this_working'].diff()

Config['dev']  # return list of section keys
Config.sections()  # return list of sections
Config.is_current()

type(Config['dev'])  # ConfigSection
type(Config['dev']['is_this_working'])  # ConfigValue

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

config.save_config_to_profile(Custom_Config, 'custom_profile')
