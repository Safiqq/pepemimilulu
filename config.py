import os
from dotenv import dotenv_values

config = dotenv_values(".env")


def create_paths():
    if not os.path.exists("assets"):
        os.makedirs("assets")

    if not os.path.exists("assets/cropped"):
        os.makedirs("assets/cropped")
    
    if not os.path.exists("assets/cropped/ocr"):
        os.makedirs("assets/cropped/ocr")

    if not os.path.exists("assets/newdataset"):
        os.makedirs("assets/newdataset")

    if not os.path.exists("data"):
        os.makedirs("data")


create_paths()
