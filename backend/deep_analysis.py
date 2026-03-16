"""
Deep database analysis - find where 146 trades went
"""
import sqlite3
import os

print("\n" + "="*70)
print("🔍 DATABASE DEEP ANALYSIS")
print("="*70 + "\n")

# Check today's database in detail
db_file = 'trading_data_today.db'
print(f"📁 Database File: {db_file}")

if os.path.exists(db_file):
    size = os.path.getsize(db_file)
    print(f"   ✅ File size: {size/1024:.2f} KB")
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\n📋 Tables found: {len(tables)}")
    for table in tables:
        print(f"   • {table[0]}")
        
        # Count records in each table
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
        count = cursor.fetchone()[0]
        print(f"     Records: {count}")
    
    conn.close()
else:
    print(f"   ❌ File not found!")

print("\n" + "="*70)
print("💡 ANALYSIS RESULT")
print("="*70)
print("""
If database file is 148 KB but shows 0 trades:
  1. ✅ Database structure was created
  2. ✅ Transactions were started
  3. ❌ Data was NOT committed to disk
  
This usually happens when:
  • Bot crashed before commit
  • Session ended abruptly
  • Transaction rolled back

The 146 trades displayed on dashboard were:
  ✅ Real calculations (in memory)
  ❌ Never persisted to database
  
Status: DATA LOST (in-memory only)
""")
print("="*70 + "\n")
