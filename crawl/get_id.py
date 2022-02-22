import requests
import json

from requests.adapters import HTTPAdapter
from urllib3 import Retry

from crawl.cache import Cache

from db.setup import session
from db.models import *


def get_id_by_nickname(nickname):


    c = Cache()

    if nickname in c.INSTA_NICKNAME_ID_DICT:
        return c.INSTA_NICKNAME_ID_DICT[nickname]

    user_row = session.query(InstaUser).filter(InstaUser.nickname == nickname).first()
    if user_row is not None:
        return user_row.id

    s = requests.session()
    s.mount('https://', HTTPAdapter(max_retries=Retry(total=10,
                                                      backoff_factor=0.5, )))


    page_url = "https://www.instagram.com/{}/".format(nickname)
    INSTA_COOKIES = c.INSTA_COOKIES
    print(page_url)

    res = s.get(page_url, cookies=INSTA_COOKIES)
    if res.status_code != 200:
        return None

    data = json.loads(res.text.split('window._sharedData = ')[1].split(";</script>")[0])

    user_id = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["id"]

    c.INSTA_NICKNAME_ID_DICT[nickname] = user_id

    user_row = InstaUser(
        id=user_id, nickname=nickname
    )

    print(user_id)

    session.add(user_row)
    session.commit()

    return user_id
