class Cache:
    __shared_state = {
        "INSTA_COOKIES" : "",
        "INSTA_HEADERS" : {},
        "INSTA_NICKNAME_ID_DICT" : {}
    }
    def __init__(self):
        self.INSTA_COOKIES = None
        self.INSTA_HEADERS = None
        self.INSTA_NICKNAME_ID_DICT = None
        self.__dict__ = self.__shared_state