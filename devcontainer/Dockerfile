FROM nvidia/cuda:12.0.0-cudnn8-devel-ubuntu20.04 as base

ENV TZ Asia/Tokyo
ENV DEBIAN_FRONTEND noninteractive

RUN sed -i 's/http:\/\/archive\.ubuntu\.com/http:\/\/jp\.archive\.ubuntu\.com/g' /etc/apt/sources.list

RUN apt-get update && apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    wget \
    curl \
    build-essential \
    git \
    cmake \
    unzip \
    tmux \
    libgl1-mesa-dev \
    libopencv-dev \
    libjpeg-dev \
    libpng-dev \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    liblzma-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install python3.10
RUN wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz && \
    tar xvf Python-3.10.13.tgz && \
    rm Python-3.10.13.tgz
WORKDIR /Python-3.10.13
RUN ./configure --enable-optimizations && \
    make -j 12 && \
    make altinstall && \
    update-alternatives --install /usr/bin/python python3 /usr/local/bin/python3.10 1 && \
    update-alternatives --install /usr/bin/pip pip3 /usr/local/bin/pip3.10 1

# poetry setting
RUN pip install -U poetry==1.6.1
RUN poetry config virtualenvs.create false

# kaggle setting
RUN pip install -U kaggle==1.5.16
COPY /.kaggle/kaggle.json /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json

RUN echo "export PS1='\[\e[36m\]kaeru\[\e[0m\] \[\e[32m\]env\[\e[0m\] \[\e[33m\]\w\[\e[0m\] $ '" >> /root/.bashrc
RUN echo "export LANG='ja_JP.UTF-8'" >> /root/.bashrc
RUN echo "alias vi='vim'" >> /root/.bashrc
RUN echo "alias gb='git branch'" >> /root/.bashrc
RUN echo "alias gst='git status'" >> /root/.bashrc

FROM base as dev

RUN mkdir -p /workspace
WORKDIR /workspace
