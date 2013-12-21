#!/usr/bin/env python

import s3_tools
import unittest
import Image
import os
from collections import Iterable
from moto import mock_s3
import boto.s3

class TestS3Tools(unittest.TestCase):

    @mock_s3
    def test_upload_file(self):
        """ Tests the upload of a file using moto.
        Ideally, creation of bucket should be moved to setUp(), but 
        moto creates new s3 mock with every decorator """

        self.connection = s3_tools.connect()
        self.test_bucket = self.connection.create_bucket('mybucket')
        self.test_file_location = 'test/assets/rob.png'

        s3_tools.upload_file_to_bucket(self.test_bucket,'foo', self.test_file_location)
        key = boto.s3.key.Key(self.test_bucket)
        key.key = 'foo'
        assert key.get_contents_as_string() == open(self.test_file_location).read()

if __name__ == '__main__':
    unittest.main()
