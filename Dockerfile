FROM python:3.11-slim

WORKDIR /app/myapp

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]

