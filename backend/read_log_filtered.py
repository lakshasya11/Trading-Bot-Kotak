
import os

log_path = r"e:\Trading_Bot_kotak\Kotak_Breakout_logic\backend\bot_debug.log"
if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
        found = 0
        for line in reversed(lines):
            if any(x in line for x in ["Entry", "Exit", "Qty", "Lots", "Signal"]):
                print(line.strip())
                found += 1
                if found > 50:
                    break
