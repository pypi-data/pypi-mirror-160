import json

from huawei_lte_api.Client import Client
from huawei_lte_api.enums.device import ControlModeEnum

from ..core.io import printx
from ..core.connection import HRC_Connection


def device_info_impl(as_json: bool):
    """ Get device information """
    try:
        with HRC_Connection() as conn:
            client = Client(conn)
            device_info_dict = client.device.information()
    except Exception as e:
        msg = 'Can not get device information, reason: "{}"' \
              .format(e)
    else:
        if not as_json:
            msg = ''
            for k, v in device_info_dict.items():
                msg += '• {}: {}\n'.format(k, v)
            msg = msg[:-1]
        else:
            msg = json.dumps(device_info_dict)

    printx(msg)


def device_reboot_impl():
    """ Reboot the router without any confirmation prompts """
    try:
        with HRC_Connection() as conn:
            Client(conn).device.set_control(ControlModeEnum.REBOOT)
    except Exception as e:
        msg = 'Execution failed, reason: "{}"'.format(e)
    else:
        msg = 'Rebooting the device, router will restart in several moments'

    printx(msg, limit_line_length=True)
