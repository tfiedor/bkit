import os
import utils
import store

__author__ = 'Tomas Fiedor'


def get_existing_bkit_dirs():
    """
    Checks the filesystem for existing .bkit directories,
    and collects them in list.

    Returns:
        List: List of existing bkit directories
    """
    return []


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
