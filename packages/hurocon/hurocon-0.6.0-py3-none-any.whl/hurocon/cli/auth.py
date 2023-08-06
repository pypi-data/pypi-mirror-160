import click
from click_didyoumean import DYMGroup

from ..implementation import iauth
from .cli_base import cli


@cli.group(cls=DYMGroup)
def auth():
    """ Router authentication """
    pass


@auth.command('login')
@click.argument('username', required=False, type=str)
@click.argument('password', required=False, type=str)
@click.argument('connection_address', required=False, type=str)
def auth_login(username: str, password: str, connection_address: str):
    """
    Safely configure all authentication related details for further interactions

    To provide all details with one command, specify the USERNAME and PASSWORD
    positional arguments. CONNECTION_ADDRESS is optional, and will be set to
    default value (192.168.8.1) if not provided.
    """
    iauth.auth_login_impl(username, password, connection_address)


@auth.command('logout')
def auth_logout():
    """ Remove all authentication details """
    iauth.auth_logout_impl()


@auth.command('test')
def auth_test_connection():
    """ Test connection to router with current auth details """
    iauth.auth_test_connection_impl()
