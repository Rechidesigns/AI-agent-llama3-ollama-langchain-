import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import psycopg
from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

try:
    from langchain_postgres import PostgresChatMessageHistory
except Exception:
    from langchain_community.chat_message_histories import PostgresChatMessageHistory

load_dotenv()

EXPIRATION_HOURS = 2  # messages older than this will be deleted


def get_conversation(session_id: str):
    """Build a ConversationChain for a given session UUID"""
    sync_connection = psycopg.connect(os.getenv('POSTGRES_URL'))

    # Ensure table exists
    PostgresChatMessageHistory.create_tables(sync_connection, 'message_store')

    # Cleanup old messages before loading conversation
    cutoff_time = datetime.utcnow() - timedelta(hours=EXPIRATION_HOURS)
    with sync_connection.cursor() as cur:
        cur.execute(
            "DELETE FROM message_store WHERE created_at < %s",
            (cutoff_time,)
        )
        sync_connection.commit()

    # Build chat history object
    history = PostgresChatMessageHistory(
        'message_store',        # table_name
        session_id,             # session_id (must be UUID)
        sync_connection=sync_connection
    )

    # Use ConversationBufferMemory with Postgres history
    memory = ConversationBufferMemory(
        memory_key='history',
        return_messages=True
    )

    llm = ChatOllama(
        model=os.getenv('OLLAMA_MODEL', 'mistral'),
        base_url=os.getenv('OLLAMA_URL')
    )

    return ConversationChain(llm=llm, memory=memory, verbose=False)
