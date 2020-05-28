import json
from collections import OrderedDict

with open("items.json", "r") as file:
    this = json.load(file)

keys = sorted(this.keys())

newthis = OrderedDict()
for i in keys:
    newthis[i] = this[i]

with open("items.json", "w") as file:
    json.dump(newthis, file)
