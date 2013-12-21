#!/usr/bin/env python

import image_manipulation
import unittest
import Image
from collections import Iterable

class TestImageManipulation(unittest.TestCase):

    def setUp(self):
        self.image = Image.open('test/assets/rob.png')

    def test_image_resize(self):
        """ Test that the image resize function works as expecte """
        dimensions = (20, 20)
        resize_image = image_manipulation.resize_image(self.image, dimensions)
        self.assertEqual(resize_image.size, dimensions)

    def test_grayscale(self):
        """ Test conversion to grayscale """
        grayscaled = image_manipulation.grayscale(self.image)
        self.assertEqual(grayscaled.mode, "L")

    def test_extract_faces_is_iterable(self):
        """ Test extraction method returns an iterable data structure """
        faces = image_manipulation.extract_faces(self.image)
        self.assertTrue(isinstance(faces, Iterable))

if __name__ == '__main__':
    unittest.main()
