FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["sh", "-c", "PYTHONPATH=/app/src python src/init_db.py && uvicorn src.main:app --host 0.0.0.0 --port 8001"]