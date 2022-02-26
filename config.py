import configparser
import os
import re
import json
import socket


# if is_local():
if socket.gethostname()[:7] == "DESKTOP":
    config = configparser.ConfigParser()
    config.read(r'D:\develop\instagram-archiver\config.ini')

    config = config["DEFAULT"]

else:
    config = os.environ

INSTA_ACCOUNT = {
    "id" : config["INSTA_ID"],
    "pw": config["INSTA_PW"]
}

CLOUDINARY_CRED = {
    "cloud_name" : config["CLOUDINARY_CLOUD_NAME"],
    "api_key": config["CLOUDINARY_API_KEY"],
    "api_secret": config["CLOUDINARY_API_SECRET"]
}

CLOUDINARY_DIRECTORY = config["CLOUDINARY_DIRECTORY"]


DB_URL = config["DATABASE_URL"]

TARGET_PAGE_LIST = [x for x in re.split(r'\s+', config["TARGET_PAGE_LIST"]) if x[0] != "#"]

print(TARGET_PAGE_LIST)

