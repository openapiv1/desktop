#!/bin/bash

export DISPLAY=:1

Xvfb :1 -ac -screen 0 1024x768x16 &
sleep 1
DISPLAY=:1 /usr/bin/xfce4-session
