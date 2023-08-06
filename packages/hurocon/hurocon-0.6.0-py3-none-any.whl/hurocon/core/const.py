from pathlib import Path


LOCAL_CONFIG_PATH = Path.home() / Path('.config/hurocon/config.json')
LOCAL_CONFIG_DEFAULT = {
    "config_version": 3,
    "connection": {
        "address": "http://192.168.8.1/",
        "timeout": 5.0
    },
    "auth": {
        "username": "admin",
        "password": "YWRtaW4="
    }
}
LOCAL_CONFIG_SCHEMA = {'type': 'object',
                       'properties': {'config_version': {'type': 'integer'},
                                      'auth': {'type': 'object',
                                               'properties': {'username': {'type': 'string'},
                                                              'password': {'type': 'string'}},
                                               'required': ['username', 'password']},
                                      'connection': {'type': 'object',
                                                     'properties': {'address': {'type': 'string'},
                                                                    'timeout': {'type': 'number'}},
                                                     'required': ['address', 'timeout']}},
                       'required': ['config_version', 'auth', 'connection']}
