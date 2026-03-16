"""
Diagnose: Trades not being stored in database
Check where 146 trades are and why they're not showing in DB
"""
import asyncio
import json
from sqlalchemy import text, inspect
from core.database import today_engine, all_engine
import sqlite3

async def diagnose_missing_trades():
    print("\n" + "="*70)
    print("🔍 DIAGNOSE: 146 TRADES NOT STORING")
    print("="*70 + "\n")
    
    # 1. Check database file size
    print("📁 1. DATABASE FILES:")
    import os
    try:
        today_db = "trading_data_today.db"
        all_db = "trading_data_all.db"
        
        if os.path.exists(today_db):
            size_mb = os.path.getsize(today_db) / (1024*1024)
            print(f"   ✅ {today_db}: {size_mb:.2f} MB")
        else:
            print(f"   ❌ {today_db}: NOT FOUND")
            
        if os.path.exists(all_db):
            size_mb = os.path.getsize(all_db) / (1024*1024)
            print(f"   ✅ {all_db}: {size_mb:.2f} MB")
        else:
            print(f"   ❌ {all_db}: NOT FOUND")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Check table schema
    print("\n📋 2. TABLE SCHEMA:")
    try:
        with today_engine.connect() as conn:
            inspector = inspect(today_engine)
            tables = inspector.get_table_names()
            print(f"   ✅ Tables in today's DB: {tables}")
            
            if 'trades' in tables:
                columns = inspector.get_columns('trades')
                print(f"   ✅ Trade columns: {[c['name'] for c in columns]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Count trades in different ways
    print("\n📊 3. TRADE COUNT (Different Methods):")
    try:
        with today_engine.connect() as conn:
            # Method 1: Simple count
            result = conn.execute(text("SELECT COUNT(*) FROM trades"))
            count1 = result.scalar()
            print(f"   Method 1 - SELECT COUNT(*): {count1}")
            
            # Method 2: Check table size
            result = conn.execute(text("SELECT COUNT(*) as cnt FROM sqlite_master WHERE type='table' AND name='trades'"))
            table_exists = result.scalar()
            print(f"   Method 2 - Table exists: {table_exists}")
            
            # Method 3: Get actual rows
            result = conn.execute(text("SELECT * FROM trades LIMIT 1"))
            rows = result.fetchall()
            print(f"   Method 3 - Sample rows: {len(rows)}")
            
            # Method 4: All rows
            result = conn.execute(text("SELECT * FROM trades"))
            all_rows = result.fetchall()
            print(f"   Method 4 - Total rows: {len(all_rows)}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Check if trades are in memory but not persisted
    print("\n💾 4. PERSISTENCE CHECK:")
    try:
        # Direct SQLite check
        conn = sqlite3.connect("trading_data_today.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM trades")
        db_count = cursor.fetchone()[0]
        print(f"   ✅ Direct SQLite count: {db_count} trades")
        
        if db_count == 146:
            print(f"   ✅ All 146 trades ARE stored in database!")
        elif db_count > 0:
            print(f"   ⚠️ Only {db_count} trades stored (missing {146 - db_count})")
        else:
            print(f"   ❌ No trades in database (all 146 in memory only)")
        
        conn.close()
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 5. Check trade data
    print("\n📈 5. TRADE DATA:")
    try:
        conn = sqlite3.connect("trading_data_today.db")
        cursor = conn.cursor()
        
        # Get summary
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN pnl <= 0 THEN 1 ELSE 0 END) as losses,
                SUM(pnl) as total_pnl,
                SUM(net_pnl) as net_pnl
            FROM trades
        """)
        
        result = cursor.fetchone()
        if result and result[0]:
            print(f"   ✅ Stored Trades: {result[0]}")
            print(f"   ✅ Wins: {result[1] or 0} | Losses: {result[2] or 0}")
            print(f"   ✅ Total P&L: ₹{result[3] or 0:.2f}")
            print(f"   ✅ Net P&L: ₹{result[4] or 0:.2f}")
        else:
            print(f"   ❌ No trades found")
        
        conn.close()
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 6. Check if market hours issue
    print("\n⏰ 7. MARKET STATUS CHECK:")
    from datetime import datetime
    now = datetime.now()
    print(f"   Current Time: {now.strftime('%H:%M:%S')} ({now.strftime('%A')})")
    
    # IST market hours: 9:15 AM - 3:30 PM
    hour = now.hour
    minute = now.minute
    
    market_open_time = (9, 15)
    market_close_time = (15, 30)
    
    if now.weekday() < 5:  # Monday to Friday
        print(f"   ✅ Weekday (trading day)")
        
        current_minutes = hour * 60 + minute
        open_minutes = market_open_time[0] * 60 + market_open_time[1]
        close_minutes = market_close_time[0] * 60 + market_close_time[1]
        
        if open_minutes <= current_minutes <= close_minutes:
            print(f"   ✅ Within market hours (9:15 AM - 3:30 PM IST)")
        else:
            print(f"   ⚠️ Outside market hours (market opens at 9:15 AM IST)")
    else:
        print(f"   ❌ Weekend (no trading)")
    
    print("\n" + "="*70)
    print("✅ SOLUTION")
    print("="*70)
    print("""
    If 146 trades are NOT in database:
    
    1. CHECK IF TRADES ARE IN MEMORY
       - Stop the bot (POST /api/stop)
       - Run this script again
       - Database should be updated
    
    2. CHECK DATABASE PERSISTENCE
       - Ensure bot is committing trades to DB
       - Look for "Trade saved to database" logs
    
    3. CHECK FOR ERRORS
       - Look at backend console for errors
       - Check if bot is in "Paper Trading" mode
    
    If 146 trades ARE in database:
    - Run: python monitor_trades.py
    - Daily Performance will show P&L
    """)
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(diagnose_missing_trades())
