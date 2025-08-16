from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import os

MODEL = os.getenv('OLLAMA_MODEL', 'mistral')
BASE = os.getenv('OLLAMA_URL')


def get_code_explainer():
    llm = ChatOllama(model=MODEL, base_url=BASE)
    prompt = PromptTemplate(
        input_variables=['code'],
        template=(
            "You are an expert software developer assistant. "
            "Analyze the following code and provide:\n"
            "1. The programming language\n"
            "2. Plain English explanation of what the code does\n"
            "3. Potential bugs or edge cases\n"
            "4. Suggestions for improvement or optimization\n"
            "5. Optional: refactored or cleaner version of the code if applicable\n\n"
            "Code:\n{code}"
        )
    )
    chain = RunnableSequence(llm, prompt)
    return chain