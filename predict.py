from datetime import datetime
import json
import os
from inference_sdk import InferenceHTTPClient
import requests
import cv2
import numpy as np
from ultralytics import YOLO
from config import config

PROJECT_ID = "c.hasil"
MODEL_VERSION = 2
CROPPED_SIZE = (120, 360)

client = InferenceHTTPClient(
    api_url="http://detect.roboflow.com", api_key=config["ROBOFLOW_API_KEY"]
)


def load_data():
    tpssalahpredict_data = {}
    tpssalahupload_data = {}
    if os.path.exists("data/tpssalahpredict.json"):
        try:
            with open("data/tpssalahpredict.json", "r", encoding="utf-8") as f:
                tpssalahpredict_data = json.loads(f.read())
        except Exception as _:
            print("error:", _)
    if os.path.exists("data/tpssalahupload.json"):
        try:
            with open("data/tpssalahupload.json", "r", encoding="utf-8") as f:
                tpssalahupload_data = json.loads(f.read())
        except Exception as _:
            print("error:", _)
    return tpssalahpredict_data, tpssalahupload_data


tpssalahpredict, tpssalahupload = load_data()


def predict_online(image_url):
    results = client.infer(image_url, model_id=f"{PROJECT_ID}/{MODEL_VERSION}")
    try:
        response = requests.get(image_url, timeout=30)
        image = cv2.imdecode(
            np.frombuffer(response.content, np.uint8), cv2.IMREAD_GRAYSCALE
        )

        results = sorted(results["predictions"], key=lambda prediction: prediction["y"])
        filename = image_url.split("-2024")[0].split("/")[-1]
        tps_url = f'{config["HHCW_PPWP_URL"]}/{filename[:2]}/{filename[:4]}/{filename[:6]}/{filename[:10]}/{filename}.json'

        if len(results) == 0:
            with open("data/tpssalahupload.json", "w", encoding="utf-8") as f:
                tpssalahupload[tps_url] = len(results)
                json.dump(tpssalahupload, f, ensure_ascii=False, indent=4)
        elif len(results) != 3:
            with open("data/tpssalahpredict.json", "w", encoding="utf-8") as f:
                tpssalahpredict[tps_url] = len(results)
                json.dump(tpssalahpredict, f, ensure_ascii=False, indent=4)

        for i, prediction in enumerate(results):
            points = [[p["x"], p["y"]] for p in prediction["points"]]
            x, y, w, h = cv2.boundingRect(np.array(points, dtype=np.float32))
            cropped_image = cv2.resize(image[y : y + h, x : x + w], CROPPED_SIZE)

            cv2.imwrite(f"assets/cropped/{filename}_{i}.jpg", cropped_image)
            print(f"({datetime.now()}) {filename}_{i}.jpg")
    except Exception as _:
        print("error:", _)


def predict_offline(dir_path="assets"):
    model = YOLO("runs/segment/train/weights/best.pt")

    filenames = sorted(os.listdir(dir_path))

    results = model.predict(dir_path, conf=0.85, imgsz=640, save=True)
    for i, result in enumerate(results):
        if len(result.boxes) == 0:
            with open("data/tpssalahupload.json", "w", encoding="utf-8") as f:
                tpssalahupload[
                    f'{config["HHCW_PPWP_URL"]}/{filenames[i][:2]}/{filenames[i][:4]}/{filenames[i][:6]}/{filenames[i][:10]}/{filenames[i].replace(".jpg", "")}.json'
                ] = len(result.boxes)
                json.dump(tpssalahupload, f, ensure_ascii=False, indent=4)
        elif len(result.boxes) != 3:
            with open("data/tpssalahpredict.json", "w", encoding="utf-8") as f:
                tpssalahpredict[
                    f'{config["HHCW_PPWP_URL"]}/{filenames[i][:2]}/{filenames[i][:4]}/{filenames[i][:6]}/{filenames[i][:10]}/{filenames[i].replace(".jpg", "")}.json'
                ] = len(result.boxes)
                json.dump(tpssalahpredict, f, ensure_ascii=False, indent=4)

        for j, box in enumerate(result.boxes):
            x1, y1, x2, y2 = box.xyxy.cpu().numpy()[0]

            image = cv2.imread(f"assets/{filenames[i]}")
            cropped_image = cv2.resize(image[y1:y2, x1:x2], CROPPED_SIZE)
            cv2.imwrite(
                f'assets/cropped/{filenames[i].replace(".jpg", "")}_{j}.jpg',
                cropped_image,
            )
            print(f'({datetime.now()}) {filenames[i].replace(".jpg", "")}_{j}.jpg')



load_data()

if __name__ == "__main__":
    is_online_str = input("Predict on cloud (Y/n): ")
    if is_online_str == "" or is_online_str.lower() == "y":
        predict_online(image_url=input("Image url: "))
    else:
        predict_offline(dir_path=input("Assets directory path (assets): "))
