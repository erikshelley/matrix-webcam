"""Phase 2 prep spike: confirm confidence-mask semantics using a real webcam frame (not synthetic)."""
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = "spike/selfie_segmenter.tflite"

cap = cv2.VideoCapture(0)
ok, frame_bgr = cap.read()
cap.release()
assert ok, "failed to read a webcam frame"

frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

options = vision.ImageSegmenterOptions(
    base_options=python.BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=vision.RunningMode.VIDEO,
    output_category_mask=False,
    output_confidence_masks=True,
)

with vision.ImageSegmenter.create_from_options(options) as segmenter:
    result = segmenter.segment_for_video(mp_image, 0)
    masks = result.confidence_masks
    print(f"num_confidence_masks={len(masks)}")
    for idx, m in enumerate(masks):
        arr = m.numpy_view()
        above_95 = (arr > 0.95).sum()
        print(
            f"mask[{idx}] shape={arr.shape} dtype={arr.dtype} "
            f"min={arr.min():.3f} max={arr.max():.3f} mean={arr.mean():.3f} "
            f"pixels_above_0.95={above_95}"
        )
print("SMOKE TEST PASSED")
