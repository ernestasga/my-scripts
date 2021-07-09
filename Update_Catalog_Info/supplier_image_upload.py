#!/usr/bin/env python3
import requests
import os

images_dir = './supplier-data/images'
host = '127.0.0.1'
endpoint = 'http://{}/upload/'.format(host)

images_to_upload = [os.path.join(images_dir, img) for img in os.listdir(images_dir) if img.endswith('.jpeg')]
for image in images_to_upload:
    with open(image, 'rb') as file:
        response = requests.post(endpoint, files={'file': file})
        if not response.ok:
            raise Exception("POST failed with status code {}".format(response.status_code))
        file.close()