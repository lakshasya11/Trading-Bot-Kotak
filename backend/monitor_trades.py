"""
Real-time Trade Execution Monitor
Checks if bot is taking trades correctly with new Supertrend parameters
"""
import asyncio
import json
from datetime import datetime, timedelta
from sqlalchemy import text
from core.database import today_engine, all_engine

async def monitor_trade_execution():
    print("\n" + "="*70)
    print("📈 REAL-TIME TRADE EXECUTION MONITOR")
    print(f"⏰ Time: {datetime.now()}")
    print("="*70 + "\n")
    
    # 1. Check bot status
    print("🤖 1. BOT STATUS:")
    try:
        import subprocess
        result = subprocess.run(
            ["powershell", "-Command", "curl -s http://localhost:8000/api/status"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout:
            status = json.loads(result.stdout)
            print(f"   ✅ Bot is running")
            print(f"   • Status: {status.get('bot_running', False)}")
            print(f"   • Paused: {status.get('bot_paused', False)}")
            print(f"   • Active Trades: {status.get('active_trades', 0)}")
        else:
            print(f"   ❌ Backend not responding (http://localhost:8000)")
            print(f"   💡 Make sure backend is running: uvicorn main:app --port 8000")
    except Exception as e:
        print(f"   ❌ Backend not running or not accessible")
        print(f"   💡 Start backend with: python -m uvicorn main:app --port 8000")
    
    # 2. Check today's trades
    print("\n📊 2. TODAY'S TRADES (Real-time):")
    try:
        with today_engine.connect() as conn:
            # Get count
            result = conn.execute(text("SELECT COUNT(*) FROM trades"))
            count = result.scalar() or 0
            
            print(f"   ✅ Total trades today: {count}")
            
            if count > 0:
                # Get stats
                result = conn.execute(text("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                        SUM(CASE WHEN pnl <= 0 THEN 1 ELSE 0 END) as losses,
                        SUM(pnl) as gross_pnl,
                        SUM(net_pnl) as net_pnl,
                        AVG(pnl) as avg_pnl,
                        MAX(pnl) as max_pnl,
                        MIN(pnl) as min_pnl
                    FROM trades
                """))
                row = result.fetchone()
                
                if row:
                    print(f"   • Wins: {row[1]} | Losses: {row[2]}")
                    print(f"   • Win Rate: {(row[1]/(row[0] or 1)*100):.1f}%")
                    print(f"   • Gross P&L: ₹{row[3] or 0:.2f}")
                    print(f"   • Net P&L: ₹{row[4] or 0:.2f}")
                    print(f"   • Avg P&L: ₹{row[5] or 0:.2f}")
                    print(f"   • Best Trade: ₹{row[6] or 0:.2f}")
                    print(f"   • Worst Trade: ₹{row[7] or 0:.2f}")
                
                # Get last 3 trades
                print(f"\n   📌 Last 3 Trades:")
                result = conn.execute(text("""
                    SELECT entry_price, exit_price, pnl, net_pnl, entry_time, exit_time
                    FROM trades
                    ORDER BY exit_time DESC
                    LIMIT 3
                """))
                
                trades = result.fetchall()
                for i, trade in enumerate(trades, 1):
                    status_icon = "📈" if trade[2] > 0 else "📉"
                    print(f"   {i}. {status_icon} Entry: ₹{trade[0]:.2f} → Exit: ₹{trade[1]:.2f} | P&L: ₹{trade[2]:.2f}")
            else:
                print(f"   ⚠️ NO TRADES YET")
                print(f"   💡 Start the bot and wait for entry signals")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Check strategy configuration
    print("\n⚙️ 3. STRATEGY CONFIGURATION (Updated):")
    try:
        with open("strategy_params.json", "r") as f:
            params = json.load(f)
        
        print(f"   ✅ Supertrend Period: {params.get('supertrend_period', 'N/A')}")
        print(f"   ✅ Supertrend Multiplier: {params.get('supertrend_multiplier', 'N/A')}")
        print(f"   ✅ ATR Period: {params.get('atr_period', 'N/A')}")
        print(f"   ✅ Trading Mode: {params.get('trading_mode', 'N/A')}")
        print(f"   ✅ Position Size: {params.get('quantity', 'N/A')} lots")
        print(f"   ✅ Risk/Trade: {params.get('risk_per_trade_percent', 'N/A')}%")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 4. Trading readiness
    print("\n" + "="*70)
    print("✅ TRADING READINESS CHECK")
    print("="*70)
    
    checks = {
        "Backend Running": False,
        "Database Connected": False,
        "Strategy Configured": False,
        "Trades Being Taken": False,
    }
    
    # Check backend
    try:
        result = subprocess.run(
            ["powershell", "-Command", "curl -s http://localhost:8000/api/status"],
            capture_output=True,
            timeout=2
        )
        checks["Backend Running"] = result.returncode == 0
    except:
        pass
    
    # Check database
    try:
        with today_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        checks["Database Connected"] = True
    except:
        pass
    
    # Check strategy
    try:
        with open("strategy_params.json") as f:
            params = json.load(f)
        checks["Strategy Configured"] = all([
            params.get('supertrend_period'),
            params.get('supertrend_multiplier'),
        ])
    except:
        pass
    
    # Check trades
    try:
        with today_engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM trades")).scalar() or 0
            checks["Trades Being Taken"] = count > 0
    except:
        pass
    
    for check, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {check}")
    
    print("\n" + "="*70)
    print("🚀 NEXT STEPS")
    print("="*70)
    print("""
    If trades are NOT being taken:
    
    1. CHECK BACKEND IS RUNNING
       python -m uvicorn main:app --port 8000
    
    2. CHECK FRONTEND IS RUNNING
       npm run dev (in frontend folder)
    
    3. START THE BOT
       POST http://localhost:8000/api/start
    
    4. WAIT FOR ENTRY SIGNALS
       Watch the dashboard for entry signals
       
    5. CHECK LOGS
       Look at backend console for "Entry signal found" logs
    
    If still no trades:
    - Check market hours (9:15 AM - 3:30 PM IST on weekdays)
    - Check if watchlist symbols have enough volume
    - Check bot logs for any errors
    """)
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(monitor_trade_execution())
