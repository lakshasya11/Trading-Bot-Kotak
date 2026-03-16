import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def check_signups():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'trading_master_db'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT', '5432')
        )
        cur = conn.cursor()
        
        cur.execute("SELECT client_id, username FROM client_bot_signups WHERE client_id = 'AC0003'")
        row = cur.fetchone()
        
        print(f"Signup Data for AC0003: {row}")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_signups()
