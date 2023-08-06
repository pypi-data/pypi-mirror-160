# Hurocon
Hurocon *(**hu**awei **ro**uter **con**trol)* - command line interface tool for interacting with Huawei LTE routers


- [Features](#features)
- [Supported Devices](#supported-devices)
- [Availability](#availability)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Development](#development)
- [Special](#special)


## Features
- Device Control
  - Information
  - Reboot
- Net
  - Cellular
    - Connection status
    - Switch connection
  - LAN
    - List devices
- SMS
  - Inbox: List, View
  - Send

> There are many features planned for future releases, you can view their full list [here](https://github.com/maximilionus/hurocon/projects/1)


## Supported Devices
Full list of supported devices is available on [this link](https://github.com/Salamek/huawei-lte-api#tested-on).


## Availability
This tool is OS-independent, which means it should work on any platform where python3 can run. Minimal python3 version required for this package is `3.7`. This does not mean that it cannot work on python versions below the minimal, but its behavior is unpredictable and no support will be provided for any issues.


## Installation
- You can install it from PyPi:

  ```bash
  pip install hurocon
  ```

- Or directly from Github repo:

  ```bash
  pip install git+https://github.com/maximilionus/hurocon.git
  ```

> Currently can only be installed with `pip` on `python >= 3.7`. Binary bundle *([pyinstaller](https://pyinstaller.org/)-based)* is planned but no ETA yet


## Quickstart
### Intro
After successful [installation](#installation) of this tool it can be accessed in shell using the following commands:

```bash
$ hurocon
# OR
$ python -m hurocon
```

You can also view a list of all main commands with:
```bash
$ hurocon --help
```

Each command and subcommand in this tool has a special `--help` flag to display detailed information about it

### Authentication
Foremost, you need to specify the authentication details so that this tool can access the device.
``` bash
$ hurocon auth login
```

### Testing Connection
After auth details successfully specified you can test your connection with router by running

```bash
$ hurocon auth test

# Returns
# Success: Successful Authentication
# Failure: Auth failed, reason: "..."
```

### Conclusion
That's it, you're ready to go. And remember - no matter how deep you go, `--help` flag is always here to help 👍


## Development
### Prepare The Environment
To prepare the development environment for this project, follow these steps:

1. Install `poetry` package manager with ([pip](https://pypi.org/project/poetry/), [standalone](https://python-poetry.org/docs/master/#installing-with-the-official-installer) *(recommended)*)

2. Run the command below to prepare the virtual environment for this project
   ```bash
   $ poetry install
   ```

3. That's it, now you can modify the code the way you want and test it in two ways
    - Run this tool with
      ```bash
      $ poetry run hurocon
      ```
    - Or activate the project environment with
      ```bash
      $ poetry shell
      Spawning shell within ...

      $ hurocon
      ```

### Build
#### Python Package
To build this tool to package *([sdist](https://docs.python.org/3/distutils/sourcedist.html) and wheel)* you should execute:

```bash
$ poetry build
Building hurocon ...
```

Prepared for distribution package will be located in `./dist/` directory


## Special
Big thanks to [Adam Schubert](https://github.com/Salamek) for his amazing [`huawei-lte-api`](https://github.com/Salamek/huawei-lte-api) package, that made this whole thing possible.
