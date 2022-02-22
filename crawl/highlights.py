import cloudinary.uploader
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from crawl.cache import Cache
from config import TARGET_PAGE_LIST, CLOUDINARY_DIRECTORY
from sqlalchemy import desc
import requests
import json
from db.setup import session
from crawl.get_id import get_id_by_nickname
from db.models import PostData, MediaSrc, StoryData, HighlightData
import datetime
from crawl.utils import get_media_io, get_random_string


def get_highlights(user_id=None, nickname= None):
    INSTA_COOKIES = Cache().INSTA_COOKIES

    highlight_list = session.query(HighlightData.id).filter(HighlightData.user_id == user_id).all()
    highlight_id_list = [x.id for x in highlight_list]

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    headers = {'User-Agent': user_agent, "X-IG-App-ID": "936619743392459"}

    s = requests.session()
    s.mount('https://', HTTPAdapter(max_retries=Retry(total=10,
                                                      backoff_factor=0.5, )))

    res = s.get(f"https://i.instagram.com/api/v1/highlights/{user_id}/highlights_tray/", cookies=INSTA_COOKIES,
                headers=headers
                )
    print(res.text)

    data = json.loads(res.text)
    highlights = data["tray"]

    new_highlight_row_list = []

    for highlight in highlights:
        icon_url = highlight["cover_media"]["cropped_image_version"]["url"]
        title = highlight["title"]
        id = highlight["id"]
        if id in highlight_id_list:
            continue

        media_filename = f"{nickname}_{id}_{get_random_string(6)}"
        upload_result = cloudinary.uploader.upload(get_media_io(icon_url),
                                                   public_id=f"{CLOUDINARY_DIRECTORY}/{nickname}/highlights/{media_filename}")

        new_image_url = upload_result["secure_url"]



        new_highlight_row = HighlightData(
            id=id,
            user_id=user_id,
            title=title,
            highlight_icon_url=new_image_url
        )
        new_highlight_row_list.append(new_highlight_row)
    session.add_all(new_highlight_row_list)
    session.commit()

    return highlight_id_list
