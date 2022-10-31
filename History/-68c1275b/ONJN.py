f = open('main.md', 'r')
lines = f.readlines()


for line in lines:
    if "![" in line:

        print("Image found!")
        if "\\label" in line:


print("End")
