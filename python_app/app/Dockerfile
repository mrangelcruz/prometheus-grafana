FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir \
    flask \
    flask_sqlalchemy \
    flask_bcrypt \
    flask-wtf \
    prometheus_client \
    psycopg2-binary


CMD ["python", "app.py"]
