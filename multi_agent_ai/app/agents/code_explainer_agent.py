from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

MODEL = os.getenv('OLLAMA_MODEL', 'mistral')
BASE = os.getenv('OLLAMA_URL')


def get_code_explainer():
    llm = ChatOllama(model=MODEL, base_url=BASE)
    prompt = PromptTemplate(
        input_variables=['code'],
        template=('Explain what the following code does in plain English. Include potential bugs and suggestions for improvement:\n\n'
                  '{code}')
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain