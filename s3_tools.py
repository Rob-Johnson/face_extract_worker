#!/usr/bin/env python

""" Upload files to amazon s3 """
import boto
import boto.s3

def connect(aws_access_key_id=None, aws_secret_access_key=None):
    """ uses api_key and secret_key if available or
    falls back on ENV variables AWS_ACCESS_KEY_ID && AWS_SECRET_ACCESS_KEY """
    if aws_access_key_id or aws_secret_access_key is None:
        return boto.connect_s3()
    else:
        return boto.connect_s3(aws_access_key_id, aws_secret_access_key)

def upload_file_to_bucket(bucket, key_name, source_file):
    """ uploads a file to a named S3 bucket """
    key = boto.s3.key.Key(bucket)
    key.key = key_name
    key.set_contents_from_filename(source_file)

def get_bucket(conn, bucket_name):
    """ returns a bucket from a name """
    return conn.get_bucket(bucket_name)

