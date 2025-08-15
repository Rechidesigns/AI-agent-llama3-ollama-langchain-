FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for psycopg3
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
# Copy requirements first so Docker can cache dependencies separately from source code
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy your app code
COPY ./multi_agent_ai /app

ENV PYTHONUNBUFFERED=1

# Run the app
CMD ["uvicorn", "multi_agent_ai.main:app", "--host", "0.0.0.0", "--port", "8000"]
