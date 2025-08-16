FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for psycopg3 / psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    pip install --no-cache-dir psycopg2-binary

# Copy the whole project
COPY . /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run the app
CMD ["uvicorn", "multi_agent_ai.main:app", "--host", "0.0.0.0", "--port", "8000"]
