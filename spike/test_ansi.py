"""Phase 0 step 6 spike: confirm ANSI escape codes work, and whether VT processing must be enabled manually."""
import ctypes
import sys

ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
STD_OUTPUT_HANDLE = -11

kernel32 = ctypes.windll.kernel32
handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

mode = ctypes.c_uint32()
got_mode = kernel32.GetConsoleMode(handle, ctypes.byref(mode))
print(f"GetConsoleMode succeeded={bool(got_mode)} raw_mode={mode.value:#06x}", flush=True)
print(f"VT flag already set: {bool(mode.value & ENABLE_VIRTUAL_TERMINAL_PROCESSING)}", flush=True)

print("BEFORE enabling VT explicitly:", flush=True)
sys.stdout.write("\x1b[32mGREEN-TEST-1\x1b[0m (should be green if VT already on)\n")
sys.stdout.flush()

new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
set_ok = kernel32.SetConsoleMode(handle, new_mode)
print(f"SetConsoleMode(ENABLE_VIRTUAL_TERMINAL_PROCESSING) succeeded={bool(set_ok)}", flush=True)

print("AFTER enabling VT explicitly:", flush=True)
sys.stdout.write("\x1b[32mGREEN-TEST-2\x1b[0m (should be green now)\n")
sys.stdout.write("\x1b[?25lCURSOR-HIDDEN-TEST\x1b[?25h\n")
sys.stdout.flush()
print("DONE", flush=True)
