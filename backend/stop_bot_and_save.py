"""
Stop Bot and Save All Trades to Database
"""
import requests
import json
import time
import sys

def stop_bot():
    print("\n" + "="*70)
    print("🛑 STOPPING BOT AND SAVING TRADES TO DATABASE")
    print("="*70 + "\n")
    
    backend_url = "http://localhost:8000"
    
    # Method 1: Try POST /api/stop
    print("📌 Attempt 1: POST /api/stop")
    try:
        response = requests.post(f"{backend_url}/api/stop", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        if response.status_code == 200:
            print("   ✅ SUCCESS - Bot stopped!")
            return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Method 2: Try different endpoints
    print("\n📌 Attempt 2: Checking available endpoints")
    endpoints = [
        ("/api/stop", "POST"),
        ("/api/stop", "GET"),
        ("/stop", "POST"),
        ("/api/status", "GET"),
    ]
    
    for endpoint, method in endpoints:
        try:
            if method == "POST":
                response = requests.post(f"{backend_url}{endpoint}", timeout=2)
            else:
                response = requests.get(f"{backend_url}{endpoint}", timeout=2)
            
            print(f"   {method} {endpoint}: {response.status_code}")
            if response.status_code == 200:
                print(f"      Response: {response.json()}")
        except:
            pass
    
    # Method 3: Check backend status
    print("\n📌 Attempting to get bot status:")
    try:
        response = requests.get(f"{backend_url}/api/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print(f"   ✅ Backend is RUNNING")
            print(f"   Bot running: {status.get('bot_running', False)}")
            print(f"   Bot paused: {status.get('bot_paused', False)}")
        else:
            print(f"   ❌ Status code: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Backend not responding: {e}")
        print(f"   💡 Make sure backend is running:")
        print(f"      python -m uvicorn main:app --port 8000")
        return False
    
    print("\n" + "="*70)
    print("💡 ALTERNATIVE SOLUTIONS")
    print("="*70)
    print("""
Option 1: USE DASHBOARD
   1. Open http://localhost:3000
   2. Click the STOP button
   3. Wait 5 seconds
   4. Run verification script

Option 2: REST API (curl)
   curl -X POST http://localhost:8000/api/stop

Option 3: DIRECTLY IN CODE
   import requests
   requests.post("http://localhost:8000/api/stop")

Option 4: KEYBOARD SHORTCUT
   In backend terminal: Press Ctrl+C to stop bot
   
Option 5: RESTART EVERYTHING
   1. Stop backend: Ctrl+C in backend terminal
   2. All trades will be saved automatically
   3. Restart backend: python -m uvicorn main:app --port 8000
    """)
    
    print("="*70 + "\n")

if __name__ == "__main__":
    stop_bot()
