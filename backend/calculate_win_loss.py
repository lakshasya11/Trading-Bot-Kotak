
import sqlite3
import os
import glob
import json

def get_detailed_stats(path):
    try:
        if not os.path.exists(path): return None
        conn = sqlite3.connect(path)
        c = conn.cursor()
        
        # Check if table exists
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trades'")
        if not c.fetchone():
            conn.close()
            return None
            
        c.execute("SELECT COUNT(*) FROM trades")
        total = c.fetchone()[0]
        
        if total == 0:
            conn.close()
            return {"total": 0, "wins": 0, "losses": 0, "breakeven": 0}
            
        c.execute("SELECT COUNT(*) FROM trades WHERE pnl > 0")
        wins = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM trades WHERE pnl < 0")
        losses = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM trades WHERE pnl = 0")
        breakeven = c.fetchone()[0]
        
        c.execute("SELECT SUM(pnl), SUM(net_pnl) FROM trades")
        pnl_sum = c.fetchone()
        
        conn.close()
        return {
            "total": total,
            "wins": wins,
            "losses": losses,
            "breakeven": breakeven,
            "gross_pnl": pnl_sum[0] or 0.0,
            "net_pnl": pnl_sum[1] or 0.0
        }
    except Exception as e:
        print(f"Error processing {path}: {e}")
        return None

BASE = r"e:\Trading_Bot_kotak\Kotak_Breakout_logic\backend"
db_files = ["trading_data_V19Q3_all.db", "trading_data_all.db", "trading_data_V1X8N_all.db"]

print(f"{'Database':<30} | {'Total':<6} | {'Wins':<6} | {'Losses':<6} | {'BE':<5} | {'Win %':<8}")
print("-" * 80)

final_results = {}
for db_name in db_files:
    path = os.path.join(BASE, db_name)
    stats = get_detailed_stats(path)
    if stats:
        win_pc = (stats['wins'] / stats['total'] * 100) if stats['total'] > 0 else 0
        final_results[db_name] = stats
        print(f"DB: {db_name}")
        print(f"  Total: {stats['total']}")
        print(f"  Wins: {stats['wins']}")
        print(f"  Losses: {stats['losses']}")
        print(f"  BE: {stats['breakeven']}")
        print(f"  Win%: {win_pc:.1f}%")

with open(os.path.join(BASE, "win_loss_summary.json"), "w") as f:
    json.dump(final_results, f, indent=2)
