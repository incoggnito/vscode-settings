import re

f = open('main.md', 'r')
lines = f.readlines()


for line in lines:
    label = ""
    if "![" in line:
        print("Image found!")
        label = line.split('\label{', 1)[1].split('}')[0]
        label = "](" + label + ")"
        re.sub(r']\(.*?\)', label, line)  # Replace

print("End")
