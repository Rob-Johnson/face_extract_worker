#!/usr/bin/env python
import os
import sys
import numpy
import cv2

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
