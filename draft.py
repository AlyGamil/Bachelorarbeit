thisdict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

confi_nodes = ["n3", "n1", "n2"]

for i in confi_nodes:
    thisdict.update({i: []})

thisdict["n1"].append(1)
thisdict["n1"].append(2)
print(thisdict)