FROM ubuntu:latest
MAINTAINER Rajdeep Dua "dua_rajdeep@yahoo.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN pip3 install --upgrade pip
ADD requirements.txt .
RUN pip3 install -r requirements.txt
WORKDIR /home/ds
CMD ["python3", "run.py"]
