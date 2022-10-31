f = open('main.md', 'r')
lines = f.readlines()


for line in lines:
    if "![" in line:

        print("Image found!")

        label = line.split('\label{', 1)[1].split('}')[0]


print("End")
