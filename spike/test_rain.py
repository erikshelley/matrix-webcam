"""Ad-hoc verification of matrix_webcam.rain.MatrixRain against real webcam + segmentation frames."""
import cv2
from matrix_webcam.rain import MatrixRain
from matrix_webcam.segmentation import SelfieSegmenter

cap = cv2.VideoCapture(0)
ok, frame = cap.read()
assert ok
height, width = frame.shape[:2]

rain = MatrixRain(width=width, height=height)
with SelfieSegmenter() as segmenter:
    for i in range(45):
        ok, frame_bgr = cap.read()
        assert ok
        frame_bgr = cv2.flip(frame_bgr, 1)
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mask = segmenter.segment(frame_rgb, i * 33)
        rendered = rain.render(frame_bgr, mask)
        if i == 44:
            cv2.imwrite("spike/rain_preview.png", rendered)
cap.release()
print("RAIN RENDER SMOKE TEST PASSED -- wrote spike/rain_preview.png")
