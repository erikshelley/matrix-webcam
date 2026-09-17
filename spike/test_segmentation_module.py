"""Ad-hoc verification of matrix_webcam.segmentation.SelfieSegmenter against real webcam frames."""
import cv2
from matrix_webcam.segmentation import SelfieSegmenter

cap = cv2.VideoCapture(0)
with SelfieSegmenter() as segmenter:
    for i in range(3):
        ok, frame_bgr = cap.read()
        assert ok
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mask = segmenter.segment(frame_rgb, i * 33)
        print(f"frame {i}: mask shape={mask.shape} dtype={mask.dtype} person_pixels={mask.sum()}")
cap.release()
print("MODULE SMOKE TEST PASSED")
