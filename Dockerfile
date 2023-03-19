FROM python:3.10.6-slim
WORKDIR /prod
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app app
CMD uvicorn app.app:app --host 0.0.0.0 --port $PORT
