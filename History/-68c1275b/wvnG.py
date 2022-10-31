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
            pattern = r"\s=\d{3}x\d{3}"
            if re.findall(pattern, line) > 0:
                re.findall(pattern, line)
                line = line +

            line = re.sub(r']\(.*?\)', label, line)
            print(line)
    new_lines.append(line)

f = open('main_converted.md', 'w')
f.writelines(new_lines)

print("End")
