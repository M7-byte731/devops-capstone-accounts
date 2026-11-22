FROM python:3.9-slim

WORKDIR /app

ENV FLASK_APP=service:app
ENV PORT=8080

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service/ ./service/
COPY tests/ ./tests/
COPY setup.cfg Procfile ./

EXPOSE 8080

CMD ["gunicorn", "--bind=0.0.0.0:8080", "--workers=2", "service:app"]
