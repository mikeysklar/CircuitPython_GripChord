import time
import board
import digitalio

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


# ─── Main loop ─────────────────────────────────────────────────────
while True:
    events = gc.update()
    for ev in events:
        print(ev)
    time.sleep(0.01)
