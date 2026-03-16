
import sqlite3
import os

def check_triggers(path):
    if not os.path.exists(path): return
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("SELECT trigger_reason, COUNT(*) FROM trades GROUP BY trigger_reason")
    triggers = c.fetchall()
    print("\nTRIGGERS FOR TODAY:")
    for t in triggers:
        print(f"  {t[0]}: {t[1]}")
    
    c.execute("SELECT exit_reason, COUNT(*) FROM trades GROUP BY exit_reason")
    exits = c.fetchall()
    print("\nEXITS FOR TODAY:")
    for e in exits:
        print(f"  {e[0]}: {e[1]}")
    
    c.execute("SELECT quantity, COUNT(*) FROM trades GROUP BY quantity")
    qtys = c.fetchall()
    print("\nQUANTITIES FOR TODAY:")
    for q in qtys:
        print(f"  Qty {q[0]}: {q[1]} trades")
        
    conn.close()

check_triggers(r"e:\Trading_Bot_kotak\Kotak_Breakout_logic\backend\trading_data_today.db")
