from huawei_lte_api.Client import Client

from ..core.io import printx
from ..core.connection import HRC_Connection


def cellular_status_impl():
    try:
        with HRC_Connection() as conn:
            con_stat = Client(conn).dial_up.mobile_dataswitch()['dataswitch']
    except Exception as e:
        cli_msg = 'Execution failed, reason: "{}"'.format(e)
    else:
        cli_msg = 'Connected to cellular network' if con_stat == '1' else \
                  'No connection to cellular network'

    printx(cli_msg, limit_line_length=True)


def cellular_set_connection_impl(mode: bool):
    try:
        with HRC_Connection() as conn:
            Client(conn).dial_up.set_mobile_dataswitch(int(mode))
    except Exception as e:
        cli_msg = 'Can not switch connection mode, reason: "{}"'.format(e)
    else:
        cli_msg = 'Successfully {} cellular data'.format('enabled' if mode else 'disabled')

    printx(cli_msg, limit_line_length=True)


def lan_list_connected_impl(count_only: bool):
    cli_msg = ''
    try:
        with HRC_Connection() as conn:
            response = Client(conn).wlan.host_list()
            devices: list = response['Hosts']['Host']

            cli_msg += '• Devices Connected: {}'.format(len(devices))

            if not count_only:
                cli_msg += '\n\n'
                for device in devices:
                    line = 1
                    for k, v in device.items():
                        cli_msg += '• ' if line == 1 else '  '
                        cli_msg += '{}: {}\n'.format(k, v)
                        line += 1
                cli_msg = cli_msg[:-1]  # Cut the ending `\n`
    except Exception as e:
        cli_msg = 'Cannot process the lan devices list, reason: "{}"'.format(e)

    printx(cli_msg)
