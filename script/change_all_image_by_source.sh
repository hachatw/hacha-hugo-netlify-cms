#!/bin/bash

source_folder="./content/zh/items/台菜"
destination_folder="./content/zh/台菜"

# Iterate through each file in the destination folder
for destination_file in "$destination_folder"/*; do
    if [ -f "$destination_file" ]; then
        # Find corresponding file in source folder
        filename=$(basename "$destination_file")
        source_file="$source_folder/$filename"

        # Check if source file exists
        if [ -f "$source_file" ]; then
            # Extract image line from source file
            image_line=$(grep "image" "$source_file")

            # Escape special characters for awk
            escaped_image_line=$(echo "$image_line" | sed -e 's/[]\/$*.^[]/\\&/g')

            # Replace image line in destination file
            awk -v new_line="$escaped_image_line" '/^image/ {$0=new_line}1' "$destination_file" > tmpfile && mv tmpfile "$destination_file"
            echo "Replaced in: $destination_file"
        else
            echo "Source file not found: $source_file"
        fi
    fi
done

echo "Done"








