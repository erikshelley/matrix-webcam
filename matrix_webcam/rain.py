"""Renders the digital-rain matrix effect onto video frames (pixels)."""
from __future__ import annotations

import random
import time
from string import printable

import cv2
import numpy as np
import numpy.typing as npt

ASCII_CHARS = [" ", "@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]
_FONT = cv2.FONT_HERSHEY_SIMPLEX
_GREEN_BGR = (0, 255, 0)


def _rand_string(character_set: str, length: int) -> str:
    return "".join(random.choice(character_set) for _ in range(length))


def _ascii_grid(image: npt.NDArray[np.uint8], cols: int, rows: int) -> list[str]:
    """Maps each grid cell's brightness to one of ASCII_CHARS, like the original ascii_image()."""
    small = cv2.resize(image, (cols, rows))
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    scale = 256 / len(ASCII_CHARS)
    return ["".join(ASCII_CHARS[int(pixel / scale)] for pixel in row) for row in gray]


class MatrixRain:
    """Stateful renderer: composites a segmented person as ASCII art plus falling rain streaks."""

    def __init__(
        self,
        width: int,
        height: int,
        letters: int = 2,
        probability: int = 5,
        updates_per_second: float = 15.0,
        cell_size: int = 14,
    ) -> None:
        self.width = width
        self.height = height
        self.letters = letters
        self.probability = probability
        self.updates_per_second = updates_per_second
        self.cols = max(1, width // cell_size)
        self.rows = max(1, height // cell_size)
        self._cell_w = width / self.cols
        self._cell_h = height / self.rows
        self._font_scale = self._cell_h / 30

        self._background = _rand_string(printable.strip(), self.cols * self.rows)
        self._foreground: list[tuple[int, int]] = []
        self._dispense: list[int] = []
        self._bg_refresh_counter = random.randint(3, 7)
        self._delta = 0.0
        self._perf_counter = time.perf_counter()

    def render(
        self, frame_bgr: npt.NDArray[np.uint8], mask: npt.NDArray[np.bool_]
    ) -> npt.NDArray[np.uint8]:
        """Returns a new BGR frame: segmented person as ASCII art, with rain streaks over it."""
        composited = np.where(mask, frame_bgr, 0).astype(np.uint8)
        canvas = np.zeros_like(frame_bgr)

        for row, line in enumerate(_ascii_grid(composited, self.cols, self.rows)):
            for col, char in enumerate(line):
                if char != " ":
                    self._draw_char(canvas, row, col, char)

        update_matrix = self._tick()

        next_foreground = []
        for row, col in self._foreground:
            self._draw_char(canvas, row, col, self._background[row * self.cols + col])
            if row < self.rows - 1:
                next_foreground.append((row + 1, col) if update_matrix else (row, col))
        self._foreground = next_foreground

        if update_matrix:
            self._dispense_new_rain()

        self._maybe_refresh_background()
        return canvas

    def _tick(self) -> bool:
        now = time.perf_counter()
        self._delta += (now - self._perf_counter) * abs(self.updates_per_second)
        self._perf_counter = now
        update_matrix = self._delta >= 1
        if update_matrix:
            self._delta -= 1
        return update_matrix

    def _dispense_new_rain(self) -> None:
        for _ in range(abs(self.letters)):
            self._dispense.append(random.randint(0, self.cols - 1))
        # 1/probability chance per tick that a dispense point deactivates.
        self._dispense = [
            column for column in self._dispense if random.randint(0, self.probability - 1)
        ]
        for column in self._dispense:
            self._foreground.append((0, column))

    def _maybe_refresh_background(self) -> None:
        self._bg_refresh_counter -= 1
        if self._bg_refresh_counter <= 0:
            self._background = _rand_string(printable.strip(), self.cols * self.rows)
            self._bg_refresh_counter = random.randint(3, 7)

    def _draw_char(self, canvas: npt.NDArray[np.uint8], row: int, col: int, char: str) -> None:
        x = int(col * self._cell_w)
        y = int((row + 1) * self._cell_h)
        cv2.putText(canvas, char, (x, y), _FONT, self._font_scale, _GREEN_BGR, 1, cv2.LINE_AA)
