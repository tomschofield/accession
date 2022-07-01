import os
import time
import cv2
import numpy as np
from os.path import abspath
from colorama import Fore, Back, Style
import pyzbar.pyzbar as pyzbar
buffer_index = 0


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
                            #print("found top camera on ", x)
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
        
def init_camera_focus():
    switch_off_auto_focus_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=auto-focus=0"
    switch_off_auto_focus_on_front_cam = "./uvc-util --select-by-index="+str(front_uvc_cam_index)+" --set=auto-focus=0"

    set_focus_to_qr_code_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=focus-abs=20"
    set_focus_to_qr_code_on_front_cam = "./uvc-util --select-by-index="+str(front_uvc_cam_index)+" --set=focus-abs=20"

    # set_focus_to_object_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=focus-abs=35"
    # set_focus_to_low_object_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=focus-abs=20"

    # set_focus_to_object_on_front_cam = "./uvc-util --select-by-index="+str(front_uvc_cam_index)+" --set=focus-abs=40"

    os.system(switch_off_auto_focus_on_top_cam)
    os.system(switch_off_auto_focus_on_front_cam)


    os.system(set_focus_to_qr_code_on_top_cam)
    os.system(set_focus_to_qr_code_on_front_cam)

def focus_cams_to_detect():
    #todo autodetect



    # TODO. ALL OF THIS WANTS WRAPPING INTO A NEAT FUNCTION - USES UVC-UTIL TO TALK TOT HE WEBCAMS

    # switch_off_auto_focus_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=auto-focus=0"
    # switch_off_auto_focus_on_front_cam = "./uvc-util --select-by-index="+str(front_uvc_cam_index)+" --set=auto-focus=0"

    set_focus_to_qr_code_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=focus-abs=20"
    set_focus_to_qr_code_on_front_cam = "./uvc-util --select-by-index="+str(front_uvc_cam_index)+" --set=focus-abs=20"


    # os.system(switch_off_auto_focus_on_top_cam)
    # os.system(switch_off_auto_focus_on_front_cam)


    os.system(set_focus_to_qr_code_on_top_cam)
    os.system(set_focus_to_qr_code_on_front_cam)

def focus_cams_to_object():
    # print("focusing cams to object on top ",top_uvc_cam_index)
    # print("focusing cams to object on front",front_uvc_cam_index)
    set_focus_to_object_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=focus-abs=35"
    # set_focus_to_low_object_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=focus-abs=20"

    set_focus_to_object_on_front_cam = "./uvc-util --select-by-index="+str(front_uvc_cam_index)+" --set=focus-abs=40"
    os.system(set_focus_to_object_on_top_cam)
    os.system(set_focus_to_object_on_front_cam)
    # if (is_top_cam):
    #     os.system(set_focus_to_low_object_on_top_cam)
    # else:
    #     os.system(set_focus_to_low_object_on_front_cam)

def focus_cams_to_low_object():
    # print("focusing cams to object on top ",top_uvc_cam_index)
    # print("focusing cams to object on front",front_uvc_cam_index)
    set_focus_to_object_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=focus-abs=35"
    set_focus_to_low_object_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=focus-abs=20"

    set_focus_to_object_on_front_cam = "./uvc-util --select-by-index="+str(front_uvc_cam_index)+" --set=focus-abs=40"
    os.system(set_focus_to_low_object_on_top_cam)
    os.system(set_focus_to_object_on_front_cam)
    # if (is_top_cam):
    #     os.system(set_focus_to_low_object_on_top_cam)
    # else:
    #     os.system(set_focus_to_low_object_on_front_cam)

def get_top_cam_index():
    # print("To do")
    cam = cv2.VideoCapture(top_cam_index)
    
    top_cam.set(3,640)
    top_cam.set(4,480)

    front_cam.set(3,640)
    front_cam.set(4,480)

    focus_cams_to_detect()


def object_is_on_plate(frame, buffer_size):
    global buffer_index
    decodedObjects = pyzbar.decode(frame)
    num_decoded_objects = len(decodedObjects)
    # print(buffer_index)
    
    if(len(objects_on_plate_buffer)<buffer_size):
        objects_on_plate_buffer.append(num_decoded_objects)
    else:
        # print("Writing to ",buffer_index)
        objects_on_plate_buffer[buffer_index] = num_decoded_objects
        buffer_index+=1
        if(buffer_index>=len(objects_on_plate_buffer)):
            buffer_index=0

    total = 0
    for item in objects_on_plate_buffer:
        total+=item
    total /= len(objects_on_plate_buffer)
    if (total<0.5):
        return True
    else:
        return False

def qr_code_seen_on_cam(frame):
   
    decodedObjects = pyzbar.decode(frame)
    num_decoded_objects = len(decodedObjects)
    # print(buffer_index)

    if(len(objects_on_plate_buffer)<buffer_size):
        objects_on_plate_buffer.append(num_decoded_objects)
    else:
        # print("Writing to ",buffer_index)
        objects_on_plate_buffer[buffer_index] = num_decoded_objects
        buffer_index+=1
        if(buffer_index>=len(objects_on_plate_buffer)):
            buffer_index=0

    total = 0
    for item in objects_on_plate_buffer:
        total+=item
    total /= len(objects_on_plate_buffer)
    if (total>0.5):
        return True
    else:
        return False

def setup_cams():
    global objects_on_plate_buffer
    # global buffer_index
    global top_cam_index
    global front_cam_index
    global top_uvc_cam_index
    global front_uvc_cam_index
    global top_cam
    global front_cam

    objects_on_plate_buffer = []
    buffer_index = 0
    top_uvc_cam_index = 0
    front_uvc_cam_index = 1
    init_camera_focus()

    top_cam_index = get_cam_index_for("accession")
    init_camera_focus()
    front_cam_index =get_cam_index_for("back_plate")
    print(top_cam_index,"top_cam_index")
    print(front_cam_index,"front_cam_index")

    
    init_camera_focus()
    time.sleep(2)
    
    front_uvc_cam_index= get_uvc_index_for(front_cam_index, "back_plate")
    init_camera_focus()
    top_uvc_cam_index = get_uvc_index_for(top_cam_index, "accession")
    
    print("top_uvc_cam_index",top_uvc_cam_index)
    print("front_uvc_cam_index",front_uvc_cam_index)
    init_camera_focus()

    top_cam = cv2.VideoCapture(top_cam_index)
    front_cam = cv2.VideoCapture(front_cam_index)

    
    
    top_cam.set(3,640)
    top_cam.set(4,480)

    front_cam.set(3,640)
    front_cam.set(4,480)

    focus_cams_to_detect()

def show_cam_images(f_frame,):
    try:
        front_frame = f_frame
        # if front_frame:
        W = 1080.
        height, width, depth = front_frame.shape
        imgScale = W/width
        newX,newY = front_frame.shape[1]*imgScale, front_frame.shape[0]*imgScale
        small_front_frame = cv2.resize(front_frame,(int(newX),int(newY)))

        cv2.imshow("front frame", small_front_frame)
        cv2.moveWindow("front frame", 955, 0) 
        cv2.namedWindow('front frame',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('front frame', 960,540)

        # small_top_frame = cv2.resize(top_frame,(int(newX),int(newY)))
        # cv2.imshow("top frame", small_top_frame)
        # cv2.moveWindow("top frame", 955, 540) 
        # cv2.namedWindow('top frame',cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('top frame', 960,540)
        keyboard = cv2.waitKey(1)
        # print("key",keyboard)
        if keyboard == 'q' or keyboard == 27:
            print("let's exit")
            # break
        elif keyboard == 'd' or keyboard == 100:
            
            camera_utils.focus_cams_to_detect()
            print("focus to detect")
            
        elif keyboard == 'o' or keyboard == 111:
            camera_utils.focus_cams_to_object()
            print("focus to object")
    except AttributeError:
        print("shape not found")

def get_uvc_index_for(cam_index, qr_code):
    tempCap = cv2.VideoCapture(cam_index)
    tempCap.set(3,640)
    tempCap.set(4,480)
    x = 0
    max_cam_indices = 2
    

    while x < max_cam_indices:
        print(Fore.GREEN+" turnong off autofocus on ",x)
        os.system("./uvc-util --select-by-index="+str(x)+" --set=auto-focus=0")

        has_expected_qr = False
        has_qr_on_long_focus = False
        print(Fore.GREEN+" Focusing camera to QR code on index ",x)
        #focus to QR 
        set_focus_to_qr_code_on_top_cam = "./uvc-util --select-by-index="+str(x)+" --set=focus-abs=20"
        os.system(set_focus_to_qr_code_on_top_cam)
        time.sleep(1)
        #is there a QR?
        _, frame = tempCap.read()
        show_cam_images(frame)
        decodedObjects = pyzbar.decode(frame)
        if len(decodedObjects)>0:
            for obj in decodedObjects:
                # print("obj.data",x,obj.data.decode("utf-8"))
                if obj.data.decode("utf-8")  == qr_code:
                    print("found QR code on ", x)
                    has_expected_qr = True
        #focus very short 
        time.sleep(1)
        print("Focusing camera to infinity  on index ",x)
        set_focus_to_infinite = "./uvc-util --select-by-index="+str(x)+" --set=focus-abs=2000"
        os.system(set_focus_to_infinite)
        #is there a QR?
        time.sleep(1)
        _, frame = tempCap.read()
        show_cam_images(frame)
        decodedObjects = pyzbar.decode(frame)
        if len(decodedObjects)>0:
            for obj in decodedObjects:
                # print("obj.data",x,obj.data.decode("utf-8"))
                if obj.data.decode("utf-8")  == qr_code:
                    print("found qr code while long focusing on ", x)
                    has_qr_on_long_focus = True
        
        time.sleep(1)
        
        if(has_expected_qr and has_qr_on_long_focus==False):
            print("found uvc index",x)
            return x
        
        x+=1
    # tempCap.release()

def get_cam_index_for(qr_code):
    # print("looking for cam showing",qr_code)
     
    num_tries = 0
    max_tries = 10
    max_cam_indices = 3
    x=0
    caps = []
    while x < max_cam_indices:
        tempCap = cv2.VideoCapture(x)
        tempCap.set(3,640)
        tempCap.set(4,480)
        caps.append(tempCap)
        x+=1
 
    x=0
    
    for cap in caps:
        print("camera number",x)
        while num_tries <max_tries:
            _, frame = cap.read()
            NoneType = type(None)
            if(isinstance(frame, NoneType) ==False):
                print(len(frame))
                decodedObjects = pyzbar.decode(frame)
                if len(decodedObjects)>0:
                    for obj in decodedObjects:
                        # print("obj.data",x,obj.data.decode("utf-8"))
                        if obj.data.decode("utf-8")  == qr_code:
                            print("found front camera on ", x)
                            return x
            else:
                print("camera turned of at index ",x)    
           
            num_tries+=1
        x+=1
        num_tries=0
        # cap.release()
        
    return -1
