import time


class GripChord:
    def __init__(self, pins=None, keymap=None, stable_ms=0.03):
        self.pins = pins or []
        self.keymap = keymap

        # timing
        self.stable_ms = stable_ms

        # state
        self.last_raw_combo = ()
        self.stable_combo = ()
        self.emitted_combo = None
        self.combo_start = 0.0
        self.rearm_delay = 0.08   # seconds (tune this)
        self.rearm_at = 0.0

        # layer state
        self.layer = 1

    def _read_combo(self):
        return tuple(
            i for i, p in enumerate(self.pins)
            if not p.value
        )

    def _lookup_key(self, combo):
        if not self.keymap:
            return None

        layer_map = self.keymap.layer_maps.get(self.layer)
        if not layer_map:
            return None

        return layer_map.get(combo)

    def update(self):
        now = time.monotonic()
        events = []

        combo = self._read_combo()

        # Raw change → reset stabilization timer
        if combo != self.last_raw_combo:
            self.combo_start = now
            self.last_raw_combo = combo
            return []

        # Stable combo candidate
        if combo and combo != self.stable_combo:
            if (now - self.combo_start) >= self.stable_ms:
                if len(combo) > len(self.stable_combo):
                    # prevent immediate re-fire
                    if now >= self.rearm_at:
                        self.stable_combo = combo
                        self.emitted_combo = combo
                        self.rearm_at = now + self.rearm_delay
                        events.append({
                            "type": "combo_down",
                            "combo": combo,
                        })
                else:
                    self.stable_combo = combo

        # Full release
        if not combo and self.emitted_combo:
            key = self._lookup_key(self.emitted_combo)

            if key is not None and self.layer in (1, 2):
                events.append({
                    "type": "key",
                    "layer": self.layer,
                    "value": key,
                    "combo": self.emitted_combo,
                })

            self.stable_combo = ()
            self.emitted_combo = None
        return events
