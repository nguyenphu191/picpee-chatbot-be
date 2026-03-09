FROM python:3.11-slim

WORKDIR /app

# Cài dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy source
COPY app /app/app
COPY scripts /app/scripts

EXPOSE 8000

# Default ENV (có thể override qua docker-compose / biến môi trường)
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

