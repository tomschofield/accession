import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

import os
import time
top_cam_index = 2
 
front_cam_index =0

top_uvc_cam_index = 1
front_uvc_cam_index = 0



# TODO. ALL OF THIS WANTS WRAPPING INTO A NEAT FUNCTION - USES UVC-UTIL TO TALK TOT HE WEBCAMS

switch_off_auto_focus_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=auto-focus=0"
switch_off_auto_focus_on_front_cam = "./uvc-util --select-by-index="+str(front_uvc_cam_index)+" --set=auto-focus=0"

set_focus_to_qr_code_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=focus-abs=20"
set_focus_to_qr_code_on_front_cam = "./uvc-util --select-by-index="+str(front_uvc_cam_index)+" --set=focus-abs=20"

set_focus_to_object_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=focus-abs=35"
set_focus_to_low_object_on_top_cam = "./uvc-util --select-by-index="+str(top_uvc_cam_index)+" --set=focus-abs=20"

set_focus_to_object_on_front_cam = "./uvc-util --select-by-index="+str(front_uvc_cam_index)+" --set=focus-abs=40"

# os.system(switch_off_auto_focus_on_top_cam)
# os.system(switch_off_auto_focus_on_front_cam)


# os.system(set_focus_to_qr_code_on_top_cam)
# os.system(set_focus_to_qr_code_on_front_cam)


top_cam = cv2.VideoCapture(top_cam_index)
front_cam = cv2.VideoCapture(front_cam_index)

front_cam.set(3,640)
front_cam.set(4,480)
# dst = f_frame * (mask_blur / 255)
# front_frame = dst.astype(np.uint8)
count = 0
while True:
    _, f_frame = front_cam.read()
    im = cv2.cvtColor(f_frame, cv2.COLOR_BGR2GRAY)
    decodedObjects = pyzbar.decode(im)
    if(len(decodedObjects)>0):
        print(decodedObjects[0].data.decode())
    # else:
    #     print("no data")
    cv2.imshow("front frame", f_frame)
    cv2.moveWindow("front frame", 955, 0) 
    cv2.namedWindow('front frame',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('front frame', 960,540)
    # print(decodedObjects)
    count = 0
