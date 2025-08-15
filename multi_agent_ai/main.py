import os
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv
from .app.agents.agent import get_conversation
from .app.agents.summarize_agent import get_summary_agent
from .app.agents.code_explainer_agent import get_code_explainer
from .app.agents.finance_agent import get_finance_agent
from .db import init_db

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
async def chat(prompt: Prompt):
    conv = get_conversation()
    resp = conv.predict(input=prompt.message)
    return {"response": resp}

@app.post('/summarize')
async def summarize(data: TextInput):
    chain = get_summary_agent()
    out = chain.run(text=data.text)
    return {"summary": out}

@app.post('/code-explainer')
async def explain_code(data: CodeInput):
    chain = get_code_explainer()
    out = chain.run(code=data.code)
    return {"explanation": out}

@app.post('/finance')
async def analyze_finance(data: FinanceInput):
    chain = get_finance_agent()
    out = chain.run(data=data.data)
    return {"analysis": out}

@app.post('/finance/upload-csv')
async def upload_csv(file: UploadFile = File(...)):
    # parse with pandas and convert to plain text/CSV to feed to finance agent
    import pandas as pd
    contents = await file.read()
    import io
    df = pd.read_csv(io.BytesIO(contents))
    # convert to a simple transaction list
    rows = []
    if 'amount' in df.columns and 'description' in df.columns:
        for _, r in df.iterrows():
            rows.append(f"{r['description']} - {r['amount']}")
    else:
        # fallback: stringify rows
        rows = df.astype(str).apply(lambda r: ', '.join(r.values), axis=1).tolist()

    chain = get_finance_agent()
    out = chain.run(data='\n'.join(rows))
    return {"analysis": out}