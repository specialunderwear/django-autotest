#!/bin/sh
# Displays a desktop notification using Growl (OS X) or libnotify (Linux). 

title=$1
message=$2
icon=$3


if type -P growlnotify >/dev/null; then
	growlnotify --image "$icon" -m "$message" "$title"
else 
	if type -P notify-send >/dev/null; then
	notify-send "$title" "$message" -i "$icon"
	fi
fi
