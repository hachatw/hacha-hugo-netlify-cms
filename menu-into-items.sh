#!/bin/bash

# Check if a Markdown file is provided as a command-line argument
if [ $# -eq 0 ]; then
  echo "Please provide the path to the Markdown file as an argument."
  exit 1
fi

# Get the Markdown file path from the command-line argument
markdown_file="$1"
target_directory="$2"

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
  ((count_line++))
  # Remove all spaces before "NT" using sed
  line="$(echo "$line" | sed -e 's/[[:space:]]*NT/NT/')"
  
  # Get the part after "NT" using awk (compatible with macOS)
  price_mark=$(echo "$line" | awk -F 'NT' '{gsub(/^[[:space:]]+|[[:space:]]+$/, "", $2); print $2}')

  # Remove the part after "NT" from the original line
  line="$(echo "$line" | sed -e 's/NT.*$//')"


  # Create temporary files for modification
  temp_file=$(mktemp)
  output_file="./content/zh/$target_directory/$line.md"

  # Execute the "hugo new" command with the current line as input
  if [[ -f $output_file ]];then
  echo "File exists, this is $line updating"
  else
  hugo new "$target_directory/$line.md"
  echo " create $markdown_file at $target_directory"
  fi
  
  echo "$count_line"

  # Check if "price:" exists in the file
  if grep -q 'price:' "$output_file"; then
  # Replace "price:[]" with "price: "price_mark""
  echo "there is price tags"
  sed -e "s/^price:.*/price: [$price_mark] /" "$output_file" > "$temp_file" && mv "$temp_file" "$output_file"
  else
  echo "no price create one "
  # Format the part_after_nt content as "price: [part_after_nt]"
  formatted_content="price: [$price_mark] "
  # Insert the formatted content to the third line of the generated Markdown file
  awk -v content="$formatted_content" 'NR==5 {print content} 1' "$output_file" > "$temp_file" && mv "$temp_file" "$output_file"
  fi

  if grep -q 'weight:' "$output_file"; then
  echo "there is weight tags"
  sed -e "s/^weight:.*/weight: $count_line /" "$output_file" > "$temp_file" && mv "$temp_file" "$output_file"
  else
  # Format the part_after_nt content as "price: [part_after_nt]"
  formatted_content="weight: [$count_line] "
  # Insert the formatted content to the third line of the generated Markdown file
  awk -v content="$formatted_content" 'NR==11 {print content} 1' "$output_file" > "$temp_file" && mv "$temp_file" "$output_file"
  fi

done < "$markdown_file"


  