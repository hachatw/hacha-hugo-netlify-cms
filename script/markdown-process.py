import sys
import os
import re
import subprocess

def read_markdown_file(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines
    
def process_line(line):
    # Remove any number of white spaces after asterisk and dash 
    if line.startswith("-"):
        line = re.sub(r'\-\s+', '-', line)
        line = line.replace('-', '')

    if line.startswith("*"):
        line = re.sub(r'\*\s+', '*', line)
        line = line.replace('*', '')

    # Remove white space before "NT" but keep after non-space characters
    line = re.sub(r'(?<=[^\s])\s+NT', ' NT', line)
    line = line.split(' NT')[0] 
    # Remove text after NT
    line = line.split(' NT')[0]

    # Remove any number of hash symbols followed by space
    line = re.sub(r'#+\s', '', line)

    # Remove "title:" and keep the data
    if line.startswith('category:'):
        line = line.replace('category:', '').strip()

    if line.startswith('categories:'):
        line = line.replace('categories:', '').strip()

    # Remove white spaces at the beginning and end of the line
    line = line.strip()
    return line

def replace_section_with_list(directory, file_name, section_name, new_values):
    file_path = f"{directory}/{file_name}.md"
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    if "category" in content:
       content = content.replace("category:","categories:") 

    section_start = content.find(section_name)
    if section_start == -1:
        print(f"Section '{section_name}' not found in the file.")
        return

    section_end = content.find('tags:', section_start)
    if section_end == -1:
        section_end = len(content)

    new_content = f"{section_name}\n"
    for value in new_values:
        new_content += f"  - {value}\n"

    updated_content = content[:section_start] + new_content + content[section_end:]

    with open(file_path, 'w') as file:
        file.write(updated_content)

# Replace the "categories" section with values from a list

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <menu_directory>")
        sys.exit(1)

    menu_directory = sys.argv[1]
    if not os.path.isdir(menu_directory):
        print(f"Error: {menu_directory} is not a valid directory.")
        sys.exit(1)

    for root, dirs, files in os.walk(menu_directory):
        for filename in files:
            if filename == "index.md":
                markdown_file = os.path.join(root, filename)
                lines = read_markdown_file(markdown_file)
                process_markdown_file(lines)
                # Perform your processing on 'lines' here

def process_markdown_file(lines):
    main_category=""
    categories_append=""
    list_category=[]
    
    for line in lines:
        if line.startswith("category:"):
            main_category = process_line(line) 

        directory = 'content/zh/items/' + main_category
        print (directory + "this is " + line)  # Only print lines that start with #

        if line.startswith("#"):
            categories_append = process_line(line) 
            list_category.append(categories_append)
            print("\n Append" +categories_append+"\n")
            print( directory + "/" + categories_append)
            command = ['hugo', 'new', f'{directory}/{categories_append}/_index.md']
            subprocess.run(command, capture_output=True, text=True)

        if line.startswith("-"):
            try:
                items_file_name = process_line(line)
                new_values = [main_category, categories_append]
                replace_section_with_list(directory, items_file_name, 'categories:', new_values)
                command = ['mv', f'{directory}/{items_file_name}.md' , f'{directory}/{categories_append}/{items_file_name}.md']
                subprocess.run(command, capture_output=True, text=True)
                print(items_file_name)
                print(new_values)  # Only print lines that start with *
                
            except FileNotFoundError:
                print(items_file_name + "not found")

        if line.startswith("*"):
            try:
                items_file_name = process_line(line)
                new_values = [main_category, categories_append]
                replace_section_with_list(directory, items_file_name, 'categories:', new_values)
                command = ['mv', f'{directory}/{items_file_name}.md' , f'{directory}/{categories_append}/{items_file_name}.md']
                subprocess.run(command, capture_output=True, text=True)
                print(items_file_name)
                print(new_values)  # Only print lines that start with *

            except FileNotFoundError:
                print(items_file_name + "not found")
    print(list_category)

if __name__ == '__main__':
    main()
