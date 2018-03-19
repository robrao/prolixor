FROM ubuntu:16.04

# setup working dir
RUN mkdir -p $HOME/prolixor
COPY img_creation.py $HOME/prolixor/
COPY requirements.txt $HOME/prolixor/
ADD fonts $HOME/prolixor/fonts
WORKDIR $HOME/prolixor

# install python
RUN \
    apt-get update && \
    apt-get install -y python python-dev python-pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

