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
    $ python -m pip install -e .
    $ python -m matrix_webcam

To install in an isolated virtual environment instead:

Create it with Python 3.11, 3.12, or 3.13. If `.venv` was created with another version, remove it and recreate it.

| Environment     | Command                    |
| --------------- | -------------------------- |
| Windows         | `py -3.13 -m venv .venv`   |
| Linux/macOS/WSL | `python3.13 -m venv .venv` |

Activate the virtual environment:

| Environment     | Command                        |
| --------------- | ------------------------------ |
| PowerShell      | `.\.venv\Scripts\Activate.ps1` |
| Linux/macOS/WSL | `. .venv/bin/activate`         |

Install dependencies in the virtual environment, then run it.

    $ python -m pip install -e .
    $ python -m matrix_webcam

After installing the project in `.venv`, you can run it later without activating the virtual environment:

| Environment     | Command                                       |
| --------------- | --------------------------------------------- |
| PowerShell      | `.\.venv\Scripts\python.exe -m matrix_webcam` |
| Linux/macOS/WSL | `./.venv/bin/python -m matrix_webcam`         |

## Increasing Resolution

A local OpenCV window opens at a requested 1280x720 resolution and you can use Zoom's screen/window capture to show it.
The preview requires a graphical display server. On WSL, use WSLg or configure an X server, and ensure the distribution can access the webcam. Native Windows is recommended for the simplest setup.
For a 1080p-capable webcam, request full HD with:

    $ python -m matrix_webcam --width 1920 --height 1080

To make the Matrix characters smaller while preserving that resolution, add `--cell-size 8`:

    $ python -m matrix_webcam --width 1920 --height 1080 --cell-size 8

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
