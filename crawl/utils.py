import requests
from io import BytesIO


import random
import string
import time

from requests.adapters import HTTPAdapter
from urllib3 import Retry


def get_media_io(url):
    s = requests.session()
    s.mount('https://', HTTPAdapter(max_retries=Retry(total=10,
                                                      backoff_factor=0.5, )))
    res = s.get(url)
    time.sleep(1.5)
    return BytesIO(res.content)




def get_random_string(size):
    chars = string.ascii_lowercase+string.ascii_uppercase+string.digits
    return ''.join(random.choice(chars) for _ in range(size))