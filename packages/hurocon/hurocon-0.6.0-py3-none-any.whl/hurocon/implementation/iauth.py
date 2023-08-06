from pwinput import pwinput

from huawei_lte_api.Client import Client

from ..core.io import printx
from ..core.local_cfg import AuthConfig
from ..core.connection import HRC_Connection
from ..core.const import LOCAL_CONFIG_DEFAULT


def auth_login_impl(username: str, password: str, connection_address: str):
    if None in (username, password):
        printx('Authentication Configurator\n')
        con_ip = input(
            '  (leave empty to use "{}")\n'
            '• Full address to router: '
            .format(LOCAL_CONFIG_DEFAULT['connection']['address'])
        )
        uname = input('• Username: ')
        passwd = pwinput(prompt='• Password: ')
    else:
        con_ip = connection_address if connection_address is not None \
            else LOCAL_CONFIG_DEFAULT['connection']['address']
        uname = username
        passwd = password

    auth_cfg = AuthConfig()
    auth_cfg.username = uname
    auth_cfg.password = passwd
    auth_cfg.connection_address = con_ip if len(con_ip) > 0 else \
        LOCAL_CONFIG_DEFAULT['connection']['address']

    auth_cfg.commit()

    printx("\nAuthentication details successfully specified")


def auth_logout_impl():
    AuthConfig().reset()
    AuthConfig().commit()
    printx("All authentication details removed")


def auth_test_connection_impl():
    try:
        with HRC_Connection() as router_con:
            Client(router_con)
    except Exception as e:
        msg = 'Auth failed, reason: "{}"'.format(e)
    else:
        msg = 'Successful Authentication'

    printx(msg, limit_line_length=True)
