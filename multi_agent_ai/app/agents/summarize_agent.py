from langchain.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

MODEL = os.getenv('OLLAMA_MODEL', 'mistral')
BASE = os.getenv('OLLAMA_URL')


def get_summary_agent():
    llm = ChatOllama(model=MODEL, base_url=BASE)
    prompt = PromptTemplate(
        input_variables=['text'],
        template='Summarize the following text in a concise bullet list:\n\n{text}'
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain