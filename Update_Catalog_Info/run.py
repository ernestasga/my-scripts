#!/usr/bin/env python3
import os
import requests

text_files_dir = './supplier-data/descriptions'
descr_files = [file for file in os.listdir(text_files_dir)]

host = '127.0.0.1'
endpont = 'http://{}/fruits/'.format(host)

for file in descr_files:
    path = os.path.join(text_files_dir, file)
    info = {}
    with open(path) as txt:
        for i, line in enumerate(txt.readlines()):
            if i == 0:
                info['name'] = line.strip()
            elif i == 1:
                info['weight'] = int(line.replace('lbs', '').strip())
            elif i == 2:
                info['description'] = line.strip()
        name = file.replace('.txt', '.jpeg', )
        info['image_name'] = name
        print(info)
        response = requests.post(endpont, json=info)
        if not response.ok:
            raise Exception("POST failed with status code {}".format(response.status_code))
        txt.close()

