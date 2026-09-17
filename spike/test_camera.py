"""Phase 0 step 5 spike: confirm cv2.VideoCapture can actually open the webcam and read a frame."""
import cv2

for name, backend in [("default", cv2.CAP_ANY), ("DSHOW", cv2.CAP_DSHOW), ("MSMF", cv2.CAP_MSMF)]:
    cap = cv2.VideoCapture(0, backend)
    opened = cap.isOpened()
    frame_ok = False
    shape = None
    if opened:
        frame_ok, frame = cap.read()
        if frame_ok:
            shape = frame.shape
    cap.release()
    print(f"backend={name}: isOpened={opened} frame_read={frame_ok} shape={shape}")
