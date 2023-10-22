FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get upgrade -y

WORKDIR /app
COPY ./rest_api/requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY ./rest_api /app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
