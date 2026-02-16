#!/bin/bash

uv run main.py $1 | xclip -selection clipboard
notify-send "Linkedin Post Content copied to clipboardl"
