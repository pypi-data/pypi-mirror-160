import click
from click_didyoumean import DYMGroup

from .cli_base import cli
from ..implementation import idevice


@cli.group(cls=DYMGroup)
def device():
    """ Device commands """
    pass


@device.command('info')
@click.option(
    '--json', 'as_json', is_flag=True,
    help='Show data in json format.'
)
def device_info(as_json: bool):
    """ Get device information """
    idevice.device_info_impl(as_json)


@device.command('reboot')
def device_reboot():
    """ Reboot the router without any confirmation prompts """
    idevice.device_reboot_impl()
