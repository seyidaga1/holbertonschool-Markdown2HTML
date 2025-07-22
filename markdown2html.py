#!/usr/bin/python3
import sys

def convert_heading(line) :
    if line.startswith("#") :
        heading_level = line.count("#")
        heading_text = line.strip("# ").strip()
        heading = f"<h{heading_level}>{heading_text}</h{heading_level}>"
        print(heading)
        return heading


def markdown_file(name,output) :
    try :
        with open(name,'r') as file :
            markdown_lines = file.readlines()

        converted_lines = []
        for line in markdown_lines :
            converted_line = convert_heading(line)
            # converted_line = convert_unordered_list(converted_line)
            converted_lines.append(f"{converted_line}\n")

        with open(output,'w') as file :
            for line in converted_lines :
                file.write(line) 

    except FileNotFoundError:
        sys.stderr.write(f"There is no such file that named : {name}")



if __name__ == '__main__' :
    if len(sys.argv) != 3 :
        sys.stderr.write("Usage : ./markdown2html.py README.md README.html")
        sys.exit(1)
    
    
    markdown_file(sys.argv[1],sys.argv[2])