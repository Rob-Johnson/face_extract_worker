#!/usr/bin/env python

""" Provides image manipulation methods for extracting faces from images
    using haar cascades """

import sys
import numpy
import logging

## add the facerec module to the path - it's not available as a pip install yet
sys.path.append('./facerec/py')

import Image
from facedet.detector import CascadedDetector

#configure logging to be consistent with rest of package
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
        "%(asctime)s - %(threadName)s - %(levelname)s - %(message)s")
streamhandler = logging.StreamHandler()
streamhandler.setLevel(logging.DEBUG)
streamhandler.setFormatter(formatter)
log.addHandler(streamhandler)


def resize_image(image, dimensions=(500,500)):
    """ Resize an image according to width and height values """
    log.debug('resizing image')
    return image.resize(dimensions)

def grayscale(image):
    """ Grayscales a single image """
    log.debug('grayscaling image')
    return image.convert("L")

def find_faces(image):
    """ Extracts the faces from an image, if any """
    """ Returns the regions of interest for a given face """
    log.debug('locating regions of interest')
    ar = numpy.asarray(image)
    detector = CascadedDetector(minSize=(1,1))
    return detector.detect(ar)

def crop_face(src, region):
    """ Given a source image, extract regions of interest """
    """ src is a numpy array """
    log.debug("cropping faces")

    src = numpy.asarray(src)
    new_image = Image.fromarray(src[region[1]:region[3], region[0]:region[2]])
    return new_image
