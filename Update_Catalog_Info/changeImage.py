#!/usr/bin/env python3
from PIL import Image
import os

images_dir = './supplier-data/images'

def refactor(img, name):
    img = img.convert('RGB')
    img = img.resize((600, 400))
    name, ext = name.split('.', 1)
    img.save(os.path.join(images_dir, name+'.jpeg'))

for root, dirs, files in os.walk(images_dir):
    for name in files:
        if name.endswith('.tiff'):
            path = os.path.join(root, name)
            img = Image.open(path)
            refactor(img, name)