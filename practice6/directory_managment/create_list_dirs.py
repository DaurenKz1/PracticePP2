import os

files = os.listdir("practice6\\directory_managment\\directory1\\directory2")



for f in files:
    if f.endswith(".txt"):
        print(f)
