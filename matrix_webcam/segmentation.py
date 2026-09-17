"""Selfie segmentation using the Mediapipe Tasks API (replaces the removed Solutions API)."""
from __future__ import annotations

import pathlib
import urllib.request

import mediapipe as mp
import numpy as np
import numpy.typing as npt
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/image_segmenter/"
    "selfie_segmenter/float16/latest/selfie_segmenter.tflite"
)
_CACHE_DIR = pathlib.Path.home() / ".cache" / "matrix_webcam"
_MODEL_PATH = _CACHE_DIR / "selfie_segmenter.tflite"

# Matches the confidence threshold the original mediapipe Solutions-API code used.
CONFIDENCE_THRESHOLD = 0.95


def _resolve_model_path() -> pathlib.Path:
    """Downloads the selfie segmenter model to a local cache dir on first use."""
    if not _MODEL_PATH.exists():
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(_MODEL_URL, _MODEL_PATH)
    return _MODEL_PATH


class SelfieSegmenter:
    """Wraps mediapipe's Tasks-API ImageSegmenter for per-frame person/background masking."""

    def __init__(self) -> None:
        options = vision.ImageSegmenterOptions(
            base_options=python.BaseOptions(model_asset_path=str(_resolve_model_path())),
            running_mode=vision.RunningMode.VIDEO,
            output_category_mask=False,
            output_confidence_masks=True,
        )
        self._segmenter = vision.ImageSegmenter.create_from_options(options)
        self._last_timestamp_ms = -1

    def segment(self, frame_rgb: npt.NDArray[np.uint8], timestamp_ms: int) -> npt.NDArray[np.bool_]:
        """Returns a boolean mask (True = person) for the given RGB frame."""
        if timestamp_ms <= self._last_timestamp_ms:
            timestamp_ms = self._last_timestamp_ms + 1
        self._last_timestamp_ms = timestamp_ms

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        result = self._segmenter.segment_for_video(mp_image, timestamp_ms)
        confidence = result.confidence_masks[0].numpy_view()
        return np.asarray(confidence > CONFIDENCE_THRESHOLD, dtype=np.bool_)

    def close(self) -> None:
        self._segmenter.close()

    def __enter__(self) -> SelfieSegmenter:
        return self

    def __exit__(self, *_exc_info: object) -> None:
        self.close()
