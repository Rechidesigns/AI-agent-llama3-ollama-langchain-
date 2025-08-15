FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY multi_agent_ai /app

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "multi_agent_ai.main:app", "--host", "0.0.0.0", "--port", "8000"]
