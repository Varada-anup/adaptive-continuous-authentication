"""
reset_profiles.py
─────────────────
Run this ONCE to clear any bad calibration profiles saved by the old version.
User accounts and behaviour history are kept — only the calibration data is cleared.

Usage:
    python reset_profiles.py
or to reset a specific user only:
    python reset_profiles.py username
"""

import sqlite3
import sys

DB_NAME = "users.db"

conn = sqlite3.connect(DB_NAME)
cur  = conn.cursor()

# Ensure the table exists (safe to run even if not yet created)
cur.execute('''
    CREATE TABLE IF NOT EXISTS calibration_profiles (
        username  TEXT PRIMARY KEY,
        vectors   TEXT,
        threshold REAL,
        updated   REAL
    )
''')

if len(sys.argv) > 1:
    username = sys.argv[1]
    cur.execute("DELETE FROM calibration_profiles WHERE username=?", (username,))
    cur.execute("DELETE FROM baselines WHERE username=?", (username,))
    print(f"✅  Cleared calibration profile for user: {username}")
else:
    cur.execute("DELETE FROM calibration_profiles")
    cur.execute("DELETE FROM baselines")
    print("✅  Cleared ALL calibration profiles.")
    print("    Users will re-calibrate automatically on next login.")

conn.commit()
conn.close()
print("Done. Start the app normally now.")
