"""Matrix webcam effect rendered in a local preview window."""
from __future__ import annotations

import argparse
import sys
import time

import cv2
import numpy as np

from matrix_webcam.rain import MatrixRain
from matrix_webcam.segmentation import SelfieSegmenter


def _positive_int(value: str) -> int:
    parsed_value = int(value)
    if parsed_value < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed_value


def parse_args() -> argparse.Namespace:
    """Parses the webcam, rain-effect, and output-mode settings from the CLI."""
    parser = argparse.ArgumentParser(description="matrix-webcam")
    parser.add_argument(
        "-d",
        "--device",
        type=int,
        default=0,
        help="Sets the index of the webcam if you have more than one webcam.",
    )
    parser.add_argument(
        "-l",
        "--letters",
        type=int,
        default=2,
        help="The number of letters produced per update.",
    )
    parser.add_argument(
        "-p",
        "--probability",
        type=int,
        default=5,
        help="1/p probability of a dispense point deactivating each tick.",
    )
    parser.add_argument(
        "-u",
        "--updates-per-second",
        type=int,
        default=15,
        help="The number of updates to perform per second.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1280,
        help="Requested preview width in pixels.",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=720,
        help="Requested preview height in pixels.",
    )
    parser.add_argument(
        "--cell-size",
        type=_positive_int,
        default=14,
        help="Matrix character-cell size in pixels; smaller values increase detail.",
    )
    parser.add_argument(
        "--output",
        choices=("preview",),
        default="preview",
        help="Render to a local OpenCV preview window.",
    )
    return parser.parse_args()


def _open_capture(device: int) -> cv2.VideoCapture:
    """Open the selected local webcam device or exit with a clear message."""
    cap = cv2.VideoCapture(device)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open webcam device index {device}.")
    return cap


def _render_loop(args: argparse.Namespace, cap: cv2.VideoCapture) -> int:
    """Render the processed frames in a local preview window."""
    window_name = "matrix-webcam"
    rain = MatrixRain(
        width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640),
        height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480),
        letters=args.letters,
        probability=args.probability,
        updates_per_second=float(args.updates_per_second),
        cell_size=args.cell_size,
    )

    with SelfieSegmenter() as segmenter:
        while True:
            success, frame = cap.read()
            if not success or frame is None:
                print("Ignoring empty camera frame.", file=sys.stderr)
                continue

            frame_rgb = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB).astype(
                np.uint8, copy=False
            )
            mask = segmenter.segment(frame_rgb, int(time.monotonic() * 1000))
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR).astype(np.uint8, copy=False)
            output = rain.render(frame_bgr, mask)

            cv2.imshow(window_name, output)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break

    return 0


def main() -> int:
    """Capture webcam frames, segment the person, render the matrix effect, and stream it."""
    args = parse_args()

    cap = cv2.VideoCapture(args.device)
    if not cap.isOpened():
        print(f"No webcam found for device index {args.device}.", file=sys.stderr)
        return 1
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    try:
        frame = None
        for _attempt in range(1, 6):
            success, frame = cap.read()
            if success and frame is not None:
                break
            time.sleep(0.25)

        if frame is None or not success:
            print(
                "Could not read a frame from the webcam. If another app is already using the "
                "camera, close it or choose a different device index.",
                file=sys.stderr,
            )
            return 1

        print(f"Preview resolution: {frame.shape[1]}x{frame.shape[0]}")
        return _render_loop(args, cap)

    except KeyboardInterrupt:
        print("\nStopping matrix-webcam.")
        return 0
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    raise SystemExit(main())
