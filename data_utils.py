def addObject(obj, data_dir):
    data ={}
    with open(data_dir+'objects.json') as json_file:
        data = json.load(json_file)
 
    data['objects'].append(obj)
    # print(data)
    with open(data_dir+'objects.json', 'w') as outfile:
        json.dump(data, outfile)
 
def addRefusedObject(obj, data_dir):
    data ={}
    with open(data_dir+'refused_objects.json') as json_file:
        data = json.load(json_file)
 
    data['objects'].append(obj)
    # print(data)
    with open(data_dir+'refused_objects.json', 'w') as outfile:
        json.dump(data, outfile)