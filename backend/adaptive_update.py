"""
adaptive_update.py
──────────────────
Slow EMA that refines each user's feature baseline across sessions.
Only called from decision_engine when a reading is clearly genuine,
so the baseline never drifts toward an intruder's pattern.

Changes vs original:
  • ALPHA lowered to 0.02 (was 0.03) — even slower drift
  • MIN_SCORE raised to 0.72 (was 0.65) — only update on confident genuine
  • std floor tightened to prevent over-wide bands hiding real anomalies
"""

import sqlite3
import json
import time

DB_NAME   = "users.db"
ALPHA     = 0.02     # 2 % new data, 98 % history
MIN_SCORE = 0.72     # only update when session looks clearly healthy


def _ensure_table():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS baselines (
            username   TEXT PRIMARY KEY,
            mean_json  TEXT,
            std_json   TEXT,
            updated_at REAL
        )
    ''')
    conn.commit()
    conn.close()


_ensure_table()


def load_baseline(username: str):
    """Return (mean_dict, std_dict) or (None, None) if not stored yet."""
    conn = sqlite3.connect(DB_NAME)
    cur  = conn.cursor()
    cur.execute(
        "SELECT mean_json, std_json FROM baselines WHERE username=?",
        (username,)
    )
    row = cur.fetchone()
    conn.close()
    if row is None:
        return None, None
    try:
        return json.loads(row[0]), json.loads(row[1])
    except Exception:
        return None, None


def save_baseline(username: str, mean: dict, std: dict):
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''
        INSERT INTO baselines (username, mean_json, std_json, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
            mean_json  = excluded.mean_json,
            std_json   = excluded.std_json,
            updated_at = excluded.updated_at
    ''', (username, json.dumps(mean), json.dumps(std), time.time()))
    conn.commit()
    conn.close()


def adaptive_update(username: str, new_features: dict, score: float):
    """
    Update the long-term baseline with a tiny EMA step.
    Only runs when score is high enough to trust the sample.
    """
    if score < MIN_SCORE:
        return   # anomalous reading — don't corrupt the baseline

    mean, std = load_baseline(username)

    if mean is None:
        # First genuine reading after calibration — seed the baseline
        init_std = {k: max(abs(v) * 0.20, 1e-3) for k, v in new_features.items()}
        save_baseline(username, dict(new_features), init_std)
        return

    new_mean = {}
    new_std  = {}
    for k in mean:
        v = new_features.get(k, mean[k])

        m = (1 - ALPHA) * mean[k] + ALPHA * v
        residual = abs(v - m)
        s = (1 - ALPHA) * std.get(k, residual + 1e-4) + ALPHA * residual
        # floor: at least 5 % of mean or 1 ms
        s = max(s, abs(m) * 0.05, 1e-3)

        new_mean[k] = m
        new_std[k]  = s

    save_baseline(username, new_mean, new_std)
    print(f"[{username}] Baseline EMA updated (score={score:.3f})")
