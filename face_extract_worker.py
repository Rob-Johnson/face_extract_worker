#!/usr/bin/env python
import logging
import pika
import image_manipulation 
import s3_tools
import Image
import json
import requests
import os
from StringIO import StringIO

class FaceExtractWorker:
    def __init__(self, rmq_uri):
        try:
            rmq_connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=rmq_uri))
        except Exception:
            logger.fatal("No connection to rmq available")

        self.rmq_channel = rmq_connection.channel()
        self.rmq_channel.queue_declare(queue='user_images', durable=True)
        self.s3_connection = s3_tools.connect()

    def consume(self):
        self.rmq_channel.basic_qos(prefetch_count=1)
        self.rmq_channel.basic_consume(self.extract_upload,
                queue='user_images')
        self.rmq_channel.start_consuming()

    def extract_upload(self,ch, method, properties, body):
        """ JSON Payload should look like {'uid':1234, 'picture':'http://foo.bar', 'id':'facebookimageurl'} """
        logger.info('Processing Record')
        logger.debug('Message Body: %s',body)
        body = json.loads(body)
        image_url, user, photo_id = body['picture'], body['uid'], body['id']
        normalized = image_manipulation.grayscale(
                        image_manipulation.resize_image(get_image(image_url)))


        roi = image_manipulation.extract_faces(normalized)
        logger.debug('found %d regions of interest', len(roi))
        user_bucket = s3_tools.get_or_create_bucket(self.s3_connection, '{}'.format(user))
        [s3_tools.upload_file_to_bucket(user_bucket, '{}_{}_{}'.format(user,photo_id,index), extracted) for index, extracted in enumerate(roi)]
        ch.basic_ack(delivery_tag = method.delivery_tag)

def get_image(url):
    response = requests.get(url)
    return Image.open(StringIO(response.content))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("FACE_EXTRACT_WORKER")

    location = lambda uri: uri if uri is not None else 'localhost'
    worker = FaceExtractWorker(location(os.environ.get('RABBITMQ_URI')))

    worker.consume()
