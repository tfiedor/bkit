import os
import utils
import store
import config

__author__ = 'Tomas Fiedor'


def get_existing_bkit_dirs():
    """
    Checks the filesystem for existing .bkit directories,
    and collects them in list.

    Returns:
        List: List of existing bkit directories
    """
    bkits = []
    for root, _, _ in os.walk("/"):
        if root.endswith('.bkit'):
            bkits.append(root)
            print("Found .bkit at : {}".format(root))
    return bkits


def get_registered_bkits():
    """
    Returns registered bkit directories from config,
    that are available.

    Returns:
        List: List of registered bkit directories
    """
    return [
        section for section in config.config.sections() if os.path.exists(section)
    ]


def is_registered(bkit):
    """
    Arguments:
        bkit(directory): bkit directory that is checked
    Returns:
        bool: True if bkit is registered bkit directory
    """
    return config.config.has_section(bkit)


def register_bkit(bkit_directory):
    """
    Registers given bkit_directory inside the config.

    Arguments:
        bkit_directory(directory): directory of .bkit to be registered
    """
    if config.config.has_section(bkit_directory):
        utils.warn("{} already registered as bkit".format(bkit_directory))
    else:
        config.config.add_section(bkit_directory)
        config.config.set(bkit_directory, 'valid', 'true')


def initialize_bkit_dir(bkit_dir):
    """
    Unless the @p bkit_dir is not already initialized,
    create a basic structure for the bkit.

    Arguments:
        bkit_dir(path): destination to the bkit dir
    """
    if os.path.exists(bkit_dir):
        utils.warn("'%s' is already a valid .bkit directory" % bkit_dir)
    else:
        os.mkdir(bkit_dir)
        os.mkdir(os.path.join(bkit_dir, 'objects'))
        store.touch_file(os.path.join(bkit_dir, 'index.bkit'))
        store.touch_file(os.path.join(bkit_dir, 'config.ini'))
        utils.log('Successfully initialized bkit at \'%s\'' % bkit_dir)

        register_bkit(bkit_dir)
