from qiime2.config import Config, config_profile

print(Config)
# > Config<profile=None>

print(Config.valid)
# > True

print(Config.values)
# > {
# >     'dev':
# >         {
# >             'is_this_working': 'hello world',
# >             'dev_mode': True,
# >         }
# > }

with config_profile('foo'):
    print(Config)
    # > Config<profile='foo'>


with config_profile('/path/to/bar'):
    print(Config)
    # > Config<profile='bar'>


# With a 'default' profile in the search path:
print(Config)
# > Config<profile='default'>


print(Config.list_valid_profiles())
# > ['default', 'foo', 'bar']

print(Config.list_invalid_profiles())
# > ['baz']


Config.new_profile('quux')
Config.delete_profile('quux')
Config.backup('/path/to/default')  # appends unix timestamp
print(Config.list_valid_profiles())
# > ['default', 'default-1484261576', 'foo', 'bar']
