import serial

def classes_to_string(classes):
    obj_as_string=""
    for item in classes:
        obj_as_string += item["class"]+" "
    return obj_as_string.strip()
 
def get_categories_from_classes(classes):
    categories = []
    for c in classes:
        if "type_hierarchy" in c.keys():
            categories.append(c["type_hierarchy"])
    return categories
 
def get_best_fitting_class(classes):  
    max_fit = 0
    best_fit = ""
    for c in classes:
        if c["score"] > max_fit:
            exploded=c["class"].split()
            if exploded[len(exploded)-1]!="color":
                max_fit=c["score"]
                best_fit=c["class"]
    return best_fit

def getArduinoPort():
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    # print (myports)
 
    arduino_port = [port for port in myports if 'Arduino Uno' in port ][0]
    return arduino_port[0]