import cloudinary
from config import CLOUDINARY_CRED

cloudinary.config(
    cloud_name = CLOUDINARY_CRED["cloud_name"],
    api_key = CLOUDINARY_CRED["api_key"],
    api_secret = CLOUDINARY_CRED["api_secret"]
)
