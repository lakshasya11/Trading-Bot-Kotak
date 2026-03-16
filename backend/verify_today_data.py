"""
Comprehensive Data Verification Script
Verify if today's 146 trades and ₹87,089.80 profit are correctly stored in database
"""
import asyncio
import json
import sqlite3
from datetime import datetime
from sqlalchemy import text
from core.database import today_engine, all_engine

async def verify_today_data():
    print("\n" + "="*80)
    print("✅ VERIFY TODAY'S TRADING DATA - MARCH 13, 2026")
    print("="*80 + "\n")
    
    # Expected values from report
    expected = {
        "total_trades": 146,
        "wins": 101,
        "losses": 45,
        "gross_pnl": 125008.00,
        "charges": 37918.20,
        "net_pnl": 87089.80
    }
    
    print("📋 EXPECTED TODAY'S REPORT:")
    print(f"   • Total Trades: {expected['total_trades']}")
    print(f"   • Wins: {expected['wins']} | Losses: {expected['losses']}")
    print(f"   • Gross P&L: ₹{expected['gross_pnl']:.2f}")
    print(f"   • Charges: ₹{expected['charges']:.2f}")
    print(f"   • Net P&L: ₹{expected['net_pnl']:.2f}\n")
    
    # Check direct database
    print("="*80)
    print("🔍 CHECKING DATABASE...")
    print("="*80 + "\n")
    
    try:
        # Direct SQLite connection
        conn = sqlite3.connect("trading_data_today.db")
        cursor = conn.cursor()
        
        # Get actual values from database
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN pnl <= 0 THEN 1 ELSE 0 END) as losses,
                SUM(pnl) as gross_pnl,
                SUM(charges) as total_charges,
                SUM(net_pnl) as net_pnl
            FROM trades
        """)
        
        result = cursor.fetchone()
        actual = {
            "total_trades": result[0] or 0,
            "wins": result[1] or 0,
            "losses": result[2] or 0,
            "gross_pnl": round(result[3] or 0, 2),
            "charges": round(result[4] or 0, 2),
            "net_pnl": round(result[5] or 0, 2)
        }
        
        print("✅ ACTUAL DATA IN DATABASE:")
        print(f"   • Total Trades: {actual['total_trades']}")
        print(f"   • Wins: {actual['wins']} | Losses: {actual['losses']}")
        print(f"   • Gross P&L: ₹{actual['gross_pnl']:.2f}")
        print(f"   • Charges: ₹{actual['charges']:.2f}")
        print(f"   • Net P&L: ₹{actual['net_pnl']:.2f}\n")
        
        # Verify calculations
        print("="*80)
        print("📊 DATA VERIFICATION")
        print("="*80 + "\n")
        
        verification_results = []
        
        # Check 1: Total Trades
        check1 = actual['total_trades'] == expected['total_trades']
        status1 = "✅ MATCH" if check1 else f"❌ MISMATCH (Expected {expected['total_trades']}, Got {actual['total_trades']})"
        print(f"1. Total Trades: {status1}")
        verification_results.append(check1)
        
        # Check 2: Wins
        check2 = actual['wins'] == expected['wins']
        status2 = "✅ MATCH" if check2 else f"❌ MISMATCH (Expected {expected['wins']}, Got {actual['wins']})"
        print(f"2. Winning Trades: {status2}")
        verification_results.append(check2)
        
        # Check 3: Losses
        check3 = actual['losses'] == expected['losses']
        status3 = "✅ MATCH" if check3 else f"❌ MISMATCH (Expected {expected['losses']}, Got {actual['losses']})"
        print(f"3. Losing Trades: {status3}")
        verification_results.append(check3)
        
        # Check 4: Gross P&L
        check4 = abs(actual['gross_pnl'] - expected['gross_pnl']) < 1
        status4 = "✅ MATCH" if check4 else f"❌ MISMATCH (Expected ₹{expected['gross_pnl']:.2f}, Got ₹{actual['gross_pnl']:.2f})"
        print(f"4. Gross P&L: {status4}")
        verification_results.append(check4)
        
        # Check 5: Charges
        check5 = abs(actual['charges'] - expected['charges']) < 1
        status5 = "✅ MATCH" if check5 else f"❌ MISMATCH (Expected ₹{expected['charges']:.2f}, Got ₹{actual['charges']:.2f})"
        print(f"5. Total Charges: {status5}")
        verification_results.append(check5)
        
        # Check 6: Net P&L
        check6 = abs(actual['net_pnl'] - expected['net_pnl']) < 1
        status6 = "✅ MATCH" if check6 else f"❌ MISMATCH (Expected ₹{expected['net_pnl']:.2f}, Got ₹{actual['net_pnl']:.2f})"
        print(f"6. Net P&L: {status6}")
        verification_results.append(check6)
        
        # Check 7: Win Rate
        if actual['total_trades'] > 0:
            expected_winrate = (expected['wins'] / expected['total_trades']) * 100
            actual_winrate = (actual['wins'] / actual['total_trades']) * 100
            check7 = abs(expected_winrate - actual_winrate) < 0.1
            status7 = "✅ MATCH" if check7 else f"❌ MISMATCH (Expected {expected_winrate:.1f}%, Got {actual_winrate:.1f}%)"
            print(f"7. Win Rate: {status7}")
            verification_results.append(check7)
        
        # Summary
        print("\n" + "="*80)
        if all(verification_results):
            print("✅ ✅ ✅ ALL DATA VERIFIED - DATABASE IS CORRECT! ✅ ✅ ✅")
        else:
            print("❌ SOME DATA MISMATCHES - DATABASE NEEDS FIX")
        print("="*80 + "\n")
        
        # Sample trades to confirm data quality
        print("📈 SAMPLE OF LAST 5 TRADES (to verify data quality):")
        cursor.execute("""
            SELECT 
                symbol, entry_price, exit_price, quantity, pnl, charges, net_pnl, 
                entry_time, exit_time
            FROM trades
            ORDER BY exit_time DESC
            LIMIT 5
        """)
        
        trades = cursor.fetchall()
        for i, trade in enumerate(trades, 1):
            pnl_icon = "📈" if trade[4] > 0 else "📉"
            print(f"   {i}. {pnl_icon} {trade[0]} | Entry: ₹{trade[1]:.2f} → Exit: ₹{trade[2]:.2f}")
            print(f"      Qty: {trade[3]} | P&L: ₹{trade[4]:.2f} | Charges: ₹{trade[5]:.2f} | Net: ₹{trade[6]:.2f}")
        
        conn.close()
        
        # Final Report
        print("\n" + "="*80)
        print("📝 FINAL VERIFICATION REPORT")
        print("="*80)
        
        if all(verification_results):
            print("""
✅ TODAY'S DATA IS CORRECTLY STORED IN DATABASE!

Your trading report is ACCURATE:
  ✅ 146 trades recorded
  ✅ 101 wins, 45 losses (69.2% win rate)
  ✅ Gross P&L: ₹125,008.00
  ✅ Charges: ₹37,918.20
  ✅ Net P&L: ₹87,089.80

All calculations verified and correct!
Database integrity: PERFECT
System status: PRODUCTION READY ✅
            """)
        else:
            print("""
❌ DATA MISMATCH DETECTED!

Some values in the report don't match the database.
This may indicate:
  1. Data was not fully persisted
  2. Database corruption
  3. Calculation error

ACTION: Review the mismatches above and rerun after bot stop.
            """)
        
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("This usually means:")
        print("  1. Database file is corrupted")
        print("  2. Database is locked by another process")
        print("  3. Trades table doesn't exist")

if __name__ == "__main__":
    asyncio.run(verify_today_data())
