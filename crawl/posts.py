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
from db.models import PostData, MediaSrc
import datetime
from crawl.utils import get_media_io, get_random_string


def get_posts(user_id = None, nickname = None):
    INSTA_COOKIES = Cache().INSTA_COOKIES

    s = requests.session()
    s.mount('https://', HTTPAdapter(max_retries=Retry(total=10,
                                                      backoff_factor=0.5, )))





    end_cursor = ""

    post_list = session.query(PostData.id).filter(PostData.user_id == user_id).all()
    post_id_list = [x.id for x in post_list]



    while True:

        res = s.get(
            'https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables={"id":"' + user_id + '","first":20,"after":"' + end_cursor + '"}',
            cookies=INSTA_COOKIES)

        data = json.loads(res.text)

        # print(data)

        is_has_next_page = data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
        end_cursor = data["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]

        edges = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]

        new_post_row_list = []
        new_media_row_list = []

        for edge in edges:
            post_data = edge["node"]
            post_id = post_data["id"]

            if post_id in post_id_list:

                continue

            thumbnail_url = post_data["thumbnail_src"]
            media_list = []

            if "edge_sidecar_to_children" in post_data:
                target_edge = post_data["edge_sidecar_to_children"]["edges"]
            else:
                target_edge = [edge]

            for x in target_edge:
                node = x["node"]
                if node["is_video"] is True:
                    media_list.append({"type": "video", "url": node["video_url"]})
                else:
                    media_list.append({"type": "image", "url": node["display_url"]})

            text = post_data["edge_media_to_caption"]["edges"][0]["node"]["text"]
            timestamp = post_data["taken_at_timestamp"]

            shortcode = post_data["shortcode"]

            thumbnail_filename = f"thumbnail_{nickname}_{post_id}_{get_random_string(6)}"



            upload_result = cloudinary.uploader.upload(get_media_io(thumbnail_url),
                                                       public_id=f"{CLOUDINARY_DIRECTORY}/{nickname}/thumbnail/{thumbnail_filename}")
            new_thumbnail_url = upload_result["secure_url"]

            new_post_row = PostData(
                id=post_id,
                user_id=user_id,
                text=text,
                shortcode=shortcode,
                thumbnail_url=new_thumbnail_url,
                upload_datetime=datetime.datetime.fromtimestamp(timestamp),
                crawl_datetime=datetime.datetime.now()
            )

            new_post_row_list.append(new_post_row)

            for idx, media in enumerate(media_list):
                media_filename = f"{nickname}_{post_id}_{idx}_{get_random_string(6)}"

                if media["type"] == "image":

                    upload_result = cloudinary.uploader.upload(get_media_io(media["url"]),
                                                               public_id=f"{CLOUDINARY_DIRECTORY}/{nickname}/posts/{media_filename}")

                else:
                    upload_result = cloudinary.uploader.upload_large(get_media_io(media["url"]), resource_type = "video",
                                                                     public_id=f"{CLOUDINARY_DIRECTORY}/{nickname}/posts/{media_filename}.mp4")

                new_media_url = upload_result["secure_url"]

                new_media_row = MediaSrc(
                    post_id=post_id,
                    media_type=media["type"],
                    url=new_media_url
                )

                new_media_row_list.append(new_media_row)

            # print(media_list)


        session.add_all(new_post_row_list)
        session.commit()
        session.add_all(new_media_row_list)
        session.commit()


        if is_has_next_page is False:
            break


