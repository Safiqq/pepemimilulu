import json
import os
import sys
import requests

if not os.path.exists('data'): 
    sys.exit('No data found')

if not os.path.exists('assets'): 
    os.makedirs('assets')

for root, dirs, files in os.walk('data/provinsi'):
    if root.count('/') == 5:
        for file in files:
            with open(f'{root}/{file}', 'r', encoding='utf-8') as f:
                img_url = json.loads(f.read())['images'][1]
                if img_url is not None:
                    img_data = requests.get(img_url).content
                    with open(f'assets/{file.replace("json", "jpg")}', 'wb') as img:
                        img.write(img_data)