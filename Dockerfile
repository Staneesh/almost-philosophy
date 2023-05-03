FROM nvidia/cuda:11.8.0-devel-ubuntu20.04
ENV TZ=Europe/Warsaw
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip

# WORKDIR /almost-philisophy/
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
