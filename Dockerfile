FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/logs && \
    chown -R root:root /app/logs

USER root

EXPOSE 7777

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7777"]