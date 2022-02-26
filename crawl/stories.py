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
from db.models import PostData, MediaSrc, StoryData
import datetime
from crawl.utils import get_media_io, get_random_string


def get_stories(user_id=None, nickname=None, highlight_id=None):
    INSTA_COOKIES = Cache().INSTA_COOKIES

    s = requests.session()
    s.mount('https://', HTTPAdapter(max_retries=Retry(total=10,
                backoff_factor=0.5,)))
    new_story_row_list = []

    print(nickname)



    print(user_id)

    story_list = session.query(StoryData.id).filter(StoryData.user_id == user_id).all()
    story_id_list = [x.id for x in story_list]

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    headers = {'User-Agent': user_agent, "X-IG-App-ID": "936619743392459"}

    if highlight_id is None:
        reel_id = user_id
    else:
        reel_id = highlight_id

    res = s.get("https://i.instagram.com/api/v1/feed/reels_media/?reel_ids=" + reel_id, cookies=INSTA_COOKIES,
                headers=headers
                )

    data = json.loads(res.text)

    try:
        stories = data["reels"][reel_id]["items"]
    except:
        return

    for story in stories:

        timestamp = story["taken_at"]
        id = story["id"]

        if id in story_id_list:
            continue

        image_url = story["image_versions2"]["candidates"][0]["url"]

        media_filename = f"{nickname}_{id}_{get_random_string(6)}"
        upload_result = cloudinary.uploader.upload(get_media_io(image_url),
                                                   public_id=f"{CLOUDINARY_DIRECTORY}/{nickname}/stories/{media_filename}")

        new_image_url = upload_result["secure_url"]

        if story["media_type"] == 2:  # video
            type = "video"
            video_url = story["video_versions"][0]["url"]
            media_filename = f"{nickname}_{id}_{get_random_string(6)}"
            upload_result = cloudinary.uploader.upload_large(get_media_io(video_url), resource_type="video",
                                                             public_id=f"{CLOUDINARY_DIRECTORY}/{nickname}/stories/{media_filename}.mp4")
            new_video_url = upload_result["secure_url"]
        else:
            type = "image"
            new_video_url = None

        new_story_row = StoryData(
            id=id,
            user_id=user_id,
            type=type,
            image_url=new_image_url,
            video_url=new_video_url,
            highlight_id=highlight_id,
            upload_datetime=datetime.datetime.fromtimestamp(timestamp),
            crawl_datetime=datetime.datetime.now()
        )

        new_story_row_list.append(new_story_row)

        print(timestamp, id, new_image_url, new_video_url)

    session.add_all(new_story_row_list)
    session.commit()
