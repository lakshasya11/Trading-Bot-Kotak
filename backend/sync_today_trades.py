#!/usr/bin/env python3
"""
Sync Today's Trades to TODAY Database
====================================
Copies today's 146 trades from all_engine to today_engine database.
"""

import sqlite3
from datetime import date

today_str = date.today().isoformat()

print("🔄 SYNCING TODAY'S TRADES FROM ALL-TIME DB TO TODAY DB")
print("="*60)

# Connect to both databases
today_conn = sqlite3.connect("trading_data_today.db")
all_conn = sqlite3.connect("trading_data_all.db")

today_cursor = today_conn.cursor()
all_cursor = all_conn.cursor()

# Get all trades from today in the all-time database
all_cursor.execute("""
    SELECT * FROM trades 
    WHERE DATE(entry_time) = ?
    ORDER BY id
""", (today_str,))

trades_from_all = all_cursor.fetchall()
print(f"\n📊 Found {len(trades_from_all)} trades in all_engine for {today_str}")

if len(trades_from_all) == 0:
    print("❌ No trades found to sync")
    today_conn.close()
    all_conn.close()
    exit(1)

# Get column names from all_engine
all_cursor.execute("PRAGMA table_info(trades)")
columns_info = all_cursor.fetchall()
column_names = [col[1] for col in columns_info]

print(f"✅ Columns: {', '.join(column_names[:10])}... ({len(column_names)} total)")

# Clear today's database first
print("\n🗑️  Clearing today's database...")
today_cursor.execute("DELETE FROM trades")
today_conn.commit()

# Insert trades into today's database
print(f"📥 Inserting {len(trades_from_all)} trades into today_engine...")

placeholders = ", ".join(["?"] * len(column_names))
insert_sql = f"INSERT INTO trades ({', '.join(column_names)}) VALUES ({placeholders})"

try:
    for i, trade in enumerate(trades_from_all):
        today_cursor.execute(insert_sql, trade)
        if (i + 1) % 50 == 0:
            print(f"   Inserted {i + 1}/{len(trades_from_all)} trades...")
    
    today_conn.commit()
    print(f"✅ All {len(trades_from_all)} trades synced successfully!")
    
    # Verify
    today_cursor.execute(f"SELECT COUNT(*) FROM trades WHERE DATE(entry_time) = ?", (today_str,))
    synced_count = today_cursor.fetchone()[0]
    print(f"\n📊 Verification: {synced_count} trades now in today_engine")
    
    if synced_count == len(trades_from_all):
        print("✅ SYNC COMPLETE - All trades persisted!")
    else:
        print(f"⚠️  Mismatch: Expected {len(trades_from_all)}, got {synced_count}")
        
except Exception as e:
    print(f"❌ Error during sync: {e}")
    today_conn.rollback()

today_conn.close()
all_conn.close()

print("\n" + "="*60)
