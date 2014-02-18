#!/usr/bin/env python
import logging
import pika
import image_manipulation 
import s3_tools
import Image
import json
import requests
import os
import cStringIO

class FaceExtractWorker:
    def __init__(self, rmq_uri):
        try:
            rmq_connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=rmq_uri))
        except Exception:
            logger.fatal("No connection to rmq available")

        self.rmq_channel = rmq_connection.channel()
        self.result_queue = self.rmq_channel.queue_declare(queue="user_images", durable=True)

        self.queue_name = self.result_queue.method.queue
        self.s3_connection = s3_tools.connect()

    def consume(self):
        """ Bind to the worker queue """
        self.rmq_channel.basic_consume(self.extract_upload,
                queue=self.queue_name)
        self.rmq_channel.start_consuming()

    def extract_upload(self,ch, method, properties, body):
        """ JSON Payload should look like {'user_id':1234, 'picture':'http://foo.bar', 'id':'facebook_image_id'} """

        logger.info('Processing Record')
        logger.debug('Message Body: %s', body)
        body = json.loads(body)
        image_url, user, photo_id = body['source'], body['user_id'], body['id']
        normalized = image_manipulation.grayscale(
                        image_manipulation.resize_image(get_image(image_url)))


        #find roi's
        roi = image_manipulation.find_faces(normalized)
        logger.debug('found %d regions of interest', len(roi))

        #crop images to get faces
        cropped = []
        for face in roi:
            image_buffer= cStringIO.StringIO()
            cropped_image = image_manipulation.crop_face(normalized, face)
            cropped_image.save(image_buffer, format='JPEG')
            cropped.append(image_buffer)

        #find the bucket to upload to
        user_bucket = s3_tools.get_or_create_bucket(self.s3_connection, 'robj_{}_unconfirmed'.format(user))

        #upload each cropped image to s3
        for index, extracted in enumerate(cropped):
            s3_tools.upload_string_to_bucket(user_bucket, '{}_{}_{}'.format(user,photo_id,index), extracted.getvalue())

        #we're done, so acknowledge the message
        ch.basic_ack(delivery_tag = method.delivery_tag)

def get_image(url):
    response = requests.get(url)
    return Image.open(cStringIO.StringIO(response.content))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("FACE_EXTRACT_WORKER")

    location = lambda uri: uri if uri is not None else 'localhost'
    worker = FaceExtractWorker(location(os.environ.get('RABBITMQ_URI')))

    worker.consume()
