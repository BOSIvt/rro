#!/bin/bash

application=./meeting_helper.py
$application & xterm
#sleep 5s
wmctrl -b toggle,fullscreen

