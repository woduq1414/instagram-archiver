from config import TARGET_PAGE_LIST
from crawl.get_id import get_id_by_nickname
from crawl.highlights import get_highlights
from crawl.login import login
from crawl.posts import get_posts
import storage.setup
from crawl.stories import get_stories


def insta_crawl_job():


    login()

    for nickname in TARGET_PAGE_LIST:
        user_id = get_id_by_nickname(nickname)

        if user_id is None:
            continue

        get_posts(user_id = user_id, nickname=nickname)

        highlight_id_list = get_highlights(user_id=user_id, nickname=nickname)
        get_stories(user_id = user_id, nickname=nickname)
        for highlight_id in highlight_id_list:
            print(highlight_id)
            get_stories(user_id=user_id, nickname=nickname, highlight_id=highlight_id)


if __name__ == "__main__":
    insta_crawl_job()