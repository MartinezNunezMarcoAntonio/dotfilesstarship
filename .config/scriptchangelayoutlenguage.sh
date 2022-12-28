#!/bin/sh
# This shell script is PUBLIC DOMAIN. You may do whatever you want with it.

TOGGLE=$HOME/.toggle_touchpad

if [ ! -e $TOGGLE ]; then
    touch $TOGGLE
    setxkbmap -layout us -variant intl
    notify-send -t 1000 "International US"
else
    rm $TOGGLE
    setxkbmap us
    notify-send -t 1000 "Standard US"
fi
