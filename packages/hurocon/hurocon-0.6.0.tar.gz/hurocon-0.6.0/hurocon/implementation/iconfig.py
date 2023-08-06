from ..core.io import printx
from ..core.local_cfg import LocalConfig
from ..core.const import LOCAL_CONFIG_PATH


def config_init_impl():
    cfg = LocalConfig(auto_file_creation=False)

    if not cfg.file_exists():
        if cfg.create_file():
            printx('Configuration file successfully generated at "{}"'
                   .format(LOCAL_CONFIG_PATH),
                   limit_line_length=True
                   )
        else:
            printx('Can not generate configuration file at "{}"'
                   .format(LOCAL_CONFIG_PATH),
                   limit_line_length=True
                   )
    else:
        printx('Configuration file already exists on path: "{}"'
               .format(LOCAL_CONFIG_PATH),
               limit_line_length=True
               )


def config_remove_impl():
    if LocalConfig.erase_config() is True:
        printx("All local configuration files and dirs successfully erased")
    else:
        printx("No local configuration files detected")


def config_get_path_impl():
    printx(LOCAL_CONFIG_PATH)


def config_exist_impl():
    if LOCAL_CONFIG_PATH.exists() is True:
        printx("Configuration file do exist")
    else:
        printx("Configuration file doesn't exist")
