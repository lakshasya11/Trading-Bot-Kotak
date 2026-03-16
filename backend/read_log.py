
import os

log_path = r"e:\Trading_Bot_kotak\Kotak_Breakout_logic\backend\bot_debug.log"
if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
        for line in lines[-100:]:
            print(line.strip())
