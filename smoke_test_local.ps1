$ErrorActionPreference = "Stop"

$venvPython = Join-Path $PSScriptRoot ".venv311\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    throw "Could not find virtual environment at $venvPython"
}

@'
import cv2
import time
from matrix_webcam.segmentation import SelfieSegmenter
from matrix_webcam.rain import MatrixRain

cap = cv2.VideoCapture(0)
ok, frame = cap.read()
if not ok or frame is None:
    raise RuntimeError("Could not read a frame from webcam device 0.")

rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
with SelfieSegmenter() as seg:
    mask = seg.segment(rgb, int(time.monotonic() * 1000))

out = MatrixRain(frame.shape[1], frame.shape[0]).render(frame, mask)
cv2.imwrite("matrix_debug_out.png", out)
print("saved matrix_debug_out.png")
cap.release()
'@ | & $venvPython -

if (Test-Path (Join-Path $PSScriptRoot "matrix_debug_out.png")) {
    Write-Host "Smoke test succeeded. Open matrix_debug_out.png to verify the effect."
} else {
    throw "Smoke test did not produce matrix_debug_out.png"
}
