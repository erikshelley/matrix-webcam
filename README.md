# matrix-webcam

[![PyPI version](https://badge.fury.io/py/matrix-webcam.svg)](https://badge.fury.io/py/matrix-webcam)
[![License MIT](https://img.shields.io/github/license/joschuck/matrix-webcam.svg)](https://github.com/joschuck/matrix-webcam/blob/main/LICENSE)
[![issues](https://img.shields.io/github/issues/joschuck/matrix-webcam.svg)](https://github.com/joschuck/matrix-webcam/issues)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

This package displays your webcam video feed as a matrix-rain effect.

Take your next video conference from within the matrix!

![matrix-webcam demo](https://raw.githubusercontent.com/joschuck/matrix-webcam/main/doc/matrix-webcam02.gif)

## Running it

Install from source:

    $ git clone https://github.com/joschuck/matrix-webcam.git
    $ cd matrix-webcam
    $ python -m pip install -e .

Then run the local preview mode:

    $ python -m matrix_webcam --output preview

A local OpenCV window opens at a requested 1280x720 resolution and you can use Zoom's screen/window capture to show it.
For a 1080p-capable webcam, request full HD with:

    $ python -m matrix_webcam --width 1920 --height 1080

To make the Matrix characters smaller while preserving that resolution, add `--cell-size 8`:

    $ python -m matrix_webcam --width 1920 --height 1080 --cell-size 8

The default cell size is 14 pixels. Smaller values increase visual detail but require more processing.
The app prints the resolution actually provided by the camera at startup.
Close the window with its title-bar X, or focus it and press `Esc` or `q` to stop the app.

### Usage

    usage: matrix-webcam [-h] [-d DEVICE] [-l LETTERS] [-p PROBABILITY] [-u UPDATES_PER_SECOND] [--width WIDTH] [--height HEIGHT] [--cell-size CELL_SIZE] [--output {preview}]

    options:
    -h, --help            show this help message and exit
    -d DEVICE, --device DEVICE
                        Sets the index of the webcam if you have more than one webcam.
    -l LETTERS, --letters LETTERS
                        The number of letters produced per update.
    -p PROBABILITY, --probability PROBABILITY
                        1/p probability of a dispense point deactivating each tick.
    -u UPDATES_PER_SECOND, --updates-per-second UPDATES_PER_SECOND
                        The number of updates to perform per second.
    --width WIDTH       Requested preview width in pixels.
    --height HEIGHT     Requested preview height in pixels.
    --cell-size CELL_SIZE
                        Matrix character-cell size in pixels; smaller values increase detail.
    --output {preview}
                        Render to a local OpenCV preview window.

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
    $ . .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows
    $ python -m pip install -e .[dev]

Then run the project tests or smoke checks:

    $ python -m ruff check .
    $ python -m mypy matrix_webcam

## License
This project is licensed under the MIT License (see the `LICENSE` file for details).


## Development

I'd recommend creating a new virtual environment (if you are under Ubuntu install it using `sudo apt install python3-venv` using 

    $ python3 -m venv venv/
    $ source venv/bin/activate

Then install the dependencies using:

    $ pip install -e .[dev,deploy]

Setup pre-commit, too:

    $ pre-commit install

### TODO

* [x] add webcam selection
* [ ] Move to opencv-python-headless
* [ ] add tests

## License
This project is licensed under the MIT License (see the `LICENSE` file for details).
