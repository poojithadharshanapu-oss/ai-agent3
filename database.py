def init_db():
    conn = get_db_connection()
    if conn is None:
        return
    
    try:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS ai_logs (
                id SERIAL PRIMARY KEY,
                question TEXT,
                answer TEXT
            );
        ''')
        conn.commit()
        cur.close()
    except Exception as e:
        print("Error initializing DB:", e)
    finally:
        conn.close()
