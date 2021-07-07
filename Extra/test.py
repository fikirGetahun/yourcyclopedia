import json
import datetime
import sys
from collections import namedtuple

data = {
    "music": [{
        "id": 3,
        "NF": "rap",
        "what": [
            {
                "a" : "bbb",
                "b" : "ddd"
            },
            {
                "d" : "ggg",
                "f" : "ddd"
            }
            ],
        "emenem": "rap and hiphop",
        "jocole": "rap and trap lazy"
    }]
    ,
    "trds":[{
        "id":9,
        "ghg":"ghgh",
        "ggh":"jh"
    }]
    
}

new = {
    "id" : 10,
    "ghg" : "new file",
    "ggh" : "new"
}
 


dumper =    json.dumps(new, indent=4)

# with open("test.json", "w") as write:
#     json.dump(data, write)
# filee = open("test.json", "r")
# write = json.load(filee)
# write["trds"].append(new) 
# filee.close()

# filee = open("test.json", "w")
# json.dump(write, filee)
# filee.close()

with open("test.json") as read:
    x = json.loads(read.read(), object_hook = lambda d : namedtuple('x', d.keys() ) (*d.values()))

# file = open("test.json", "r")
# load = json.load(file)
# cal = []
# cal = load["trds"] 
# file.close()
# s = x[1]
# print(x[1][0].ghg[1])

# for each in s:
#     print(each.id)
x = len(data)
print(type(x))
# file = open("test.json", "w")
# json.dump(load, file)
# file.close()

# with open("test.json") as read:
#     j = json.loads(read.read(), object_hook = lambda d : namedtuple('x', d.keys() ) (*d.values()))

# file = open("test.json", "r")
# load = json.load(file)
# num = len(load["trds"])
# file.close()

# print(num)
# var= "afds"
# open(f"drafts/{var}.py ", "x")
# print(j[1].id)


# collect = ""
# text = "abcdefg"

# for s in text:
#     collect = collect + s

# print(collect)