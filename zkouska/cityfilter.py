import json

with open ("obce.geojson", encoding = "utf-8") as file:
    seznam_obci = json.load(file)
print(seznam_obci)
