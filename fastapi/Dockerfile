FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt 

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
