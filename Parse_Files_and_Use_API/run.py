#!/usr/bin/env python3
import os
import requests

txt_dir = '/data/feedback'
ip = '127.0.0.1'
endpont = 'http://{}/feedback'.format(ip)
for item in os.listdir(txt_dir):
    feedback = {}
    path = os.path.join(txt_dir, item)
    with open(path, 'r') as file:
        for i, line in enumerate(file.readlines()):
            if i == 0:
                feedback['title'] = line.strip()
            elif i == 1:
                feedback['name'] = line.strip()
            elif i == 2:
                feedback['date'] = line.strip()
            elif i == 3:
                feedback['feedback'] = line.strip()
        print(feedback)
        response = requests.post(endpont, json=feedback)
        if not response.ok:
            raise Exception("POST failed with status code {}".format(response.status_code))