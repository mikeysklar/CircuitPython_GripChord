import time
import board
import digitalio
from adafruit_hid.keycode import Keycode

from gripchord import GripChord
import chords_config   # required by your constructor, even if unused yet


# ─── Switch inputs ────────────────────────────────────────────────
SW_PINS = (
    board.IO6,
    board.IO5,
    board.IO4,
    board.IO2,
    board.IO7,
)

pins = []
for gp in SW_PINS:
    p = digitalio.DigitalInOut(gp)
    p.direction = digitalio.Direction.INPUT
    p.pull = digitalio.Pull.UP
    pins.append(p)


# ─── GripChord engine ──────────────────────────────────────────────
gc = GripChord(pins, chords_config)

print("GripChord ready")

# ─── magic key decoder ─────────────────────────────────────────────
def key_name(k):
    for name, val in Keycode.__dict__.items():
        if val == k:
            return name
    return k

# ─── Main loop ─────────────────────────────────────────────────────
while True:
    events = gc.update()
    for ev in events:
        if ev["type"] == "key":
            print(ev["combo"], "→", key_name(ev["value"]))
    time.sleep(0.01)
