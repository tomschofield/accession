from __future__ import print_function
import serial
import serial.tools.list_ports
import socketio
import time
# https://python-socketio.readthedocs.io/en/latest/client.html
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import json
 
import json
import os
from os.path import abspath
 
# from ibm_watson import VisualRecognitionV3, ApiException
from random import randrange

import colour_lookup
 
import datetime
import tensor_distance

 
from colorama import Fore, Back, Style

image_dir = "./client_v2/dist/client_v2/assets/images/"
data_dir = "./client_v2/dist/client_v2/assets/"


 


existing_data = {}
with open(data_dir+'objects.json') as json_file:
        existing_data = json.load(json_file)
 
acceptance_thresh=0.5
# standard Python
sio = socketio.Client()
 
# 
use_serial = True  
 
 
 
# visual_recognition = VisualRecognitionV3(
#     '2018-03-19',
#     iam_apikey='PUT YOUR IBM WATSON KEY HERE')

 
def getTopCamIndex(front_cam_index):
    print("finding top cam")
     
    num_tries = 0
    max_tries = 20
    max_cam_indices = 5
    x=0
    while x < max_cam_indices:
        if x != front_cam_index:
            print("checking camera ",x)
            cap = cv2.VideoCapture(x)
            while num_tries <max_tries:
                _, frame = cap.read()
                decodedObjects = pyzbar.decode(frame)
                if len(decodedObjects)>0:
                    for obj in decodedObjects:
                        print("obj.data",x,obj.data.decode("utf-8"))
                        if obj.data.decode("utf-8")  == "_accession_":
                            print("found top camera on ", x)
                            return x
                num_tries+=1
            cap.release()
        x+=1
         
 
def getFrontCamIndex():
    print("finding front cam")
     
    num_tries = 0
    max_tries = 20
    max_cam_indices = 5
    x=0
    while x < max_cam_indices:
        print("checking camera ",x)
        cap = cv2.VideoCapture(x)
        while num_tries <max_tries:
            _, frame = cap.read()
            decodedObjects = pyzbar.decode(frame)
            if len(decodedObjects)>0:
                for obj in decodedObjects:
                    print("obj.data",x,obj.data.decode("utf-8"))
                    if obj.data.decode("utf-8")  == "accession":
                        print("found front camera on ", x)
                        return x
            num_tries+=1
        x+=1
        cap.release()
 
 
def getCamIndexFor(qr_code):
    print("looking for cam showing",qr_code)
     
    num_tries = 0
    max_tries = 20
    max_cam_indices = 5
    x=0
    cap = []
    while x < max_cam_indices:
        cap.append(cv2.VideoCapture(x))
        x+=1
 
    x=0
    cap ={}
    while x < max_cam_indices:
        print("checking camera ",x)
        # cap[x] = cv2.VideoCapture(x)
        if x==0:
            cap = cv2.VideoCapture(0)
        elif x==1:
            cap = cv2.VideoCapture(1)
        elif x==2:
            cap = cv2.VideoCapture(2)
        elif x==3:
            cap = cv2.VideoCapture(3)
        elif x==4:
            cap = cv2.VideoCapture(4)
 
        while num_tries <max_tries:
            _, frame = cap.read()
            decodedObjects = pyzbar.decode(frame)
            if len(decodedObjects)>0:
                for obj in decodedObjects:
                    print("obj.data",x,obj.data.decode("utf-8"))
                    if obj.data.decode("utf-8")  == qr_code:
                        print("found front camera on ", x)
                        return x
            num_tries+=1
        x+=1

 
 
def getArduinoPort():
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    print (myports)
 
    arduino_port = [port for port in myports if 'Arduino Uno' in port ][0]
    return arduino_port[0]
 
@sio.event
def message(data):
    print('I received a message!')
 
@sio.event
def connect():
    print("I'm connected!")
 
@sio.event
def disconnect():
    print("I'm disconnected!")
 
 
sio.connect('http://localhost:3000')
 
def classify(image_file):
    # print("classifying",image_file)
    path = abspath(image_file)
    try:
        with open(path, 'rb') as images_file:
            results = visual_recognition.classify(
                images_file=images_file,
                threshold='0.1',
                classifier_ids=['default']).get_result()
        # print(json.dumps(results, indent=2))
        return results
    except ApiException as ex:
        print(ex)
 
 
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
 
 
def makeObject(fname_base, use_top_cam):
    global acceptance_thresh
    # results = {}
    # if use_top_cam:
    #     print(Fore.MAGENTA+"USING TOP CAMERA IMAGE FOR CLASSIFICATION")
    #     results = classify(image_dir+fname_base+"_top_0.jpg")
    # else:
    #     print(Fore.CYAN+"USING FRONT CAMERA IMAGE FOR CLASSIFICATION")
    #     results = classify(image_dir+fname_base+"_front_2.jpg")
 
    # new_object={}
 
    # new_object["imageSrcFront0"]=fname_base+"_front_0.jpg"
    # new_object["imageSrcFront1"]=fname_base+"_front_1.jpg"
    # new_object["imageSrcFront2"]=fname_base+"_front_2.jpg"
    # new_object["imageSrcFront3"]=fname_base+"_front_3.jpg"
 
    # new_object["imageSrcTop0"]=fname_base+"_top_0.jpg"
 
 
 
    # new_object["dimensions"]={"width": 1, "length":1, "height":1}
    # new_object["AI_keys"]=results['images'][0]['classifiers'][0]['classes']
    # new_object["colours"]=getColours( new_object["AI_keys"])
    # new_object["accession_time"]=str(dt.strftime("%s")) 
    # new_object["categories"]=get_categories_from_classes(new_object["AI_keys"])
    # new_object["title"]=get_best_fitting_class(new_object["AI_keys"])

    # index = randrange(len(existing_data['objects'])-1)

    # seed = existing_data['objects'][index]
 
    # print(Fore.YELLOW+"ASSESSING OBJECT AGAINST COLLECTIONS ITEM",seed["title"],"FOR ACCESSION. ACCEPTANCE THRESHOLD IS",acceptance_thresh,"\nDO NOT REMOVE YOUR ITEM.\n THIS WILL TAKE A COUPLE OF MINUTES")
    # new_object["similarity"]=str(tensor_distance.test_similiarity(classes_to_string(new_object["AI_keys"]), classes_to_string(seed["AI_keys"])))


    # acceptance_thresh+=0.005
 
    # if float(new_object["similarity"])>acceptance_thresh:
 
    #     addObject(new_object, data_dir)
    #     sio.emit('new-message',new_object)
    #     print(Fore.GREEN+"OBJECT WAS ACCEPTED. IT HAD A SIMILARITY SCORE OF:", new_object["similarity"])
    # else:
    #     addRefusedObject(new_object, data_dir)
    #     print(Fore.RED+"OBJECT WAS NOT ACCEPTED. IT HAD A SIMILARITY SCORE OF:", new_object["similarity"])
    #     # print(ascii_no_entry)
 
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
 
def getColours(watson_results):
    colours = []
    try:
        # print("watson_results.images",watson_results.images)
        # print("watson_results.images[0]",watson_results.images[0])
        # print('watson_results.images[0].classifiers[0]',watson_results.images[0].classifiers[0])
        # print("watson_results.images[0].classifiers[0].classes",watson_results.images[0].classifiers[0].classes)
        for ai_class in watson_results:
             
            exploded= ai_class['class'].split()
            # print ("exploded",exploded)
            if exploded[len(exploded)-1]=="color":
                colour_name = ""
                for x in exploded[:-1]:
                    colour_name+=x+" "
                colour_obj={}
                colour_obj["colour_name"]=colour_name.strip()
                colour_obj["hex"]=colour_lookup.lookupColour(colour_name.strip())
                     
                colours.append(colour_obj)
        return colours
    except:
        empty = []
        return empty
 




print(Fore.GREEN+ "SETTING UP CAMERAS")


# I'M HAVING TO SET THESE MANUALLY CURRETLY THANKS TO PROBLEMS WITH THE QR  CODE DETEXTION
top_cam_index = 0
 
front_cam_index =2

top_uvc_cam_index = 0
front_uvc_cam_index = 1



# TODO. ALL OF THIS WANTS WRAPPING INTO A NEAT FUNCTION - USES UVC-UTIL TO TALK TOT HE WEBCAMS

switch_off_auto_focus_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=auto-focus=0"
switch_off_auto_focus_on_front_cam = "./uvc-util --select-by-index="+str(front_uvc_cam_index)+" --set=auto-focus=0"

set_focus_to_qr_code_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=focus-abs=20"
set_focus_to_qr_code_on_front_cam = "./uvc-util --select-by-index="+str(front_uvc_cam_index)+" --set=focus-abs=20"

set_focus_to_object_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=focus-abs=35"
set_focus_to_low_object_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=focus-abs=20"

set_focus_to_object_on_front_cam = "./uvc-util --select-by-index="+str(front_uvc_cam_index)+" --set=focus-abs=40"

os.system(switch_off_auto_focus_on_top_cam)
os.system(switch_off_auto_focus_on_front_cam)


os.system(set_focus_to_qr_code_on_top_cam)
os.system(set_focus_to_qr_code_on_front_cam)


top_cam = cv2.VideoCapture(top_cam_index)
front_cam = cv2.VideoCapture(front_cam_index)
 
print(Fore.GREEN+"FRONT CAMERA IS ON:" ,front_cam_index)
print(Fore.GREEN+"TOP CAMERA IS ON:",top_cam_index)
 
 
font = cv2.FONT_HERSHEY_PLAIN
 
 
 # CIRCULAR BUFFER FOR SMOOTHING OUT SOME OF THE CODE FINDING NONESENESE
found_objects_buffer = []
count = 0
while count <3:
    found_objects_buffer.append(1)
    count+=1
count = 0
messageSent =False
 
if use_serial:
    print(Fore.BLUE, "SETTING UP ACCESSION LIGHTS AND MOTORS")
    s = serial.Serial(getArduinoPort(), 9600, timeout=5)
else:
    print("run without arduinos")
 
mask = cv2.imread('mask.png')
 
messageCounter = 0
 
found_object = False
p_found_object = False
frame_count = 0
fname_base = ""
 
mask_blur = cv2.imread('opencv_draw_mask_blur.jpg')
use_top_cam = False
 
while True:
    _, top_frame = top_cam.read()
    _, f_frame = front_cam.read()
    dst = f_frame * (mask_blur / 255)
    front_frame = dst.astype(np.uint8)
 
    # every 15 frames if we are not processing an object
    if frame_count >= 15 and found_object==False:
        frame_count=0
        print("looking for object")
        decodedObjects = pyzbar.decode(front_frame)
 
        found_objects_buffer[count] = len(decodedObjects)
 
        # lets take a mean of the buffer and see we have an object or not
        average = 0
        for fob in found_objects_buffer:
            average+=fob
        average/=len(found_objects_buffer)
        count+=1
        if(count)>=len(found_objects_buffer):
            count=0
 
        # print("num_objects",len(decodedObjects), "smoothed num_objects", average)
        if average == 0:
            print(Fore.CYAN+"OBJECT FOUND")
            dt = datetime.datetime.now()
            fname_base = str(dt.strftime("%s")) 
            found_object = True

            
            if messageCounter ==4:
                print(Fore.RED+ "REMOVE YOUR OBJECT FROM ACCESSION")
                os.system(set_focus_to_qr_code_on_top_cam)
                os.system(set_focus_to_qr_code_on_front_cam)
                found_object = False

        elif average>0 and average <0.5:
            print(Fore.CYAN+"POSSIBLE OBJECT FOUND")
            os.system(set_focus_to_qr_code_on_top_cam)
            os.system(set_focus_to_qr_code_on_front_cam)
        else:
            print(Fore.GREEN+"PLACE AN OBJECT ON THE PLATE FOR ACCESSION")
            os.system(set_focus_to_qr_code_on_top_cam)
            os.system(set_focus_to_qr_code_on_front_cam)
            messageCounter = 0
 
    if found_object == True and messageCounter < 5:


        # do we have something low down and exposing the rear qr code
        decodedObjects = pyzbar.decode(front_frame)    
        if len(decodedObjects) > 0:
            use_top_cam = True

        if use_top_cam:
            os.system(set_focus_to_low_object_on_top_cam)
        else:
            os.system(set_focus_to_object_on_top_cam)
        os.system(set_focus_to_object_on_front_cam)
        # _, top_frame = top_cam.read()
        # _, f_frame = front_cam.read()
        # lets check one last time it's not a false alarm
        decodedObjects = pyzbar.decode(top_frame)    
        if len(decodedObjects) > 0:
            found_object = False
            messageCounter=4
            print(Fore.RED+"FALSE ALARM, NO OBJECT FOUND")
        
        if messageCounter== 0:
            print(Fore.BLUE+"TAKING PHOTO 1")
            if len(decodedObjects) > 0:
                found_object = False
                messageCounter=4
                print(Fore.RED+"FALSE ALARM, NO OBJECT FOUND")

            else:             
                cv2.imwrite(image_dir+fname_base+"_top_0.jpg", top_frame)
                cv2.imwrite(image_dir+fname_base+"_front_0.jpg", front_frame)
                if use_serial:
                    s.write(str.encode('50\n'))
                time.sleep(3)
                messageCounter+=1
        elif messageCounter== 1:
            print(Fore.BLUE+"TAKING PHOTO 2")
            decodedObjects = pyzbar.decode(top_frame)    
            if len(decodedObjects) > 0:
                found_object = False
                messageCounter=4
                print(Fore.RED+"FALSE ALARM, NO OBJECT FOUND")

            else:
                cv2.imwrite(image_dir+fname_base+"_front_1.jpg", front_frame)
                if use_serial:
                    s.write(str.encode('100\n'))
                time.sleep(3)
                messageCounter+=1
        elif messageCounter== 2:
            print(Fore.BLUE+"TAKING PHOTO 3")

            decodedObjects = pyzbar.decode(top_frame)    
            if len(decodedObjects) > 0:
                found_object = False
                messageCounter=4
                print(Fore.RED+"FALSE ALARM, NO OBJECT FOUND")
            else:
                cv2.imwrite(image_dir+fname_base+"_front_2.jpg", front_frame)
                if use_serial:
                    s.write(str.encode('150!\n'))
                time.sleep(3)
                messageCounter+=1
        elif messageCounter== 3:
            print(Fore.BLUE+"TAKING PHOTO 4")
            cv2.imwrite(image_dir+fname_base+"_front_3.jpg", front_frame)
            if use_serial:
                s.write(str.encode('200!\n'))
            time.sleep(3)
            decodedObjects = pyzbar.decode(top_frame)    
            if len(decodedObjects) > 0:
                found_object = False
                messageCounter=4
                print(Fore.RED+"FALSE ALARM, NO OBJECT FOUND")
            else:
                makeObject(fname_base, use_top_cam)
 
            messageCounter+=1
            os.system(set_focus_to_qr_code_on_top_cam)
            os.system(set_focus_to_qr_code_on_front_cam)
             
            found_object = False
            use_top_cam = False
 
    frame_count+=1
 

    W = 1080.
    height, width, depth = front_frame.shape
    imgScale = W/width
    newX,newY = front_frame.shape[1]*imgScale, front_frame.shape[0]*imgScale
    small_front_frame = cv2.resize(front_frame,(int(newX),int(newY)))
 
    cv2.imshow("front frame", small_front_frame)
    cv2.moveWindow("front frame", 955, 0) 
    cv2.namedWindow('front frame',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('front frame', 960,540)
 
    small_top_frame = cv2.resize(top_frame,(int(newX),int(newY)))
    cv2.imshow("top frame", small_top_frame)
    cv2.moveWindow("top frame", 955, 540) 
    cv2.namedWindow('top frame',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('top frame', 960,540)

    keyboard = cv2.waitKey(1)
    if keyboard == 'q' or keyboard == 27:
        print("let's exit")
        break
        

cv2.destroyAllWindows()
exit()
 