import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('POSTGRES_URL') or 'postgresql+psycopg://postgres:postgres@localhost:5432/ai_agent'

engine = create_engine(DB_URL, future=True)

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS message_store (
            id SERIAL PRIMARY KEY,
            session_id TEXT NOT NULL,
            message JSONB NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        """))
        conn.commit()
