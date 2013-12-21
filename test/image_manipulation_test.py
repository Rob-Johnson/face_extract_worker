#!/usr/bin/env python

import image_manipulation
import unittest
import Image

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

if __name__ == '__main__':
    unittest.main()
