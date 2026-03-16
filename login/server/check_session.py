import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def check_latest_session():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'trading_master_db'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT', '5432')
        )
        cur = conn.cursor()
        
        cur.execute("""
            SELECT client_id, username, kite_username, session_date, login_time 
            FROM user_session_data 
            ORDER BY login_time DESC 
            LIMIT 1
        """)
        row = cur.fetchone()
        
        if row:
            print(f"Latest Session Data:")
            print(f"Client ID: {row[0]}")
            print(f"Login Username (DB): {row[1]}")
            print(f"Kite Username (DB): {row[2]}")
            print(f"Date: {row[3]}")
            print(f"Time: {row[4]}")
        else:
            print("No session data found.")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_latest_session()
