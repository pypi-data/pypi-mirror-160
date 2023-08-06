from sys import exit  # Base for `pyinstaller` impl. Default exit() will not work.
from shutil import rmtree
from base64 import b64encode, b64decode

import jsonschema
from serialix import JSON_Format

from .. import meta
from .io import printx
from .const import LOCAL_CONFIG_PATH, LOCAL_CONFIG_DEFAULT, LOCAL_CONFIG_SCHEMA


_config_update_checked = False


class LocalConfig(JSON_Format):
    def __init__(self, **kwargs):
        super().__init__(
            LOCAL_CONFIG_PATH, LOCAL_CONFIG_DEFAULT,
            parser_write_kwargs={"indent": 4},
            **kwargs
        )

        if self.file_exists():
            self.__check_updates()
            self.__validate_schema()

    def __check_updates(self):
        global _config_update_checked

        if not _config_update_checked:
            local_version = self.get('config_version', None)
            if local_version is None: self.__config_corrupted_notice()
            builtin_version = LOCAL_CONFIG_DEFAULT['config_version']

            if local_version > builtin_version:
                # Exit if local config was generated with newer version of hurocon
                printx(
                    '! Version of the local configuration file is newer than {app_name} ({app_version}) supports.'
                    '\n\n• Local version: {confv_local}'
                    '\n• Supported version: {confv_builtin}'
                    .format(app_name=meta.name, app_version=meta.version,
                            confv_local=local_version, confv_builtin=builtin_version),
                    limit_line_length=True
                )
                printx(
                    '\nThis may happen when you downgrade {app_name} to version, that'
                    ' used the old scheme of configuration system. Consider upgrading'
                    ' to a newer version of {app_name} or clean the configuration '
                    'files. You can erase all configuration files running this command:'
                    '\n\n\t$ hurocon config remove'.format(app_name=meta.name),
                    limit_line_length=True
                )
                exit()
            elif local_version < builtin_version:
                if local_version < 2:
                    self['connection_address'] = 'http://{}/'.format(
                        self.get('connection_ip', '')
                    )

                    self.pop('connection_ip', None)

                    self['auth']['password'] = b64encode(
                        self
                        .get('auth', {})
                        .get('password',
                             LOCAL_CONFIG_DEFAULT['auth']['password']
                             ).encode()
                    ).decode()

                if local_version < 3:
                    self['connection'] = {
                        'address': self.get('connection_address',
                                            LOCAL_CONFIG_DEFAULT['connection']['address']),
                        'timeout': LOCAL_CONFIG_DEFAULT['connection']['timeout']
                    }

                    self.pop('connection_address', None)

                self['config_version'] = builtin_version
                self.commit()

            _config_update_checked = True

    def __validate_schema(self):
        try:
            jsonschema.validate(self.dictionary, LOCAL_CONFIG_SCHEMA)
        except Exception:
            self.__config_corrupted_notice()

    @staticmethod
    def __config_corrupted_notice():
        printx('! Configuration file is corrupted'
               '\n│ Please reset it by running the following commands'
               '\n├   $ hurocon config remove'
               '\n└   $ hurocon config init')
        exit()

    @staticmethod
    def erase_config() -> bool:
        """
        Erase all local configuration files and dirs

        :return: Do the existing file was successfully removed
        :rtype: bool
        """
        result = False

        if LOCAL_CONFIG_PATH.parent.exists():
            rmtree(LOCAL_CONFIG_PATH.parent)
            result = True

        return result


class AuthConfig():
    username = ""
    connection_address = ""

    def __init__(self) -> None:
        self.__cfg = LocalConfig()
        self.username = self.__cfg['auth']['username']
        self.__password = self.__cfg['auth']['password']
        self.connection_address = self.__cfg['connection']['address']

    def commit(self):
        self.__cfg['auth']['username'] = self.username
        self.__cfg['auth']['password'] = self.__password
        self.__cfg['connection']['address'] = self.connection_address
        self.__cfg.commit()

    def reset(self):
        self.__cfg.reset_to_defaults()
        self.__cfg.commit()

    @property
    def password(self) -> str:
        return b64decode(self.__password).decode()

    @password.setter
    def password(self, passwd: str) -> None:
        self.__password = b64encode(passwd.encode()).decode()
