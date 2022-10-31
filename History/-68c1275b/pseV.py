import re

f = open('main.md', 'r')
lines = f.readlines()

new_lines = []
for line in lines:
    label = ""
    if "![" in line:
        print("Image found!")
        if "\label{" in line:
            label = line.split('\label{', 1)[1].split('}')[0]  # Retreive Lable
            label = "](" + label + ")"
            # Replace word between brackets
            line = re.sub(r']\(.*?\)', label, line)
            print(line)
    new_lines.append(line)

print("End")
