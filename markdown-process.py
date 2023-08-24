import sys

def read_markdown_file(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines
    
def replace_section_with_list(directory, file_name, section_name, new_values):
    file_path = f"{directory}/{file_name}"
    
    with open(file_path, 'r') as file:
        content = file.read()

    section_start = content.find(section_name)
    if section_start == -1:
        print(f"Section '{section_name}' not found in the file.")
        return

    section_end = content.find('\n', section_start)
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
        print("Usage: python script.py <markdown_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    lines = read_markdown_file(markdown_file)

    for line in lines:
        if line.startswith("title"):
            categories = line 
            directory = 'content/zh/items/' + categories
            print(directory)  # Only print lines that start with #
        if line.startswith("#"):
            categories_append = line 
            print(categories_append)  # Only print lines that start with #
        if line.startswith("*"):
            items_file_name = line
            new_values = ['categories', 'categories_append']
            replace_section_with_list(directory, items_file_name, 'categories:', new_values)
            print(new_values)  # Only print lines that start with *
if __name__ == '__main__':
    main()
