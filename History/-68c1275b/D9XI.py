import re

f = open('main.md', 'r')
lines = f.readlines()

new_lines = []
del_line = False
for line in lines:
    label = ""
    if "![" in line:
        print("Image found!")
        if "\label{" in line:

            # find the new image name
            label = line.split('\label{', 1)[1].split('}')[
                0]  # Retreive Lablel
            label = "](image/" + label + ")"

            # add the height and width information
            pattern = r"\s=\d{3}x\d{3}"
            if len(re.findall(pattern, line)) > 0:
                size = re.findall(pattern, line)[0]
                w, h = size[2:].split("x")
                line = line[:-1] + "{ width=" + w + " heigth=" + h + " }\n"
                print(line)

            # Replace the image link
            line = re.sub(r']\(.*?\)', label, line)
            print(line)

    # remove all info boxes
    pattern = r":{3}\w"
    if len(re.findall(pattern, line)) > 0:
        del_line = True

    if not del_line:
        print(line)
        new_lines.append(line)

    pattern = r":{3}$"
    if len(re.findall(pattern, line)) > 0:
        del_line = False


f = open('main_converted.md', 'w')
f.writelines(new_lines)

print("End")
