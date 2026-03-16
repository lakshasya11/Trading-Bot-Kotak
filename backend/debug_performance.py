"""
Debug script to check Daily Performance data
Run this to diagnose why performance is showing 0
"""
import asyncio
import json
from sqlalchemy import create_engine, text
from core.database import today_engine, all_engine

async def check_performance():
    print("\n" + "="*60)
    print("🔍 DAILY PERFORMANCE DEBUG")
    print("="*60 + "\n")
    
    # Check today's database
    print("📊 1. Checking TODAY's trades database:")
    try:
        with today_engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    COUNT(*) as total_trades,
                    SUM(pnl) as gross_pnl,
                    SUM(charges) as total_charges,
                    SUM(net_pnl) as net_pnl,
                    SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                    SUM(CASE WHEN pnl <= 0 THEN 1 ELSE 0 END) as losses
                FROM trades
            """))
            
            row = result.fetchone()
            if row and row[0] and row[0] > 0:
                print(f"   ✅ Total Trades: {row[0]}")
                print(f"   ✅ Gross P&L: ₹{row[1] or 0:.2f}")
                print(f"   ✅ Total Charges: ₹{row[2] or 0:.2f}")
                print(f"   ✅ Net P&L: ₹{row[3] or 0:.2f}")
                print(f"   ✅ Wins: {row[4] or 0} | Losses: {row[5] or 0}")
            else:
                print("   ❌ NO TRADES IN TODAY'S DATABASE")
    except Exception as e:
        print(f"   ❌ Error checking today's database: {e}")
    
    # Check all-time database
    print("\n📊 2. Checking ALL-TIME trades database:")
    try:
        with all_engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    COUNT(*) as total_trades,
                    SUM(pnl) as gross_pnl,
                    SUM(charges) as total_charges,
                    SUM(net_pnl) as net_pnl
                FROM trades
            """))
            
            row = result.fetchone()
            if row and row[0] and row[0] > 0:
                print(f"   ✅ Total Trades (All-Time): {row[0]}")
                print(f"   ✅ Total Gross P&L: ₹{row[1] or 0:.2f}")
                print(f"   ✅ Total Charges: ₹{row[2] or 0:.2f}")
                print(f"   ✅ Total Net P&L: ₹{row[3] or 0:.2f}")
            else:
                print("   ❌ NO TRADES IN ALL-TIME DATABASE")
    except Exception as e:
        print(f"   ❌ Error checking all-time database: {e}")
    
    # Check recent trades
    print("\n📊 3. Most Recent Trades (Last 5):")
    try:
        with today_engine.connect() as conn:
            result = conn.execute(text("""
                SELECT trade_id, entry_price, exit_price, pnl, charges, net_pnl, entry_time
                FROM trades
                ORDER BY entry_time DESC
                LIMIT 5
            """))
            
            trades = result.fetchall()
            if trades:
                for trade in trades:
                    print(f"   • Trade ID: {trade[0]}")
                    print(f"     Entry: ₹{trade[1]:.2f} → Exit: ₹{trade[2]:.2f}")
                    print(f"     P&L: ₹{trade[3]:.2f} | Charges: ₹{trade[4]:.2f} | Net: ₹{trade[5]:.2f}")
                    print()
            else:
                print("   ❌ NO RECENT TRADES FOUND")
    except Exception as e:
        print(f"   ❌ Error fetching recent trades: {e}")
    
    print("="*60)
    print("🔧 TROUBLESHOOTING GUIDE:")
    print("="*60)
    print("""
If Daily Performance shows 0:

1. ✅ Have you STARTED the bot? (/api/start)
   - Check the bot status endpoint: /api/status
   - Make sure bot_running: true
   
2. ✅ Have TRADES been executed?
   - Start bot and wait for entry signal
   - Check trade history: /api/trade_history
   
3. ✅ Is the database saving trades correctly?
   - This debug script checks database
   - Run: python backend/debug_performance.py
   
4. ✅ Is the WebSocket connection active?
   - Open browser console (F12)
   - Check for connection errors
   - Look for "performance" messages

5. ✅ Frontend receiving data?
   - Open browser console (F12)
   - Type: console.log(useStore.getState().dailyPerformance)
   - Should show P&L values
    """)
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(check_performance())
