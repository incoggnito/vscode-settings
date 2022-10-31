import re

f = open('main.md', 'r')
lines = f.readlines()

new_lines = []
for line in lines:
    label = ""
    if "![" in line:
        print("Image found!")
        if "\label{" in line:
            label = line.split('\label{', 1)[1].split('}')[
                0]  # Retreive Lablel
            label = "](" + label + ")"
            # Replace word between brackets
            if re.findall(r']\(.*?\)'. line)[0] in :

            line = re.sub(r']\(.*?\)', label, line)
            print(line)
        if re.match(r"=")
    new_lines.append(line)

f = open('main_converted.md', 'w')
f.writelines(new_lines)

print("End")
