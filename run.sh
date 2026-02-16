#!/bin/bash

DB="$HOME/personal/projects/coursera-link-copier/courses.db"
SAVE_DIR="/home/himanshu/work/assignments/predictive_stats/guided_projects/certs"

# Step 1: Select course
selected_course=$(sqlite3 -noheader -batch "$DB" "SELECT title FROM courses;" \
    | rofi -dmenu -p "Select Course")

[ -z "$selected_course" ] && exit 0

# Step 2: Extract certificate URL
cert_record=$(sqlite3 -noheader -batch "$DB" \
    "SELECT cert_link FROM courses WHERE title = '$selected_course';")

# Extract certificate ID from the record URL
# /records/X11MCPX6YFDR -> X11MCPX6YFDR
cert_id=$(basename "$cert_record")

# Build the PDF download URL
pdf_url="https://www.coursera.org/api/certificate.v1/pdf/$cert_id"

# Step 3: Choose action
action=$(echo -e "Copy Certificate Link\nPost on LinkedIn\nDownload PDF" | \
    rofi -dmenu -p "Action for: $selected_course")

[ -z "$action" ] && exit 0

case "$action" in
    "Copy Certificate Link")
	echo "$cert_record" | xclip -selection clipboard
        ;;
    "Post on LinkedIn")
        $HOME/personal/projects/coursera-link-copier/generate_post.sh "$selected_course" 
        xdg-open "https://www.linkedin.com/feed/"
        ;;
	"Download PDF")
		mkdir -p "$SAVE_DIR"
		wget -O "$SAVE_DIR/$selected_course.pdf" "$pdf_url"
		notify-send "Coursera" "Downloaded PDF for $selected_course"
	;;
esac
