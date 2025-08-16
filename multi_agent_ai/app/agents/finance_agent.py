from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import os

MODEL = os.getenv('OLLAMA_MODEL', 'mistral')
BASE = os.getenv('OLLAMA_URL')


def get_finance_agent():
    llm = ChatOllama(model=MODEL, base_url=BASE)

    prompt = PromptTemplate(
        input_variables=['data'],
        template=(
            "You are a financial analyst. Given the following transaction lines (one per line), produce:\n"
            "1) total expenses (sum)\n2) top 3 categories or merchants\n3) any anomalies\n4) practical suggestions to save money.\n\n"
            "Transactions:\n{data}"
        )
    )

    chain = RunnableSequence(llm, prompt)
    return chain