from click_didyoumean import DYMGroup

from .cli_base import cli
from ..implementation import iconfig


@cli.group(cls=DYMGroup)
def config():
    """ CLI configuration """


@config.command('init')
def config_init():
    """
    Initialize local configuration file

    File will only be generated if no configuration file already exists
    on default path.
    """
    iconfig.config_init_impl()


@config.command('remove')
def config_remove():
    """ Erase local configuration """
    iconfig.config_remove_impl()


@config.command('path')
def config_get_path():
    """
    Path to local configuration file

    Note that this command will show the hardcoded path to config file, so it
    doesn't mean that this file actually exists at the time the command is
    called
    """
    iconfig.config_get_path_impl()


@config.command('exist')
def config_exist():
    """ Check does the local configuration file exists """
    iconfig.config_exist_impl()
