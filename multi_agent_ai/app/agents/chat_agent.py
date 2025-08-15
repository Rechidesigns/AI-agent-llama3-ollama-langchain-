from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Initialize the LLM
llm = Ollama(model="llama3")

# Set up memory (conversation history)
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# Create a prompt template
prompt_template = PromptTemplate(
    input_variables=["history", "input"],  # Must match memory_key and user input
    template="""
You are a helpful AI assistant.

Conversation so far:
{history}

User input:
{input}

Respond helpfully and clearly.
"""
)

# Create the conversation chain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt_template,
    verbose=True
)

# Function to chat
def chat_agent(user_input: str) -> str:
    return conversation.run(user_input)
