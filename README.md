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
