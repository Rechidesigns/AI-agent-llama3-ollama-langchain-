from pydantic import BaseModel

class Prompt(BaseModel):
    message: str

class TextInput(BaseModel):
    text: str

class CodeInput(BaseModel):
    code: str

class FinanceInput(BaseModel):
    data: str
