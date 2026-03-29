import os
from fastapi import FastAPI
import google.generativeai as genai
from database import get_db_connection, init_db

app = FastAPI()

# ✅ Secure API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# ✅ Initialize DB
@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"message": "AI agent is running"}

@app.get("/ask")
def ask_question(question: str):
    try:
        # 1. Generate response
        response = model.generate_content(question)
        answer = response.text if response.text else "No response generated"

        # 2. Store in DB
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO ai_logs (question, answer) VALUES (%s, %s)",
                (question, answer)
            )
            conn.commit()
            cur.close()
            conn.close()

        # 3. Return response
        return {
            "question": question,
            "answer": answer
        }

    except Exception as e:
        return {
            "error": str(e)
        }