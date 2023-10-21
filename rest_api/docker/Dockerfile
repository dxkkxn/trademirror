FROM python:bullseye
RUN apt update -y && apt upgrade -y
WORKDIR /home/app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./src .
EXPOSE 5000
CMD ["python3","main.py"]


