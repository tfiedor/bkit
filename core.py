import os
import utils
import store
import config

__author__ = 'Tomas Fiedor'


class BkitRepository(object):
    """Wrapper over bkit directory"""
    def __init__(self, directory="", tag="", registered=True):
        """
        Arguments:
            directory(pathname): path to the bkit directory
            tag(string): tag for the bkit directory
            registered(bool): true if the bkit is registered in the config
        """
        self.dir = directory
        self.tag = tag
        self.registered = registered

    def __repr__(self):
        return "{}@{}".format(self.tag, self.dir)


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


def register_bkit(bkit_directory, tag=""):
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
        config.config.set(bkit_directory, 'tag', tag)


def translate_bkit_id(id):
    """Translates the identification of bkit repository to unique id

    Since the user can either use the tag identification or the path
    identifications to identify which bkit directory he wants to use
    this takes care of it.

    Arguments:
        id(str): either pathname or tag

    Returns:
        str: pathname (or section name from config) of bkit
    """
    config_sections = config.config.sections()
    tags = {str(config.config.get(section, 'tag')): section
            for section in config_sections if section != "Global"
            }

    id_is_pathname = id in config_sections
    id_is_tag = id in tags.keys()

    # Warn user that the given id can be both pathname and tag
    if id_is_pathname and id_is_tag:
        utils.warn("'{}' is both tag and valid path name to bkit".format(id))
        return id
    # Abort with exceptions, not a bkit directory at all
    elif not id_is_pathname and not id_is_tag:
        raise utils.BkitFailureException("{} does not represents valid "
                                         "bkit directory".format(id))
    # Nothing to translate
    elif id_is_pathname:
        return id
    else:
        assert id_is_tag
        return tags[id]


def create_bkit_from_id(id, init=False):
    """Create a bkit object represented by id

    Attributes:
        id(str): either pathname to the valid bkit or tagname

    Returns:
        BkitRepository: bkit represented by the id
    """
    # if we are creating bkit by running bkit init
    # we don't construct the object at all
    if init:
        return BkitRepository(id, id)

    bkit_path = translate_bkit_id(id)
    bkit_tag = config.config.get(bkit_path, 'tag')
    bkit = BkitRepository(bkit_path, bkit_tag)

    return bkit


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
