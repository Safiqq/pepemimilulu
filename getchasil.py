import json
import os
import sys
import requests
import cv2 as cv
import numpy as np

if not os.path.exists('data'): 
    sys.exit('No data found')

if not os.path.exists('assets'): 
    os.makedirs('assets')

for root, dirs, filenames in os.walk('data/provinsi'):
    if root.count('/') == 5:
        for filename in filenames:
            with open(f'{root}/{filename}', 'r', encoding='utf-8') as f:
                img_url = json.loads(f.read())['images'][1]
                if img_url is not None:
                    response = requests.get(img_url)
                    img_data = np.frombuffer(response.content, dtype=np.uint8)
                    img = cv.imdecode(img_data, cv.IMREAD_GRAYSCALE)
                    cv.imwrite(f'assets/{filename.replace("json", "jpg")}', img)