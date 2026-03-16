
import sqlite3
import os

def get_last_trade(path):
    if not os.path.exists(path): return None
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("SELECT symbol, entry_time, exit_time, pnl FROM trades ORDER BY id DESC LIMIT 1")
    t = c.fetchone()
    conn.close()
    return t

BASE = r"e:\Trading_Bot_kotak\Kotak_Breakout_logic\backend"
last_today = get_last_trade(os.path.join(BASE, 'trading_data_today.db'))
last_all = get_last_trade(os.path.join(BASE, 'trading_data_all.db'))

print(f"LAST_TODAY: {last_today}")
print(f"LAST_ALL: {last_all}")
if last_today == last_all:
    print("SYNC_STATUS: OK")
else:
    print("SYNC_STATUS: MISMATCH")
