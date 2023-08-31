import os
import re
import shutil

def create_or_update_file(output_file):
    if os.path.exists(output_file):
        print(f"File exists, updating {output_file}")
    else:
        print(f"Creating {output_file}")
        shutil.copy('./content/zh/template.md', output_file)

def process_markdown(markdown_file, target_directory):
    count_line = 0

    with open(markdown_file, 'r') as file:
        for line in file:
            if '*' not in line:
                continue

            line = line.strip('*').strip()
            count_line += 1

            # Extract price_mark using regular expression
            price_match = re.search(r'NT([^ ]*)', line)
            if price_match:
                price_mark = price_match.group(1)
            else:
                price_mark = ""

            line = re.sub(r'NT.*$', '', line).strip()

            output_file = f"./content/zh/{target_directory}/{line}.md"
            create_or_update_file(output_file)

            with open(output_file, 'r') as output_f:
                content = output_f.read()
            
            if 'price:' in content:
                print("There is price tag")
                content = re.sub(r'^price:.+', f'price: [{price_mark}]', content, flags=re.MULTILINE)
            else:
                print("No price tag, creating one")
                formatted_price = f'price: [{price_mark}]'
                content = re.sub(r'^title:.+', f'{formatted_price}\n\\g<0>', content)

            if 'weight:' in content:
                print("There is weight tag")
                content = re.sub(r'^weight:.+', f'weight: {count_line}', content, flags=re.MULTILINE)
            else:
                print("No weight tag, creating one")
                formatted_weight = f'weight: {count_line}'
                content = re.sub(r'^date:.+', f'{formatted_weight}\n\\g<0>', content)

            with open(output_file, 'w') as output_f:
                output_f.write(content)

def main():
    markdown_file = 'your_markdown_file.md'
    target_directory = 'your_target_directory'

    if not os.path.isfile(markdown_file):
        print(f"File not found: {markdown_file}")
        return

    process_markdown(markdown_file, target_directory)

if __name__ == '__main__':
    main()
