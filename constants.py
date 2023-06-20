from dotenv import load_dotenv
from os import getenv

load_dotenv()

MAX_TITLE_LEN = getenv("MAX_TITLE_LEN", 70)
CARDS_PER_PAGE = getenv("CARDS_PER_PAGE", 15)
AVATAR_CACHE_SIZE = getenv("AVATAR_CACHE_SIZE", 64)
API = getenv("API", "http://127.0.0.1:8080")
