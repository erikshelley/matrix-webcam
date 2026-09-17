# matrix-webcam

[![PyPI version](https://badge.fury.io/py/matrix-webcam.svg)](https://badge.fury.io/py/matrix-webcam)
[![License MIT](https://img.shields.io/github/license/erikshelley/matrix-webcam.svg)](https://github.com/erikshelley/matrix-webcam/blob/main/LICENSE)
[![issues](https://img.shields.io/github/issues/erikshelley/matrix-webcam.svg)](https://github.com/erikshelley/matrix-webcam/issues)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

This package displays your webcam video feed as a matrix-rain effect.

Take your next video conference from within the matrix!

![matrix-webcam demo](https://raw.githubusercontent.com/erikshelley/matrix-webcam/main/doc/matrix-webcam02.gif)

## Running it

Install from source:

This project requires Python 3.11-3.13.

    $ git clone https://github.com/erikshelley/matrix-webcam.git
    $ cd matrix-webcam

| Environment          | Setup           | Run           |
| -------------------- | --------------- | ------------- |
| Windows PowerShell   | `.\setup.ps1`   | `.\run.ps1`   |
| Linux, macOS, or WSL | `bash setup.sh` | `bash run.sh` |

The setup scripts create `.venv` with Python 3.13 by default and install the project there. To use Python 3.11 or 3.12 instead, run `./setup.ps1 -PythonVersion 3.12` in PowerShell or `PYTHON_VERSION=3.12 bash setup.sh` on Linux, macOS, or WSL.

### Older WSL distributions

Ubuntu 20.04 and other older WSL distributions do not provide a supported Python version by default. To keep one Ubuntu distribution, upgrade the existing installation in place from 20.04 to 22.04, then from 22.04 to 24.04.

Before upgrading, back up the distribution from Windows PowerShell. Replace `<DistroName>` with the name from `wsl --list --verbose` (often `Ubuntu`):

    $ wsl --list --verbose
    $ wsl --shutdown
    $ wsl --export <DistroName> ubuntu-20.04-backup.tar

From Windows PowerShell, open the distribution:

    $ wsl -d <DistroName>

Inside the Ubuntu shell, check available disk space, held packages, and the current release before upgrading:

    $ df -h
    $ lsb_release -a
    $ apt-mark showhold

Do not upgrade if the root filesystem is near full (above about 80-90% used or with only a few GB free), if the release is not Ubuntu 20.04, or if `apt-mark showhold` lists packages. Free disk space first, investigate held packages before unholding them with `sudo apt-mark unhold <package-name>`, and do not skip releases. The first upgrade must start on 20.04; the second must start on 22.04. An empty `apt-mark showhold` result is expected.

Perform the first upgrade:

    $ sudo apt update
    $ sudo apt full-upgrade
    $ sudo dpkg --configure -a
    $ sudo apt -f install
    $ sudo apt autoremove
    $ sudo apt install update-manager-core
    $ sudo do-release-upgrade

After the first upgrade, exit the Ubuntu shell. From Windows PowerShell, restart WSL and reopen the distribution:

    $ wsl --shutdown
    $ wsl -d <DistroName>

Inside Ubuntu, verify the release and package state:

    $ lsb_release -a
    $ python3 --version
    $ sudo apt update
    $ sudo apt full-upgrade

Confirm that `lsb_release -a` reports Ubuntu 22.04 before repeating the upgrade steps to reach Ubuntu 24.04. Repeat the restart and verification steps after the final upgrade, then confirm that it reports Ubuntu 24.04. Test important tools, repositories, and files before deleting the export backup. The upgrade can require significant disk space and may disable third-party repositories. Ubuntu 20.04 is end-of-life, so its package sources may require adjustment before the first upgrade.

To roll back if the upgrade has problems, return to Windows PowerShell, unregister the upgraded distribution, and restore the export. `wsl --unregister` permanently deletes the current distribution, so only use it after confirming the backup archive exists:

    $ wsl --shutdown
    $ wsl --unregister <DistroName>
    $ wsl --import <DistroName> C:\WSL\<DistroName> ubuntu-20.04-backup.tar --version 2

From Windows PowerShell, open the restored distribution as its original Linux user:

    $ wsl -d <DistroName> -u <LinuxUser>

Use an empty directory for `C:\WSL\<DistroName>`. The restored distribution contains its original users and files; specify the original Linux username with `-u` on the first launch.

## Configuration

Edit [matrix-webcam.toml](matrix-webcam.toml) to set defaults for all runtime options. The run scripts load it automatically. Command-line options override the file; for example, `./run.ps1 --width 1920` uses the configured values except for `width`.

## Increasing Resolution

The default resolution of the local OpenCV window is 1280x720.
You can use Zoom's screen/window capture to show it.
The preview requires a graphical display server. On WSL, use WSLg or configure an X server, and ensure the distribution can access the webcam. Native Windows is recommended for the simplest setup.
WSLg is available in modern WSL installations but is not guaranteed with WSL2. In Windows PowerShell, run `wsl --version`; if the output includes a WSLg version, it is available. If it is missing, try `wsl --update`, then restart WSL with `wsl --shutdown`. If WSLg remains unavailable, configure an X server instead.
For a 1080p-capable webcam, request full HD with:

    $ .\run.ps1 --width 1920 --height 1080
    $ bash run.sh --width 1920 --height 1080

To make the Matrix characters smaller while preserving that resolution, add `--cell-size 8`:

    $ .\run.ps1 --width 1920 --height 1080 --cell-size 8
    $ bash run.sh --width 1920 --height 1080 --cell-size 8

The default cell size is 14 pixels. Smaller values increase visual detail but require more processing.
The app prints the resolution actually provided by the camera at startup.
Close the window with its title-bar X, or focus it and press `Esc` or `q` to stop the app.

### Usage

| Option                                                             | Default   | Description                                                                 |
| ------------------------------------------------------------------ | --------- | --------------------------------------------------------------------------- |
| `-h`, `--help`                                                     | N/A       | Show help and exit.                                                         |
| `-d DEVICE`, `--device DEVICE`                                     | `0`       | Webcam device index.                                                        |
| `-l LETTERS`, `--letters LETTERS`                                  | `2`       | Letters produced per update. (How heavy is the rain)                        |
| `-p PROBABILITY`, `--probability PROBABILITY`                      | `5`       | Each point has a $1/p$ chance of deactivating each update. (1/evaporation)  |
| `-u UPDATES_PER_SECOND`, `--updates-per-second UPDATES_PER_SECOND` | `15`      | Number of updates per second.                                               |
| `--width WIDTH`                                                    | `1280`    | Requested preview width in pixels.                                          |
| `--height HEIGHT`                                                  | `720`     | Requested preview height in pixels.                                         |
| `--cell-size CELL_SIZE`                                            | `14`      | Matrix character-cell size in pixels. Smaller values increase detail.       |
| `--output {preview}`                                               | `preview` | Render to a local OpenCV preview window.                                    |

## Zoom and other video apps

The project now supports the local preview window as the only output path.

### Local preview window
Run:

    $ python -m matrix_webcam --output preview

Then in Zoom, select the preview window using screen/window capture instead of a camera input.

This is the supported output path for the application.

## Development

Create a virtual environment and install the project in editable mode:

    $ python -m venv .venv
    $ . .venv/bin/activate  # Linux, macOS, or WSL
    $ .\.venv\Scripts\Activate.ps1  # Windows PowerShell
    $ .\.venv\Scripts\activate.bat  # Windows Command Prompt
    $ python -m pip install -e .[dev]

Then run the project tests or smoke checks:

    $ python -m ruff check .
    $ python -m mypy matrix_webcam
    $ pre-commit install

## License
This project is licensed under the MIT License (see the `LICENSE` file for details).
