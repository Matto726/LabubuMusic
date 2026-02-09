import os
import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

# Load local environment if available
load_dotenv()

# --- Credentials ---
API_ID = int(getenv("API_ID", "35020744"))
API_HASH = getenv("API_HASH", "0b3d137e0309b92d43f82b13a24deae2")
BOT_TOKEN = getenv("BOT_TOKEN", "8561351372:AAHMOO7tFeWxkDKeDlgtJuEups5F9s7GsmE")

# --- Database & Storage ---
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://matto_laado:@MonkeyFOrever567890@cluster0.q5dcvoq.mongodb.net/?appName=Cluster0")
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1003809861696"))
TEMP_DB_FOLDER = "tempdb"

# --- Owner Configuration ---
OWNER_ID = int(getenv("OWNER_ID", "8333964509"))
OWNER_USERNAME = getenv("OWNER_USERNAME", "boobubots")

# --- Deployment ---
HEROKU_API_KEY = getenv("HRKU-AAtKwnaZwQxb0GSbWRNoFNi8ZQh-kKQ6KyuyuUgyui1Q_____wd4I1uCcrKe")
HEROKU_APP_NAME = getenv("madhupaplu")

# --- Updates & Repo ---
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/Matto726/LabubuMusic")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", None)

# --- Links & Branding ---
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/Laboobubots")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "https://t.me/Laboobubots")

# Socials
INSTAGRAM = getenv("INSTAGRAM", "https://t.me/Laboobubots")
YOUTUBE = getenv("YOUTUBE", "https://t.me/Laboobubots")
GITHUB = getenv("GITHUB", "https://t.me/Laboobubots")
DONATE = getenv("DONATE", "https://t.me/Laboobubots")
PRIVACY_LINK = getenv("PRIVACY_LINK", "https://telegra.ph/Privacy-Policy-for-LabubuMusic-01-01")

# --- Images ---
START_IMG_URL = getenv("START_IMG_URL", "https://telegra.ph/file/c5952790fa8235f499749.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://telegra.ph/file/c5952790fa8235f499749.jpg")
PLAYLIST_IMG_URL = getenv("PLAYLIST_IMG_URL", "https://telegra.ph/file/c5952790fa8235f499749.jpg")
STATS_IMG_URL = getenv("STATS_IMG_URL", "https://telegra.ph/file/c5952790fa8235f499749.jpg")
TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", "https://telegra.ph/file/c5952790fa8235f499749.jpg")
TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", "https://telegra.ph/file/c5952790fa8235f499749.jpg")
STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://telegra.ph/file/c5952790fa8235f499749.jpg")
SOUNCLOUD_IMG_URL = getenv("SOUNCLOUD_IMG_URL", "https://telegra.ph/file/c5952790fa8235f499749.jpg")
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://telegra.ph/file/c5952790fa8235f499749.jpg")
SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", "https://telegra.ph/file/c5952790fa8235f499749.jpg")
SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", "https://telegra.ph/file/c5952790fa8235f499749.jpg")
SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", "https://telegra.ph/file/c5952790fa8235f499749.jpg")

# --- Limits & Settings ---
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 300))
DURATION_LIMIT = DURATION_LIMIT_MIN * 60
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824)) # 1GB
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))

# --- External APIs ---
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)

# --- Sessions ---
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

# --- Global State Variables ---
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# --- Utility Functions ---
def time_to_seconds(time_str):
    """
    Converts a time string (HH:MM:SS or MM:SS) to integer seconds.
    Required by queue/playback modules.
    """
    if not time_str:
        return 0
        
    parts = time_str.split(':')
    parts = [int(p) for p in parts]
    
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 1:
        return parts[0]
    else:
        return 0