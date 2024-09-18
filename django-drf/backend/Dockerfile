FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh

COPY . .

EXPOSE 8000

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
