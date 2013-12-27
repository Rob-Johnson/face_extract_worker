#!/usr/bin/env python
import os
import sys
import numpy
import cv2
import pprint
import logging

## add the facerec module to the path - it's not available as a pip install yet
sys.path.append('./facerec/py')

import Image
from facedet.detector import CascadedDetector

log = logging.getLogger("IMAGE_MANIPULATION")


def resize_image(image, dimensions=(10,10)):
    """ Resize an image according to width and height values """
    log.debug('resizing image')
    return image.resize(dimensions)

def grayscale(image):
    """ Grayscales a single image """
    log.debug('grayscaling image')
    return image.convert("L")

def extract_faces(image):
    """ Extracts the faces from an image, if any """
    """ Returns the regions of interest for a given face """
    ar = numpy.asarray(image)
    detector = CascadedDetector(minNeighbors=1)
    return detector.detect(ar)

def extract_regions_of_interest(src, regions):
    """ Given a source image, extract regions of interest """
    """ src is a numpy array """
    images = []
    for index, region in enumerate(regions):
        src = numpy.asarray(src)
        extracted = src[region[1]:region[3], region[0]:region[2]]
        images.append(extracted)
        return images
