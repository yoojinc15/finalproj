import json
import glob

path = ".\\SF/*"
file_list = glob.glob(path)
# file_list_py = [file for file in file_list if file.endswith(".py")]
print(file_list)

businesses_list = {}

for f in file_list:
    print(f)
    with open(f, "r") as j:
        v = json.load(j)
    for b in v['businesses']:
        businesses_list[b['id']] = b
        print(b['id'])

with open("SF_businesses.json", "w") as j:
    json.dump(businesses_list, j)
