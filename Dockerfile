# Use the official Python image as the base
FROM python:3.10.6-slim

WORKDIR /app

COPY app.py requirements.txt /app/
COPY data/ /app/data/
COPY .streamlit/secrets.toml /app/.streamlit/secrets.toml

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["streamlit", "run", "app.py"]
