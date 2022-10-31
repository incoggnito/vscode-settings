f = open('main.md', 'r') 
lines = f.readlines()


for line in lines:
    if "![" in line:
        print("Image found!")

print("End")