FROM python:3.11.5-slim
RUN apt-get update && apt-get upgrade -y
WORKDIR /app
COPY ./transaction-fetcher/requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY ./transaction-fetcher/ /app
CMD ["python3","-u","main.py"]
