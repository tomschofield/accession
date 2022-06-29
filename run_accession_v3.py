from __future__ import print_function
import serial
import serial.tools.list_ports
import socketio
import time
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import json
import os
from os.path import abspath
from random import randrange
import colour_lookup
import datetime
from colorama import Fore, Back, Style

#my own libraries
import colour_lookup 
import datetime
#import tensor_distance
import utils
import camera_utils
import data_utils
import get_rekognition_data
import colour_utils

buffer_index = 0
# image_dir =  "/Users/ntws2/Desktop/accession/client_v2/src/assets/images/"# "./client_v2/dist/client_v2/assets/images/"
# data_dir = "/Users/ntws2/Desktop/accession/client_v2/src/assets/"

image_dir =  "/Users/ntws2/Dropbox/htdocs/accession/assets/images/"# "./client_v2/dist/client_v2/assets/images/"
data_dir = "/Users/ntws2/Dropbox/htdocs/accession/assets/"
use_network = True
use_serial = True

object_was_on_plate  = False

if (use_serial):
    print(Fore.BLUE, "SETTING UP ACCESSION LIGHTS AND MOTORS")
    port_name = utils.getArduinoPort()
    print("running on",port_name)
    s = serial.Serial(port_name, 9600, timeout=5)
else:
    print("run without arduinos")

if(use_network):

    print("connecting to server")
    sio = socketio.Client()

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

def show_cam_images_for_frame(front_frame):
         
        W = 1080.
        height, width, depth = front_frame.shape
        imgScale = W/width
        newX,newY = front_frame.shape[1]*imgScale, front_frame.shape[0]*imgScale
        small_front_frame = cv2.resize(front_frame,(int(newX),int(newY)))

        cv2.imshow("front frame", small_front_frame)
        cv2.moveWindow("front frame", 955, 0) 
        cv2.namedWindow('front frame',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('front frame', 960,540)
    
       
def getArduinoPort():
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    print (myports)
 
    arduino_port = [port for port in myports if 'Arduino Uno' in port ][0]
    return arduino_port[0]
def show_cam_images():
        front_frame = f_frame
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

def accession_object():
    dt = datetime.datetime.now()
    fname_base = str(dt.strftime("%s")) 

    global top_frame
    global f_frame
    time.sleep(1)
    _, top_frame = camera_utils.top_cam.read()
    _, f_frame = camera_utils.front_cam.read()
    global image_dir

    # check whether we can see the back cam
    back_code_occluded = camera_utils.object_is_on_plate(f_frame, 5)
    if(back_code_occluded==False):
        camera_utils.focus_cams_to_low_object()
    
    #to do
    print("Attempting to Accession_object")
    time.sleep(3)
    
    print(Fore.BLUE+"TAKING PHOTO 1")    
    _, top_frame = camera_utils.top_cam.read()
    _, f_frame = camera_utils.front_cam.read()
    cv2.imwrite(image_dir+fname_base+"_top_0.jpg", top_frame)
    cv2.imwrite(image_dir+fname_base+"_front_0.jpg", f_frame)
    if use_serial:
        s.write(str.encode('50\n'))
    time.sleep(3)
    
    print(Fore.BLUE+"TAKING PHOTO 2")
    _, top_frame = camera_utils.top_cam.read()
    _, f_frame = camera_utils.front_cam.read()
    cv2.imwrite(image_dir+fname_base+"_front_1.jpg", f_frame)
    if use_serial:
        s.write(str.encode('50\n'))
    time.sleep(3)
    
    print(Fore.BLUE+"TAKING PHOTO 3")
    _, top_frame = camera_utils.top_cam.read()
    _, f_frame = camera_utils.front_cam.read()
    cv2.imwrite(image_dir+fname_base+"_front_2.jpg", f_frame)
    if use_serial:
        s.write(str.encode('50\n'))
    time.sleep(3)
    
    print(Fore.BLUE+"TAKING PHOTO 4")
    _, top_frame = camera_utils.top_cam.read()
    _, f_frame = camera_utils.front_cam.read()
    cv2.imwrite(image_dir+fname_base+"_front_3.jpg", f_frame)
    if use_serial:
        s.write(str.encode('50\n'))
    time.sleep(3)
    new_object = get_rekognition_data.all_data_from_image_formatted(image_dir, fname_base, back_code_occluded)
    
    object_is_fit = get_object_fit(new_object)
    new_object['relevance'] = object_is_fit
    if(len(new_object['AI_keys'])>0  ):
        sio.emit('new-message',new_object)
        add_object_to_catalogue(new_object)
    else:
        print(Fore.RED+ "COULD NOT RECOGNISE OBJECT")
    print(Fore.RED+ "REMOVE YOUR OBJECT FROM ACCESSION")

def get_object_fit(new_object):
    object_fit = 0
    print("Getting object fit")
    global data_dir
    f = open(data_dir+'objects.json')  
    data = json.load(f)
    color_similarity_hits = 0
    num_colours = 0
    color_similarity = 0

    for o_colour in new_object['colours']:
        for object in data:
            for colour in object['colours']:
                score = colour_utils.get_colour_comparison(o_colour,colour)
                num_colours+=1
                if(score<10):
                    print("score",score)
                    color_similarity_hits+=1
    if (num_colours>0):
        color_similarity = color_similarity_hits/num_colours
    # print("num_colours",color_similarity)
    # if(color_similarity > 0.7):
    #     object_fit+=1
    #now lets check categories
    category_match_hits = 0
    num_categories = 0
    category_similarity = 0
    for o_category in new_object['categories']:
        for object in data:
            for category in object['categories']:
                if (o_category == category):
                    category_match_hits+=1
            num_categories+=1
    if (num_categories>0):
        category_similarity = category_match_hits/num_categories

    #now lets check classes
    key_match_hits = 0
    num_keys = 0
    key_similarity = 0
    for o_key in new_object['AI_keys']:
        for object in data:
            for key in object['AI_keys']:
                # print(key,o_key)
                if (o_key['class'] == key['class']):
                    key_match_hits+=1
            num_keys+=1
    if (num_keys>0):
        key_similarity = key_match_hits/num_keys
    return color_similarity + category_similarity + key_similarity

def add_object_to_catalogue(new_object):
    global data_dir
    f = open(data_dir+'objects.json')  
    # returns JSON object as 
    # a dictionary
    # print ("bew object",new_object)
    data = json.load(f)
    print("loaded json",len(data))
    f.close()
    data.append(new_object)
    print("udated json",len(data))
    with open(data_dir+'objects.json', 'w') as f:
        json.dump(data, f)




def run():
    # 
    global object_was_on_plate
    print(Fore.GREEN+"FRONT CAMERA IS ON:" ,camera_utils.front_cam_index)
    print(Fore.GREEN+"TOP CAMERA IS ON:",camera_utils.top_cam_index)
    mask_blur = cv2.imread('opencv_draw_mask_blur.jpg')
    frame_count = 0
    while True:
        global top_frame
        global f_frame

        _, top_frame = camera_utils.top_cam.read()
        _, f_frame = camera_utils.front_cam.read()
        # dst = f_frame * (mask_blur / 255)
        # front_frame = dst.astype(np.uint8)
        object_is_on_plate = camera_utils.object_is_on_plate(top_frame, 5)


        if (object_is_on_plate):
            # print("object on plate")
            #do this
            if(object_was_on_plate==False):
                #do nothing probably
                camera_utils.focus_cams_to_object()
                accession_object()
                camera_utils.focus_cams_to_detect()
        else:
            #do nothing probably
            if (frame_count % 20 == 0):
                print(Fore.GREEN+"PLACE AN OBJECT ON THE PLATE FOR ACCESSION")

        frame_count+=1
        object_was_on_plate  =object_is_on_plate


        show_cam_images()
        keyboard = cv2.waitKey(1)
        # print("key",keyboard)
        if keyboard == 'q' or keyboard == 27:
            print("let's exit")
            break
        elif keyboard == 'd' or keyboard == 100:
            
            camera_utils.focus_cams_to_detect()
            print("focus to detect")
            
        elif keyboard == 'o' or keyboard == 111:
            camera_utils.focus_cams_to_object()
            print("focus to object")
            
    cv2.destroyAllWindows()



camera_utils.setup_cams()

run()
