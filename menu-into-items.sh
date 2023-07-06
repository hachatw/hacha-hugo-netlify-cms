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

  # Execute the "hugo new" command with the current line as input
  hugo new "$formated_folder/$line.md"

done < "$markdown_file"
