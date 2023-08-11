#!/bin/bash

source_folder="./content/zh/items/台菜"
destination_folder="./content/zh/台菜"

# Iterate through each file in the source folder
for source_file in "$source_folder"/*; do
    if [ -f "$source_file" ]; then
        # Extract image line from source file
        image_line=$(grep "image:" "$source_file")

        if [ -n "$image_line" ]; then
            # Get filename from source file
            filename=$(basename "$source_file")

            # Find corresponding file in destination folder
            destination_file="$destination_folder/$filename"
            
            # Extract image line from destination file
            destination_image_line=$(grep "image:" "$destination_file")

            # Compare source and destination image lines using pattern-based match
            if ! grep -qF "$image_line" <<< "$destination_image_line"; then
                # Replace image line in destination file using awk
                if [ -f "$destination_file" ]; then
                    awk -v new_line="$image_line" '{gsub(/image:.*/, new_line)}1' "$destination_file" > tmpfile && mv tmpfile "$destination_file"
                    echo "Replaced in: $destination_file"
                else
                    echo "Destination file not found: $destination_file"
                fi
            fi
        fi
    fi
done

echo "Done"

