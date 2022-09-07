FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

WORKDIR /ml-api

COPY . ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /ml-api/requirements/requirements.txt

CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port $PORT"]
