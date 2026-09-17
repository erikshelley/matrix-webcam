"""Phase 0 step 4 spike: confirm Mediapipe Tasks ImageSegmenter works end-to-end. Throwaway script."""
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = "spike/selfie_segmenter.tflite"

# Synthetic 256x256 RGB test image (a bright square on a dark background, no real webcam needed).
image = np.zeros((256, 256, 3), dtype=np.uint8)
image[64:192, 64:192] = 200

mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

options = vision.ImageSegmenterOptions(
    base_options=python.BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=vision.RunningMode.IMAGE,
    output_category_mask=True,
)

with vision.ImageSegmenter.create_from_options(options) as segmenter:
    result = segmenter.segment(mp_image)
    mask = result.category_mask.numpy_view()
    print("mask shape:", mask.shape, "dtype:", mask.dtype)
    print("unique values:", np.unique(mask))
    print("SMOKE TEST PASSED")
