import psycopg2
from psycopg2 import sql

def fix_schema_and_test_connection():
    config = {
        'host': 'localhost',
        'database': 'trading_master_db',
        'user': 'postgres',
        'password': '3917',
        'port': '5432'
    }
    
    # 1. Fix Schema via Remote IP (Confirmed working)
    print("Connecting to 192.168.0.104 to fix schema...")
    try:
        remote_config = config.copy()
        remote_config['host'] = '192.168.0.104'
        
        conn = psycopg2.connect(**remote_config)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if constraint exists, if not add it
        table_name = 'client_bot_signups'
        cur.execute(f"ALTER TABLE {table_name} DROP CONSTRAINT IF EXISTS client_bot_signups_client_id_key")
        cur.execute(f"ALTER TABLE {table_name} ADD CONSTRAINT client_bot_signups_client_id_key UNIQUE (client_id)")
        print("✓ Successfully added UNIQUE constraint to client_bot_signups(client_id)")
        
        conn.close()
    except Exception as e:
        print(f"❌ Schema fix failed: {e}")

if __name__ == "__main__":
    fix_schema_and_test_connection()
