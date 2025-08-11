from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

def chat_agent(user_input: str) -> str:
    prompt = f"User: {user_input}\nAI:"
    return llm.invoke(prompt)
