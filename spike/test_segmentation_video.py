"""Phase 2 prep spike: confirm confidence-mask output + VIDEO running mode semantics before writing the real module."""
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = "spike/selfie_segmenter.tflite"

image = np.zeros((256, 256, 3), dtype=np.uint8)
image[64:192, 64:192] = 200
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

options = vision.ImageSegmenterOptions(
    base_options=python.BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=vision.RunningMode.VIDEO,
    output_category_mask=False,
    output_confidence_masks=True,
)

with vision.ImageSegmenter.create_from_options(options) as segmenter:
    for i in range(3):
        result = segmenter.segment_for_video(mp_image, i * 33)
        masks = result.confidence_masks
        print(f"frame {i}: num_confidence_masks={len(masks)}")
        for idx, m in enumerate(masks):
            arr = m.numpy_view()
            print(f"  mask[{idx}] shape={arr.shape} dtype={arr.dtype} min={arr.min():.3f} max={arr.max():.3f}")
    print("SMOKE TEST PASSED")
