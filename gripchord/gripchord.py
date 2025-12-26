class GripChord:
    def __init__(self, pins=None, keymap=None, **timing):
        self.pins = pins or []
        self.keymap = keymap

    def update(self):
        if not self.pins:
            return []

        combo = tuple(
            i for i, p in enumerate(self.pins)
            if not p.value
        )

        if combo:
            return [{"type": "combo", "combo": combo}]
        return []
