#!/bin/bash

# Check if a Markdown file is provided as a command-line argument
if [ $# -eq 0 ]; then
  echo "Please provide the path to the Markdown file as an argument."
  exit 1
fi

# Get the Markdown file path from the command-line argument
markdown_file="$1"
formated_folder="$2"

# Check if the Markdown file exists
if [ ! -f "$markdown_file" ]; then
  echo "File not found: $markdown_file"
  exit 1
fi

# Read each line of the Markdown file
while IFS= read -r line
do
  # Skip lines that don't contain the asterisk (*)
  if [[ ! "$line" == *"*"* ]]; then
    continue
  fi
  # Remove leading and trailing whitespaces
  line="$(echo "$line" | sed -e 's/^[[:space:]]*\* //')"

  # Skip empty lines
  if [ -z "$line" ]; then
    continue
  fi

  # Remove all spaces before "NT" using sed
  line="$(echo "$line" | sed -e 's/[[:space:]]*NT/NT/')"
  
  # Get the part after "NT" using awk (compatible with macOS)
  part_after_nt=$(echo "$line" | awk -F 'NT' '{gsub(/^[[:space:]]+|[[:space:]]+$/, "", $2); print $2}')

  # Remove the part after "NT" from the original line
  line="$(echo "$line" | sed -e 's/NT.*$//')"

  # Execute the "hugo new" command with the current line as input
  hugo new "$formated_folder/$line.md"

  echo " this is $markdown_file at $formated_folder"

  # Create temporary files for modification
  temp_file=$(mktemp)
  target_directory=$formated_folder
  output_file="./content/zh/$target_directory/$line.md"

  # Format the part_after_nt content as "price: [part_after_nt]"
  formatted_content="price: [$part_after_nt]"

  # Insert the formatted content to the third line of the generated Markdown file
  awk -v content="$formatted_content" 'NR==5 {print content} 1' "$output_file" > "$temp_file" && mv "$temp_file" "$output_file"


done < "$markdown_file"
