import requests
from config import INSTA_ACCOUNT
from crawl.cache import Cache
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from crawl.cache import *
import datetime
import json


def login():


    is_file_exist = True
    try:
        f = open("./login_cred.txt", 'r')
        data = json.loads(f.read())

        if datetime.datetime.now().timestamp() - data["timestamp"] >= 60 * 60 * 24:
            is_file_exist = False
        else:
            Cache().INSTA_COOKIES = data["cookies"]
            return
    except Exception as e:
        is_file_exist = False


    link = 'https://www.instagram.com/accounts/login/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'

    time = int(datetime.datetime.now().timestamp())
    response = requests.get(link)
    csrf = response.cookies['csrftoken']

    payload = {
        'username': INSTA_ACCOUNT["id"],
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{INSTA_ACCOUNT["pw"]}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    login_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf
    }

    login_response = requests.post(login_url, data=payload, headers=login_header)
    json_data = json.loads(login_response.text)

    if json_data["authenticated"]:

        print("login successful")
        cookies = login_response.cookies
        cookie_jar = cookies.get_dict()

    else:

        print("login failed ", login_response.text)
        return

    # print(cookie_jar)

    if is_file_exist is False:
        f = open("./login_cred.txt", 'w')
        f.write(json.dumps({
            "timestamp" : datetime.datetime.now().timestamp(), "cookies" : cookie_jar
        }))
        f.close()


    Cache().INSTA_COOKIES = cookie_jar


if __name__ == "__main__":
    login()
