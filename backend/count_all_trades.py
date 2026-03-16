
import sqlite3
import os
import glob

def get_counts(path):
    try:
        if not os.path.exists(path): return "Missing"
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trades'")
        if not c.fetchone():
            conn.close()
            return "No trades table"
        c.execute("SELECT COUNT(*) FROM trades")
        count = c.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        return f"Error: {e}"

BASE = r"e:\Trading_Bot_kotak\Kotak_Breakout_logic\backend"
db_files = glob.glob(os.path.join(BASE, "*.db"))

print("Trade Counts per Database:")
print("-" * 30)
for db in sorted(db_files):
    name = os.path.basename(db)
    count = get_counts(db)
    print(f"{name}: {count}")
