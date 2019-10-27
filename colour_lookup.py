import json

data=[]

with open("colours.json", "r") as read_file:
    data = json.load(read_file)

# print(data)

def lookupColour(colourName):
    
    for point in data:
        if point['name'].lower()==colourName:
            return point['hex']
    return "#000000"
