# Image Extract Worker

Created as part of final year project at the University of Sussex.

This watches RabbitMQ for messages detailing user photos, retrieves the photo, extracts the faces and posts individual faces to AmazonS3.

### Caveats:

Relies on OpenCV, which places it's python packages in the system site packages. Thus, if you're using a virtualenv, you'll have to
use --allow-system-site-packages when you create the env.
