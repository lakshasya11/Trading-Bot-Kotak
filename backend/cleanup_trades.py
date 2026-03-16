import sqlite3
from datetime import date

# Connect to the database
conn = sqlite3.connect('trading_data_V1X8N_today.db')
cursor = conn.cursor()

# Find and delete test trades
test_trades = [
    ('TEST123CE', 'TEST_VERIFY'),
    ('NIFTY2631723150CE', 'TEST'),
]

print("Removing test trades...")
for symbol, trigger in test_trades:
    cursor.execute("""
        DELETE FROM trades 
        WHERE symbol = ? AND trigger_reason = ?
    """, (symbol, trigger))
    deleted = cursor.rowcount
    print(f"  ✅ Deleted {deleted} trades: {symbol} ({trigger})")

conn.commit()

# Verify count
cursor.execute('SELECT COUNT(*) FROM trades')
count = cursor.fetchone()[0]
print(f"\n✅ Database cleaned!")
print(f"📊 Remaining trades: {count}")

# Show remaining trades
cursor.execute("""
    SELECT entry_time, symbol, trigger_reason, net_pnl 
    FROM trades 
    ORDER BY entry_time DESC
""")
print("\nRemaining trades:")
for row in cursor.fetchall():
    print(f"  {row[0]} | {row[1]} | {row[2]} | ₹{row[3]}")

conn.close()
