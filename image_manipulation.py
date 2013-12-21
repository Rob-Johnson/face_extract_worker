#!/usr/bin/env python
import os
import sys
import numpy
import cv2
import pprint

## add the facerec module to the path - it's not available as a pip install yet
sys.path.append('./facerec/py')

import Image
from facedet.detector import CascadedDetector


def resize_image(image, dimensions=(10,10)):
    """ Resize an image according to width and height values """
    return image.resize(dimensions)

def grayscale(image):
    """ Grayscales a single image """
    return image.convert("L")

def extract_faces(image):
    """ Extracts the faces from an image, if any """
    """ Returns the regions of interest for a given face """
    ar = numpy.asarray(image)
    detector = CascadedDetector(minNeighbors=1)
    return detector.detect(ar)

def create_image_from_region_of_interest(src, regions, output_dir="extracted"):
    """ Given a source image, extract regions of interest """
    """ src is a numpy array """
    for index, region in enumerate(regions):
        src = numpy.asarray(src)
        if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        extracted = src[region[1]:region[3], region[0]:region[2]]
        cv2.imwrite('{}/{}_{}.png'.format(output_dir,os.utime, index), extracted)
