import os
from fastapi import FastAPI, UploadFile, File, Request, Response
from pydantic import BaseModel
from dotenv import load_dotenv

from multi_agent_ai.utils.session import get_or_create_session_id
from .app.agents.agent import get_conversation_runnable
from .app.agents.summarize_agent import get_summary_agent
from .app.agents.code_explainer_agent import get_code_explainer
from .app.agents.finance_agent import get_finance_agent
from .db import init_db
import pandas as pd
import io

load_dotenv()

app = FastAPI(title="FastAPI LangChain Agent Starter")

# Initialize DB / tables
init_db()

class Prompt(BaseModel):
    message: str

class TextInput(BaseModel):
    text: str

class CodeInput(BaseModel):
    code: str

class FinanceInput(BaseModel):
    data: str

@app.post('/chat')
async def chat(prompt: Prompt, request: Request, response: Response):
    session_id = get_or_create_session_id(request, response)
    chain, recent_history = get_conversation_runnable(session_id=session_id)

    # Pass a dict to match the prompt variables
    out = chain.invoke({
        "text": prompt.message,
        "chat_history": recent_history
    })

    return {"session_id": session_id, "response": out}



@app.post('/summarize')
async def summarize(data: TextInput):
    chain = get_summary_agent()
    # Pass the text as the single positional input
    out = chain.invoke(data.text)
    return {"summary": out}



@app.post('/code-explainer')
async def explain_code(data: CodeInput):
    chain = get_code_explainer()
    out = chain.invoke(data.code)
    # out = chain.invoke({"code": data.code})
    return {"explanation": out}

@app.post('/finance')
async def analyze_finance(data: FinanceInput):
    chain = get_finance_agent()
    out = chain.invoke(data.data)
    return {"analysis": out}

@app.post('/finance/upload-csv')
async def upload_csv(file: UploadFile = File(...)):
    import pandas as pd
    import io

    contents = await file.read()
    
    encodings_to_try = ['utf-8', 'utf-16', 'latin1']
    df = None
    for enc in encodings_to_try:
        try:
            df = pd.read_csv(io.BytesIO(contents), encoding=enc, on_bad_lines='skip', sep=None, engine='python')
            break
        except Exception:
            continue

    if df is None:
        return {"error": "Unable to parse CSV file. Please upload a valid CSV."}

    # Convert to transaction list
    rows = []
    if 'amount' in df.columns and 'description' in df.columns:
        for _, r in df.iterrows():
            rows.append(f"{r['description']} - {r['amount']}")
    else:
        rows = df.astype(str).apply(lambda r: ', '.join(r.values), axis=1).tolist()

    chain = get_finance_agent()
    out = chain.invoke('\n'.join(rows))
    
    return {"analysis": out}

