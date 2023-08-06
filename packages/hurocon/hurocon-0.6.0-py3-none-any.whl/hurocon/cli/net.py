import click
from click_didyoumean import DYMGroup

from .cli_base import cli
from ..implementation import inet


@cli.group(cls=DYMGroup)
def net():
    """ Network controls """
    pass


# Cellular cli group
@net.group(cls=DYMGroup)
def cellular():
    """ Cellular connection controls """
    pass


@cellular.command('status')
def cellular_status():
    """ Get cellular connection status """
    inet.cellular_status_impl()


@cellular.command('set')
@click.argument('mode', required=True, type=bool)
def cellular_set_connection(mode: bool):
    """
    Enable or disable cellular connection

    MODE (bool): True, False | [Y]es, [N]o | 1, 0
    """
    inet.cellular_set_connection_impl(mode)


# LAN cli group
@net.group(cls=DYMGroup)
def lan():
    """ Lan connection controls """


@lan.command('list')
@click.option(
    '--count-only', '-C', 'count_only',
    is_flag=True,
    help='Show only number of connected devices, no additional info'
)
# ? How 'bout json output support ?
def lan_list_connected(count_only: bool):
    """ List devices connected to network """
    inet.lan_list_connected_impl(count_only)
