#!/usr/bin/python3

"""
markdown2html.py

A simple Markdown to HTML converter.

Usage:
    ./markdown2html.py README.md README.html
"""

import sys


def convert_p_tag(line, p_tag):
    p_text = line.rstrip('\n')
    if not p_tag:
        return f"<p>\n{p_text}", True
    else:
        return f"<br/>\n{p_text}", True


def convert_ordered_list(line, in_list_ol):
    ol_text = line.strip("*").strip()
    if not in_list_ol:
        return f"<ol>\n\t<li>{ol_text}</li>", True
    else:
        return f"\t<li>{ol_text}</li>", True


def convert_unordered_list(line, in_list_ul):
    ul_text = line.strip("-").strip()
    if not in_list_ul:
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
        in_list_ul = False
        in_list_ol = False
        p_tag = False

        for idx, line in enumerate(markdown_lines):
            stripped = line.strip()

            if line.startswith("#"):
                if in_list_ul:
                    converted_lines.append("</ul>\n")
                    in_list_ul = False
                if in_list_ol:
                    converted_lines.append("</ol>\n")
                    in_list_ol = False
                if p_tag:
                    converted_lines.append("</p>\n")
                    p_tag = False
                converted_line = convert_heading(line)
                converted_lines.append(f"{converted_line}\n")

            elif line.startswith("-"):
                if in_list_ol:
                    converted_lines.append("</ol>\n")
                    in_list_ol = False
                if p_tag:
                    converted_lines.append("</p>\n")
                    p_tag = False
                converted_line, in_list_ul = convert_unordered_list(line, 
                                                                    in_list_ul)
                converted_lines.append(f"{converted_line}\n")

            elif line.startswith("*"):
                if in_list_ul:
                    converted_lines.append("</ul>\n")
                    in_list_ul = False
                if p_tag:
                    converted_lines.append("</p>\n")
                    p_tag = False
                converted_line, in_list_ol = convert_ordered_list(line, in_list_ol)
                converted_lines.append(f"{converted_line}\n")

            elif stripped == "":
                if in_list_ul:
                    converted_lines.append("</ul>\n")
                    in_list_ul = False
                if in_list_ol:
                    converted_lines.append("</ol>\n")
                    in_list_ol = False
                if p_tag:
                    converted_lines.append("</p>\n")
                    p_tag = False

            else:
                if not p_tag:
                    converted_line, p_tag = convert_p_tag(line, p_tag)
                    converted_lines.append(f"{converted_line}\n")
                else:
                    converted_line, p_tag = convert_p_tag(line, p_tag)
                    converted_lines.append(f"{converted_line}\n")

        if in_list_ul:
            converted_lines.append("</ul>\n")
        if in_list_ol:
            converted_lines.append("</ol>\n")
        if p_tag:
            converted_lines.append("</p>\n")

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
