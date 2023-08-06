from typing import Callable


def get_cli() -> Callable:
    """
    Initialize CLI, prepare all modules

    :return: Click CLI object. (Used in unit-tests)
    """
    from .cli_base import cli

    # Initialize CLI modules
    from . import auth, config, device, sms, net, \
        lte  # Deprecated modules on this line

    return cli


def run_cli():
    """ Run CLI """
    cli_ready = get_cli()
    cli_ready()
