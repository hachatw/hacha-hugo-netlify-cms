import sys
import re
import subprocess

def read_markdown_file(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines
    
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

def process_line(line):
    # Remove leading and trailing whitespaces
    line = line.strip()

    # Remove asterisks * and hash # symbols
    line = line.replace('* ', '')
    # Remove any number of hash symbols followed by space
    line = re.sub(r'#+\s', '', line)
    # Remove text after NT
    line = line.split(' NT')[0]

    # Remove "title:" and keep the data
    if line.startswith('category:'):
        line = line.replace('category:', '').strip()

    if line.startswith('categories:'):
        line = line.replace('categories:', '').strip()

    return line


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <markdown_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    lines = read_markdown_file(markdown_file)
    list_category=[]

    main_category=""

    for line in lines:
        if line.startswith("category:"):
            main_category = process_line(line) 

        directory = 'content/zh/items/' + main_category
        print (directory + line)  # Only print lines that start with #

        if line.startswith("#"):
            categories_append = process_line(line) 
            list_category.append(categories_append)
            print("\n" +categories_append+"\n")
            print( directory + "/" + categories_append)
            command = ['hugo', 'new', f'{directory}/{categories_append}/_index.md']
            subprocess.run(command, capture_output=True, text=True)

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
