import configparser
import utils
import os

__author__ = 'Tomas Fiedor'
BKIT_CONFIG = "bkit.ini"

# Attempt to load config file, if the file does not exist yet,
# dummy file is created with empty [Global] section
config = configparser.ConfigParser()
if os.path.exists(BKIT_CONFIG):
    config.read(BKIT_CONFIG)
else:
    config.add_section('Global')
utils.log("Loaded config file: {}".format(BKIT_CONFIG))


def save_config():
    """Save configuration file to BKIT_CONFIG file path"""
    with open(BKIT_CONFIG, 'w') as config_file:
        config.write(config_file)
