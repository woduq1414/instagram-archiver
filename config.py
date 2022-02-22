import configparser
import os
import re
import json
import socket


# if is_local():
if socket.gethostname()[:7] == "DESKTOP":
    config = configparser.ConfigParser()
    config.read(r'D:\develop\instagram-archiver\config.ini')
    INSTA_ACCOUNT = {
        "id" : config["DEFAULT"]["INSTA_ID"],
        "pw": config["DEFAULT"]["INSTA_PW"]
    }

    CLOUDINARY_CRED = {
        "cloud_name" : config["DEFAULT"]["CLOUDINARY_CLOUD_NAME"],
        "api_key": config["DEFAULT"]["CLOUDINARY_API_KEY"],
        "api_secret": config["DEFAULT"]["CLOUDINARY_API_SECRET"]
    }

    CLOUDINARY_DIRECTORY = config["DEFAULT"]["CLOUDINARY_DIRECTORY"]


    DB_URL = config["DEFAULT"]["DB_URL"]

    TARGET_PAGE_LIST = [x for x in re.split(r'\s+', config["DEFAULT"]["TARGET_PAGE_LIST"]) if x[0] != "#"]

    print(TARGET_PAGE_LIST)

else:

    INSTA_ACCOUNT = {
        "id": os.environ.get("INSTA_ID"),
        "pw" : os.environ.get("INSTA_PW")
    }
