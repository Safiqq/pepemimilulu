import json
import os
import requests
import cv2
import numpy as np

# from datetime import datetime
from predict import predict_online

for root, dirs, filenames in os.walk("data/provinsi"):
    if root.count("/") == 5:
        for filename in filenames:
            with open(f"{root}/{filename}", "r", encoding="utf-8") as f:
                img_url = json.loads(f.read())["images"][1]
                if img_url is not None:
                    try:
                        response = requests.get(img_url, timeout=30)
                        img_data = np.frombuffer(response.content, dtype=np.uint8)
                        img = cv2.imdecode(img_data, cv2.IMREAD_GRAYSCALE)

                        # Save image offline to predict locally
                        # cv2.imwrite(f'assets/{filename.replace("json", "jpg")}', img)
                        # print(f'({datetime.now()}) {filename.replace("json", "jpg")}')

                        # Use image url to predict on cloud
                        predict_online(
                            image_url=img_url,
                        )
                    except Exception as _:
                        print("error:", _)
