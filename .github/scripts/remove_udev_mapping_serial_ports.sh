#!/bin/bash

# File with udev mapping data
OUTPUT_FILE="udev_mapping.txt"

# Check if the file exists
if [[ -f "$OUTPUT_FILE" ]]; then
    echo "Processing $OUTPUT_FILE..."
    
    while IFS= read -r line; do
        # Parse name inside SYMLINK+="..." for udev file
        symlink=$(echo "$line" | awk -F'SYMLINK\\+="' '{print $2}' | awk -F'_' '{print $1}')
        if [[ -n "$symlink" ]]; then
            echo "Removing /etc/udev/rules.d/99-$symlink.rules..."
            sudo rm "/etc/udev/rules.d/99-$symlink.rules"
            echo "udevadm: reload-rules..."
            sudo udevadm control --reload-rules || echo "Error for udevadm reload-rules."
	        sudo udevadm trigger || echo "Error for udevadm reload-rules."
        fi
    done < "$OUTPUT_FILE"

    echo "Done."
else
    echo "File $OUTPUT_FILE not found."
fi