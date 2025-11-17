import json

data = json.load(open("DT_PacenoteTokens_EA.json"))
data = data[0]["Rows"]


f = open("pacenotes.txt", "w")

for key, value in data.items():
    print(key)
    f.write(key + "\n")