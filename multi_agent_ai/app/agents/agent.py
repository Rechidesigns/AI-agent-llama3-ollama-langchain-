import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import psycopg
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableSequence, RunnableMap
from langchain.prompts import PromptTemplate    

try:
    from langchain_postgres import PostgresChatMessageHistory
except Exception:
    from langchain_community.chat_message_histories import PostgresChatMessageHistory

load_dotenv()

EXPIRATION_HOURS = 2  # messages older than this will be deleted
MAX_HISTORY = 10       # number of previous messages to include


def get_conversation_runnable(session_id: str):
    """Return a RunnableSequence for a session with recent history."""

    sync_connection = psycopg.connect(os.getenv('POSTGRES_URL'))

    # Ensure table exists
    PostgresChatMessageHistory.create_tables(sync_connection, 'message_store')

    # Clean up old messages
    cutoff_time = datetime.utcnow() - timedelta(hours=EXPIRATION_HOURS)
    with sync_connection.cursor() as cur:
        cur.execute(
            "DELETE FROM message_store WHERE created_at < %s",
            (cutoff_time,)
        )
        sync_connection.commit()

    # Fetch last N messages
    history_store = PostgresChatMessageHistory(
        'message_store',
        session_id,
        sync_connection=sync_connection
    )
    recent_history = "\n".join([m.content for m in history_store.messages[-MAX_HISTORY:]])

    # Prompt template includes both previous chat and current input
    prompt = PromptTemplate(
        input_variables=['text', 'chat_history'],
        template="""
Conversation History:
{chat_history}

New Message:
{text}
"""
    )

    llm = ChatOllama(
        model=os.getenv('OLLAMA_MODEL', 'mistral'),
        base_url=os.getenv('OLLAMA_URL')
    )

    # RunnableSequence expects each step to be a Runnable or PromptTemplate
    chain = RunnableSequence(prompt, llm)

    # Return the chain and recent history string
    return chain, recent_history
