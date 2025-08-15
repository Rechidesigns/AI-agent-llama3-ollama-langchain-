import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
# prefer the stable separate package for postgres chat history
try:
    from langchain_postgres import PostgresChatMessageHistory
except Exception:
    # fallback to langchain.community if installed
    from langchain_community.chat_message_histories import PostgresChatMessageHistory


def get_conversation():
    session_id = os.getenv('SESSION_ID', 'default-session')
    history = PostgresChatMessageHistory(
        connection_string=os.getenv('POSTGRES_URL'),
        session_id=session_id,
        table_name='message_store'
    )

    memory = ConversationBufferMemory(
        memory_key='chat_history',
        chat_memory=history,
        return_messages=True
    )

    llm = ChatOllama(model=os.getenv('OLLAMA_MODEL', 'mistral'), base_url=os.getenv('OLLAMA_URL'))

    conv = ConversationChain(llm=llm, memory=memory, verbose=False)
    return conv