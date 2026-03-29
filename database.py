import psycopg2
import os

# ✅ Use environment variables (IMPORTANT for Render)
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432")
}

# ✅ Create DB connection
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None

# ✅ Initialize table
def init_db():
    conn = get_db_connection()
    
    if conn is None:
        print("Failed to connect to database")
        return

    try:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ai_logs (
                id SERIAL PRIMARY KEY,
                question TEXT,
                answer TEXT
            );
        """)

        conn.commit()
        cur.close()

    except Exception as e:
        print("Error creating table:", e)

    finally:
        conn.close()
