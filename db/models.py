from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey

from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()
# target_metadata = Base.metadata

class InstaUser(Base):
    __tablename__ = "InstaUser"

    seq = Column(Integer, primary_key=True, autoincrement=True)

    id = Column(String, nullable=False, unique=True)

    nickname = Column(String, nullable=False)

    posts = relationship('PostData', backref='author', lazy=True)


    # stories = relationship('StoryData', backref='author', lazy=True)


class PostData(Base):
    __tablename__ = 'PostData'
    seq = Column(Integer, primary_key=True, autoincrement=True)

    id = Column(String, nullable=False, unique=True)

    user_id = Column(String, ForeignKey("InstaUser.id"), nullable=False)

    text = Column(String, nullable=False)

    shortcode = Column(String, nullable=False)

    thumbnail_url = Column(String, nullable=False)

    upload_datetime = Column(DateTime, nullable=False)

    crawl_datetime = Column(DateTime, nullable=False)


class HighlightData(Base):
    __tablename__ = 'HighlightData'
    seq = Column(Integer, primary_key=True, autoincrement=True)

    id = Column(String, nullable=False, unique=True)

    user_id = Column(String, ForeignKey("InstaUser.id"), nullable=False)

    title = Column(String, nullable=False)

    highlight_icon_url = Column(String, nullable=False)


class StoryData(Base):
    __tablename__ = 'StoryData'
    seq = Column(Integer, primary_key=True, autoincrement=True)

    id = Column(String, nullable=False, unique=True)

    user_id = Column(String, ForeignKey("InstaUser.id"), nullable=False)

    type = Column(String, nullable=False)

    image_url = Column(String, nullable=False)

    video_url = Column(String, nullable=True)

    highlight_id = Column(String, ForeignKey("HighlightData.id"), nullable=True)

    upload_datetime = Column(DateTime, nullable=False)

    crawl_datetime = Column(DateTime, nullable=False)



class MediaSrc(Base):

    __tablename__ = "MediaSrc"
    seq = Column(Integer, primary_key = True, autoincrement=True)

    post_id = Column(String, ForeignKey("PostData.id"), nullable=True)

    media_type = Column(String, nullable=False)

    url = Column(String, nullable=False)
    # story_id = Column(Integer, ForeignKey("PostData.id"), nullable=True)