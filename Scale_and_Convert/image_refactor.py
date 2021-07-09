#!/usr/bin/env python3
from PIL import Image
import os

old_images_dir = './images'
output_path = '/opt/icons'

def refactor(img, name):
    # Rotate 90 degrees clockwise
    img = img.rotate(-90)
    # Resize to 128x128
    img = img.resize((128, 128))
    # Save to /opt/icons as jpeg
    img.convert('RGB').save(os.path.join(output_path, name+'.jpeg')) 
    
for root, dirs, files in os.walk(old_images_dir):
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    for name in files:
        if not name.startswith('.'):
            path = os.path.join(root, name)
            img = Image.open(path)
            refactor(img, name)

