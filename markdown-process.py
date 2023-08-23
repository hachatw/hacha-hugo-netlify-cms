import sys

def read_markdown_file(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <markdown_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    lines = read_markdown_file(markdown_file)

    for line in lines:
        if line.startswith("title"):
            print(line)  # Only print lines that start with #
        if line.startswith("#"):
            print(line)  # Only print lines that start with #
        if line.startswith("*"):
            print(line)  # Only print lines that start with *
if __name__ == '__main__':
    main()
