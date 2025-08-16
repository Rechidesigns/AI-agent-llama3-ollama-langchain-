from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import os

MODEL = os.getenv('OLLAMA_MODEL', 'mistral')
BASE = os.getenv('OLLAMA_URL')


def get_summary_agent():
    llm = ChatOllama(model=MODEL, base_url=BASE)
    prompt = PromptTemplate(
        input_variables=['text'],
        template='Summarize the following text in a concise bullet list:\n\n{text}'
    )
    chain = RunnableSequence(prompt, llm) 
    return chain