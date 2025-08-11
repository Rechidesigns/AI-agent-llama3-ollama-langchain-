## 🧩 User Flow Diagram

```mermaid
flowchart TD
    A[User sends request to FastAPI endpoint] --> B{Which endpoint?}

    B -->|/chat| C[Chat Agent: Uses Ollama Llama3 Model via LangChain]
    B -->|/finance| D[Finance Agent: Data Parsing + LLM Insights]
    B -->|/summarize| E[Summarization Agent: LLM Text Condenser]

    C --> F[LangChain processes request]
    D --> F
    E --> F

    F --> G[PostgresChatMessageHistory stores interaction]
    G --> H[Return response to FastAPI]
    H --> I[Send JSON Response to User]





#This diagram shows:  
- **User → FastAPI** (selects one of the three endpoints)  
- **FastAPI → LangChain Agent → Ollama Llama3**  
- **LangChain saves history** in Postgres using `PostgresChatMessageHistory`  
- **Response returned** to the user.  
