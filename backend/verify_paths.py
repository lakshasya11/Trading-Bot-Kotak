
import os
import sys

# Add the current directory to sys.path so we can import from core
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from core.broker_factory import ACTIVE_UCC
from core.database import TODAY_DB_PATH, ALL_DB_PATH

print(f"ACTIVE_UCC: {ACTIVE_UCC}")
print(f"TODAY_DB_PATH: {TODAY_DB_PATH}")
print(f"ALL_DB_PATH: {ALL_DB_PATH}")

if ACTIVE_UCC in TODAY_DB_PATH and ACTIVE_UCC in ALL_DB_PATH:
    print("STATUS: SUCCESS - Paths are user-specific")
else:
    print("STATUS: FAILED - Paths are NOT user-specific")
