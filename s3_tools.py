#!/usr/bin/env python

""" Upload files to amazon s3 """
import boto
import boto.s3
import logging

log = logging.getLogger("S3_TOOLS")

def connect(aws_access_key_id=None, aws_secret_access_key=None):
    """ uses api_key and secret_key if available or
    falls back on ENV variables AWS_ACCESS_KEY_ID && AWS_SECRET_ACCESS_KEY """
    if aws_access_key_id or aws_secret_access_key is None:
        return boto.connect_s3()
    else:
        log.debug('Falling back to ENV variables $AWS_ACCESS_KEY && $AWS_SECRET_KEY')
        return boto.connect_s3(aws_access_key_id, aws_secret_access_key)

def upload_string_to_bucket(bucket, key_name, source):
    """ uploads a file to a named S3 bucket """
    log.debug('uploading to key_name %s', key_name)

    #get the key
    key = bucket.new_key(key_name)

    #set the contents of the key
    key.set_contents_from_string(source)

    #make it public
    key.set_acl('public-read')

    return key


def get_or_create_bucket(conn, bucket_name):
    """ get or create a bucket """
    log.debug('finding bucket %s if it exists', bucket_name)
    bucket = conn.lookup(bucket_name)
    if bucket is None:
        log.debug('bucket doesnt exist. creating bucket %s', bucket_name)
        bucket = conn.create_bucket(bucket_name)
        bucket.set_acl('public-read')
    return bucket

