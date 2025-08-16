import os
from fastapi import FastAPI, UploadFile, File, Request, Response
from pydantic import BaseModel
from dotenv import load_dotenv
import pandas as pd
import io
from concurrent.futures import ThreadPoolExecutor
import asyncio

from multi_agent_ai.utils.session import get_or_create_session_id
from .app.agents.agent import get_conversation_runnable
from .app.agents.summarize_agent import get_summary_agent
from .app.agents.code_explainer_agent import get_code_explainer
from .app.agents.finance_agent import get_finance_agent
from .db import init_db

load_dotenv()
app = FastAPI(title="FastAPI LangChain Agent Starter")

# Initialize DB / tables
init_db()

# Thread pool for LLM invoke to avoid blocking
executor = ThreadPoolExecutor(max_workers=4)

async def run_llm_async(chain, input_text: str):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, lambda: chain.invoke(input_text))


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

    out = await run_llm_async(chain, text=prompt.message, chat_history=recent_history)
    return {"session_id": session_id, "response": out}


@app.post('/summarize')
async def summarize(data: TextInput):
    chain = get_summary_agent()
    out = await run_llm_async(chain, data.text)
    return {"summary": out}


@app.post('/code-explainer')
async def explain_code(data: CodeInput):
    chain = get_code_explainer()
    out = await run_llm_async(chain, data.code)
    return {"explanation": out}


@app.post('/finance')
async def analyze_finance(data: FinanceInput):
    chain = get_finance_agent()
    out = await run_llm_async(chain, data.data)
    return {"analysis": out}


@app.post('/finance/upload-csv')
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()

    # Try multiple encodings
    encodings_to_try = ['utf-8', 'utf-16', 'latin1']
    df = None
    for enc in encodings_to_try:
        try:
            df = pd.read_csv(io.BytesIO(contents), encoding=enc, on_bad_lines='skip', engine='python')
            break
        except Exception:
            continue

    if df is None:
        return {"error": "Unable to parse CSV file. Please upload a valid CSV."}

    # Convert to transaction list (limit to 500 for speed)
    max_rows = 500
    if 'amount' in df.columns and 'description' in df.columns:
        rows = [f"{r['description']} - {r['amount']}" for _, r in df.head(max_rows).iterrows()]
    else:
        rows = df.head(max_rows).astype(str).apply(lambda r: ', '.join(r.values), axis=1).tolist()

    chain = get_finance_agent()
    out = await run_llm_async(chain, '\n'.join(rows))  # <-- pass as single argument

    return {"analysis": out}
