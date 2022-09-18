FROM nvidia/cuda:11.1.1-cudnn8-runtime-ubuntu18.04

ENV LC_ALL=C.UTF-8
ENV LANG=c.UTF-8
ENV DASH_DEBUG_MODE True

RUN apt-get update
RUN apt-get -y install python3-pip
RUN pip3 install --upgrade pip

FROM python:3.9

WORKDIR /api

COPY requirements.txt .

RUN pip install -r requirements.txt && \
    pip install uvloop && \
    pip install pandas && \
    pip install torch==1.10.2+cu113 torchvision==0.11.3+cu113 torchaudio==0.10.2+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html && \
    pip install sklearn && \
    pip install psycopg2-binary 

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
RUN apt-get update
RUN apt-get install python3-tk -y

RUN apt-get update
RUN apt-get install vim -y

COPY . /api

EXPOSE 8050
CMD ["python", "main.py"]

