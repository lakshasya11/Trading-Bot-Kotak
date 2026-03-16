import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def check_tables():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'trading_master_db'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT', '5432')
        )
        cur = conn.cursor()
        
        # Check tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        print("Tables found:", [t[0] for t in tables])
        
        # Check user_session_data columns
        if ('user_session_data',) in tables:
            cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'user_session_data'
            """)
            columns = cur.fetchall()
            print("\nColumns in user_session_data:")
            for col in columns:
                print(f" - {col[0]}: {col[1]}")
                
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_tables()
