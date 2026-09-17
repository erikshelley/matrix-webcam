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

Ubuntu 20.04 and other older WSL distributions may not provide a supported Python version by default. See [Upgrading an Older WSL Distribution](doc/wsl-upgrade.md) for the in-place upgrade, verification, and rollback guidance.

## Configuration

Edit [matrix-webcam.toml](matrix-webcam.toml) to set defaults for all runtime options. The run scripts load it automatically. The included configuration uses Full HD (`1920x1080`), 30 updates per second, 8-pixel cells, 8 new rain sources per update, probability 4, and a segmentation threshold of `0.95`. Command-line options override the file; for example, `./run.ps1 --width 3840` uses the configured values except for `width`. Raise `segmentation_threshold` above `0.95` to make the foreground mask stricter, which can exclude background objects but may also remove details of the person.

## Increasing Resolution

The included configuration requests a 1920x1080 Full HD preview window. The webcam may provide a different actual resolution, which the application prints at startup.
You can use Zoom's screen/window capture to show it.
The preview requires a graphical display server. On WSL, use WSLg or configure an X server, and ensure the distribution can access the webcam. Native Windows is recommended for the simplest setup.
WSLg is available in modern WSL installations but is not guaranteed with WSL2. In Windows PowerShell, run `wsl --version`; if the output includes a WSLg version, it is available. If it is missing, try `wsl --update`, then restart WSL with `wsl --shutdown`. If WSLg remains unavailable, configure an X server instead.

| Preset | Resolution | Command |
| --- | --- | --- |
| Full HD | 1920x1080 | Included configuration; run `./run.ps1` or `bash run.sh`. |
| 4K | 3840x2160 | `./run.ps1 --width 3840 --height 2160` or `bash run.sh --width 3840 --height 2160` |

4K requires a 4K-capable webcam and substantially more CPU and GPU resources. Keep `--cell-size 8` or increase it if rendering is slow.

To make the Matrix characters smaller while preserving the selected resolution, lower `--cell-size`:

    $ .\run.ps1 --width 1920 --height 1080 --cell-size 8
    $ bash run.sh --width 1920 --height 1080 --cell-size 8

The included configuration uses 8-pixel cells. Smaller values increase visual detail but require more processing.
Close the window with its title-bar X, or focus it and press `Esc` or `q` to stop the app.

### Usage

| Option                                                             | Configured default | Description                                                                 |
| ------------------------------------------------------------------ | --------- | --------------------------------------------------------------------------- |
| `-h`, `--help`                                                     | N/A                | Show help and exit.                                                         |
| `-d DEVICE`, `--device DEVICE`                                     | `0`                | Webcam device index.                                                        |
| `-l LETTERS`, `--letters LETTERS`                                  | `8`                | Letters produced per update. (How heavy is the rain)                        |
| `-p PROBABILITY`, `--probability PROBABILITY`                      | `4`                | Each point has a $1/p$ chance of deactivating each update. (1/evaporation)  |
| `-u UPDATES_PER_SECOND`, `--updates-per-second UPDATES_PER_SECOND` | `30`               | Number of updates per second.                                               |
| `--width WIDTH`                                                    | `1920`             | Requested preview width in pixels.                                          |
| `--height HEIGHT`                                                  | `1080`             | Requested preview height in pixels.                                         |
| `--cell-size CELL_SIZE`                                            | `8`                | Matrix character-cell size in pixels. Smaller values increase detail.       |
| `--segmentation-threshold THRESHOLD`                               | `0.95`             | Foreground confidence required for a pixel to be shown.                     |
| `--output {preview}`                                               | `preview`          | Render to a local OpenCV preview window.                                    |

## Zoom and other video apps

The application renders to a local preview window; it does not create a virtual webcam device.

### Share the preview window

In Zoom, use screen/window sharing and select the `matrix-webcam` preview window. This shares the effect without replacing your camera feed.

### Replace the Zoom camera feed

On Windows, use OBS Virtual Camera as a bridge:

1. Start Matrix Webcam with `./run.ps1`.
2. In OBS, add a Window Capture source for the `matrix-webcam` window.
3. Start OBS Virtual Camera.
4. In Zoom's camera menu, select OBS Virtual Camera.

This replaces the Zoom camera feed without screen sharing.

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
