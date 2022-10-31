import re

f = open('main.md', 'r')
lines = f.readlines()

new_lines = []
for line in lines:
    label = ""
    if "![" in line:
        print("Image found!")
        label = line.split('\label{', 1)[1].split('}')[0]
        label = "](" + label + ")"
        line = re.sub(r']\(.*?\)', label, line)  # Replace
        print(line)
    new_lines.append(line)

print("End")
