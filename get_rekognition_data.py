# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Purpose

Shows how to use the AWS SDK for Python (Boto3) with Amazon Rekognition to
recognize people, objects, and text in images.

The usage demo in this file uses images in the .media folder. If you run this code
without cloning the GitHub repository, you must first download the image files from
    https://github.com/awsdocs/aws-doc-sdk-examples/tree/master/python/example_code/rekognition/.media
"""

import logging
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import requests
import json
import datetime
import cv2
import colour_utils
from rekognition_objects import (
    RekognitionFace, RekognitionCelebrity, RekognitionLabel,
    RekognitionModerationLabel, RekognitionText, show_bounding_boxes, show_polygons)
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

logger = logging.getLogger(__name__)



class RekognitionImage:
    """
    Encapsulates an Amazon Rekognition image. This class is a thin wrapper
    around parts of the Boto3 Amazon Rekognition API.
    """
    def __init__(self, image, image_name, rekognition_client):
        """
        Initializes the image object.

        :param image: Data that defines the image, either the image bytes or
                      an Amazon S3 bucket and object key.
        :param image_name: The name of the image.
        :param rekognition_client: A Boto3 Rekognition client.
        """
        self.image = image
        self.image_name = image_name
        self.rekognition_client = rekognition_client

    @classmethod
    def from_file(cls, image_file_name, rekognition_client, image_name=None):
        """
        Creates a RekognitionImage object from a local file.

        :param image_file_name: The file name of the image. The file is opened and its
                                bytes are read.
        :param rekognition_client: A Boto3 Rekognition client.
        :param image_name: The name of the image. If this is not specified, the
                           file name is used as the image name.
        :return: The RekognitionImage object, initialized with image bytes from the
                 file.
        """
        with open(image_file_name, 'rb') as img_file:
            image = {'Bytes': img_file.read()}
        name = image_file_name if image_name is None else image_name
        return cls(image, name, rekognition_client)

    @classmethod
    def from_bucket(cls, s3_object, rekognition_client):
        """
        Creates a RekognitionImage object from an Amazon S3 object.

        :param s3_object: An Amazon S3 object that identifies the image. The image
                          is not retrieved until needed for a later call.
        :param rekognition_client: A Boto3 Rekognition client.
        :return: The RekognitionImage object, initialized with Amazon S3 object data.
        """
        image = {'S3Object': {'Bucket': s3_object.bucket_name, 'Name': s3_object.key}}
        return cls(image, s3_object.key, rekognition_client)



    
    def detect_all_data(self, max_labels):
        """
        Detects labels in the image. Labels are objects and people.

        :param max_labels: The maximum number of labels to return.
        :return: The list of labels detected in the image.
        """
        try:
            response = self.rekognition_client.detect_labels(
                Image=self.image, MaxLabels=max_labels)
            # print(response)
            # labels = [RekognitionLabel(label) for label in response['Labels']]
            all_data= []
            for label in response['Labels']:
                all_data.append(label)

            logger.info("Found %s all_data in %s.", len(all_data), self.image_name)
        except ClientError:
            logger.info("Couldn't detect all_data in %s.", self.image_name)
            raise
        else:
            return all_data

    def detect_labels(self, max_labels):
            """
            Detects labels in the image. Labels are objects and people.

            :param max_labels: The maximum number of labels to return.
            :return: The list of labels detected in the image.
            """
            try:
                response = self.rekognition_client.detect_labels(
                    Image=self.image, MaxLabels=max_labels)
                print(response)
                labels = [RekognitionLabel(label) for label in response['Labels']]
                logger.info("Found %s labels in %s.", len(labels), self.image_name)
            except ClientError:
                logger.info("Couldn't detect labels in %s.", self.image_name)
                raise
            else:
                return labels

def get_image_crop(fname,x,y,w,h):
    img = cv2.imread(fname)
    
    height, width, channels = img.shape
    # print("height",height)
    # print("width",width)
    crop_img = img[int(y*height):int(y+(y*height)+(h*height)), int(x*width):int((x*width)+(w*width))]
    cv2.imwrite("cropped.png", crop_img)
    return crop_img

def labels_from_image(fname):
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    rekognition_client = boto3.client('rekognition')
    r_image = RekognitionImage.from_file(fname, rekognition_client)
    labels = r_image.detect_labels(100)
    print(f"Found {len(labels)} labels.")
    for label in labels:
        pprint(label.to_dict())

def all_data_from_image(fname):
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    rekognition_client = boto3.client('rekognition')
    r_image = RekognitionImage.from_file(fname, rekognition_client)
    all_data = r_image.detect_all_data(100)
    print(f"Found {len(all_data)} labels.")
    return all_data


def all_data_from_image_formatted(image_dir, fname_base, back_code_occluded):
   
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    rekognition_client = boto3.client('rekognition')
    fname =""
    if(back_code_occluded):
        fname = image_dir+fname_base+"_front_0.jpg"
    else:
        fname = image_dir+fname_base+"_top_0.jpg"

    r_image = RekognitionImage.from_file(fname, rekognition_client)
    all_data = r_image.detect_all_data(100)
    # print("all_Data",all_data)
    formatted_data = {}
    if(len(all_data)>0):
        formatted_data['imageSrcTop0'] = fname_base+"_top_0.jpg"
        formatted_data['imageSrcFront0'] = fname_base+"_front_0.jpg"
        formatted_data['imageSrcFront1'] = fname_base+"_front_1.jpg"
        formatted_data['imageSrcFront2'] = fname_base+"_front_2.jpg"
        formatted_data['imageSrcFront3'] = fname_base+"_front_3.jpg"
        formatted_data['title'] = all_data[0]['Name']
        if(back_code_occluded):
            formatted_data['imageSrcFocus']=formatted_data['imageSrcTop0'] = fname_base+"_front_0.jpg"
        else:
            formatted_data['imageSrcFocus']=formatted_data['imageSrcTop0'] = fname_base+"_top_0.jpg"
        
        
        formatted_data['accession_time'] = fname_base
        formatted_data['dimensions']= {
            "width": 1,
            "length": 1,
            "height": 1
        }
        # print("fname","images/"+fname)
        formatted_data['categories']=[]
        image_crop = get_image_crop(fname, 0.2,0.2,0.6,0.6)
        formatted_data['colours']=colour_utils.get_hex_palette("cropped.png")
        formatted_data['AI_keys'] = []
        for data in all_data:
            # print (data)
            if (data['Confidence']> 80 and data['Name']!="QR Code"):
                obj = {
                    "class":data['Name'],
                    "score":data['Confidence'],
                }
                formatted_data['AI_keys'].append(obj)
                if (len(data['Parents'])>0):
                    # print("has valid parents")
                    for parent in data['Parents']:
                        # if (parent['Name'] in formatted_data['categories'] == False):
                        formatted_data['categories'].append(parent['Name'])

        
        # print(f"Found {len(all_data)} labels.")
    else:
        print ("COULDN'T GET OBJECT DATA")
    return formatted_data



if __name__ == '__main__':
    # usage_demo()
    print(all_data_from_image_formatted("./images/1655202584_front_1.jpg"))
