"""
This module is deprecated and will be removed in version `1.0.0`.
Use `net cellular` cli group instead.
"""

import click
from click_didyoumean import DYMGroup

from .cli_base import cli
from ..implementation import inet


@cli.group(cls=DYMGroup, hidden=True)
def lte():
    """
    [DEPRECATED] Cellular connection controls

    This cli group will be removed in "1.0.0" version,
    use "net cellular" cli group instead.
    """
    pass


@lte.command('status')
def lte_status():
    """ Get cellular connection status """
    inet.cellular_status_impl()


@lte.command('set')
@click.argument('mode', required=True, type=bool)
def lte_set_connection(mode: bool):
    """
    Enable or disable cellular connection

    MODE (bool): True, False | [Y]es, [N]o | 1, 0
    """
    inet.cellular_set_connection_impl(mode)
