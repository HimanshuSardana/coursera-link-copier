#!/bin/bash
course="$*"
uv run main.py "$course" | xclip -selection clipboard
notify-send "$course" "Post copied to clipboard"
