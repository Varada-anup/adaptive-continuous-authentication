"""
feature_extractor.py
────────────────────
Extracts 9 behavioural biometric features from raw keystroke + mouse data.

Robust to short sequences, missing keys, and zero dt.
"""

import numpy as np


def _safe_stats(arr):
    """Return (mean, std) or (0.0, 0.0) for an empty / all-zero array."""
    if not arr:
        return 0.0, 0.0
    a = np.array(arr, dtype=float)
    return float(np.mean(a)), float(np.std(a) if len(a) > 1 else 0.0)


def extract_features(raw_data: dict):
    """
    Returns a feature dict or None if there isn't enough data.

    Required keys in raw_data:
        keys  – list of {down: ms, up: ms}
        mouse – list of {x, y, time: ms}

    Features returned:
        key_mean / key_std         – inter-key-down intervals
        hold_mean / hold_std       – key hold durations
        digraph_mean / digraph_std – 2-key flight times
        trigraph_mean / trigraph_std – 3-key flight times
        mouse_mean                 – mean mouse pixel-speed (px / ms)
    """
    if not isinstance(raw_data, dict):
        return None

    keys  = raw_data.get("keys",  [])
    mouse = raw_data.get("mouse", [])

    # Need at least 5 key events for meaningful stats
    if len(keys) < 5:
        return None

    hold_times = []
    intervals  = []
    digraphs   = []
    trigraphs  = []

    for i, k in enumerate(keys):
        try:
            d    = float(k["down"])
            u    = float(k["up"])
            hold = u - d
            if hold >= 0:
                hold_times.append(hold)

            if i > 0:
                prev_d = float(keys[i - 1]["down"])
                interval = d - prev_d
                if interval >= 0:
                    intervals.append(interval)
                    digraphs.append(interval)

            if i > 1:
                prev2_d = float(keys[i - 2]["down"])
                t = d - prev2_d
                if t >= 0:
                    trigraphs.append(t)

        except (KeyError, TypeError, ValueError):
            continue

    # Mouse speeds
    mouse_speeds = []
    for i in range(1, len(mouse)):
        try:
            dx = float(mouse[i]["x"])  - float(mouse[i - 1]["x"])
            dy = float(mouse[i]["y"])  - float(mouse[i - 1]["y"])
            dt = float(mouse[i]["time"]) - float(mouse[i - 1]["time"])
            if dt > 0:
                speed = (dx**2 + dy**2) ** 0.5 / dt
                mouse_speeds.append(speed)
        except (KeyError, TypeError, ValueError):
            continue

    # Require at least a few valid intervals
    if len(intervals) < 3:
        return None

    key_mean,      key_std      = _safe_stats(intervals)
    hold_mean,     hold_std     = _safe_stats(hold_times)
    digraph_mean,  digraph_std  = _safe_stats(digraphs)
    trigraph_mean, trigraph_std = _safe_stats(trigraphs)
    mouse_mean,    _            = _safe_stats(mouse_speeds)

    return {
        "key_mean":      key_mean,
        "key_std":       key_std,
        "hold_mean":     hold_mean,
        "hold_std":      hold_std,
        "digraph_mean":  digraph_mean,
        "digraph_std":   digraph_std,
        "trigraph_mean": trigraph_mean,
        "trigraph_std":  trigraph_std,
        "mouse_mean":    mouse_mean,
    }
