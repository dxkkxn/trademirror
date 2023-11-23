FROM python:3.11.5
RUN apt-get update && apt-get upgrade -y
WORKDIR /app
COPY ./frequent_traders_detection/database-driver/requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY ./frequent_traders_detection/database-driver/ /app
CMD ["python3","-u","main.py"]

