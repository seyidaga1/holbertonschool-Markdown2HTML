#!/usr/bin/python3

"""
markdown2html.py

A simple Markdown to HTML converter.

Usage:
    ./markdown2html.py README.md README.html
"""

import sys


def convert_unordered_list(line, in_list):
    ul_text = line.strip("-").strip()
    print(ul_text)
    if not in_list:
        return f"<ul>\n\t<li>{ul_text}</li>", True
    else:
        return f"\t<li>{ul_text}</li>", True


def convert_heading(line):
    heading_level = line.count("#")
    heading_text = line.strip("# ").strip()
    heading = f"<h{heading_level}>{heading_text}</h{heading_level}>"
    return heading


def markdown_file(name, output):
    try:
        with open(name, 'r') as file:
            markdown_lines = file.readlines()

        converted_lines = []
        in_list = False

        for line in markdown_lines:
            if line.startswith("#"):
                if in_list:
                    converted_lines.append("</ul>\n")
                    in_list = False
                converted_line = convert_heading(line)
                converted_lines.append(f"{converted_line}\n")

            elif line.startswith("-"):
                converted_line, in_list = convert_unordered_list(line, in_list)
                converted_lines.append(f"{converted_line}\n")

        if in_list:
            converted_lines.append("</ul>\n")

        with open(output, 'w') as file:
            for line in converted_lines:
                file.write(line)

    except FileNotFoundError:
        sys.stderr.write(f"Missing {name}\n")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file(sys.argv[1], sys.argv[2])
