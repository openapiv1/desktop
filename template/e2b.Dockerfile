FROM ubuntu:22.04

# RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
#   python3-xlib \
#   x11-xserver-utils \
#   xfce4 \
#   xfce4-goodies \
#   xvfb \
#   xubuntu-icon-theme \
#   scrot \
#   python3-pip \
#   vim \
#   curl \
#   python3-tk \
#   python3-dev \
#   x11-utils \
#   gnumeric \
#   xserver-xephyr

# RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y \
#   build-essential curl git util-linux jq

ENV PIP_DEFAULT_TIMEOUT=100 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_CACHE_DIR=1 \
  DEBIAN_FRONTEND=noninteractive

COPY ./requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt && ipython kernel install --name "python3" --user

RUN mkdir -p /home/user/.ipython/profile_default
COPY ipython_kernel_config.py /home/user/.ipython/profile_default/

COPY ./start-up.sh /home/user/
RUN chmod +x /home/user/start-up.sh

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  python3-xlib \
  x11-xserver-utils \
  xfce4 \
  xfce4-goodies \
  xvfb \
  xubuntu-icon-theme \
  scrot \
  python3-pip \
  vim \
  curl \
  python3-tk \
  python3-dev \
  x11-utils \
  gnumeric \
  xserver-xephyr
