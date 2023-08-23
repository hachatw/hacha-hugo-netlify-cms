#!/bin/bash

# Check if a Markdown file is provided as a command-line argument
if [ $# -eq 0 ]; then
  echo "Please provide the path to the Markdown file as an argument."
  exit 1
fi

# Get the Markdown file path from the command-line argument
markdown_file="$1"

# Check if the Markdown file exists
if [ ! -f "$markdown_file" ]; then
  echo "File not found: $markdown_file"
  exit 1
fi

# Declare an associative array to store variables
declare -a variables

# Read each line of the Markdown file
while IFS= read -r line
do
  # Check if the line starts with '#' symbols
  if [[ $line =~ ^#+ ]]; then
    # Extract the variable name (remove '#' symbols and trim)
    variable_name=$(echo "$line" | sed 's/^#\+//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
    current_variable="$variable_name"
  elif [ -n "$current_variable" ]; then
    # If there's a current variable name, store the line as its content
    variables["$current_variable"]+="$line"$'\n'
  fi
done < "$markdown_file"

# Display the captured variables
for variable_name in "${!variables[@]}"
do
  echo "Variable: $variable_name"
  echo "Content:"
  echo "${variables["$variable_name"]}"
  echo "----------"
done
