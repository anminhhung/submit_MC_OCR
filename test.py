import os

with open("results.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 

new_file = "new_results.txt"
with open(new_file, "a+") as f:
    for i in content:
        i = i.replace('"', '')
        f.write("{}\n".format(i))