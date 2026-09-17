"""Phase 0 step 7 spike: confirm non-blocking ESC keypress detection via msvcrt (no Enter needed)."""
import msvcrt
import time

print("Loop running. Press ESC to exit (no Enter needed). Ctrl+C also works as a fallback.", flush=True)
tick = 0
try:
    while True:
        tick += 1
        print(f"tick={tick}", flush=True)
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch == b"\x1b":
                print("ESC detected -- exiting cleanly without blocking.", flush=True)
                break
            print(f"other key detected: {ch!r} (ignored)", flush=True)
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Ctrl+C detected -- exiting cleanly.", flush=True)
print("DONE", flush=True)
