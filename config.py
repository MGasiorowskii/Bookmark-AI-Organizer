import os
from dotenv import load_dotenv

import errors

load_dotenv()


def get_or_rise(env: str) -> str:
    value = os.getenv(env)
    if not value:
        raise errors.EnvError(f"Environment variable {env} is not set or invalid.")
    return value


OPENAI_API_KEY = get_or_rise("OPENAI_API_KEY")
OPENAI_MODEL_NAME = get_or_rise("OPENAI_MODEL_NAME")
NOTION_API_KEY = get_or_rise("NOTION_API_KEY")
NOTION_DATABASE_ID = get_or_rise("NOTION_DATABASE_ID")


BROWSER_PATHS = {
    "chrome": {
        "windows": r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Bookmarks",
        "linux": "~/config/google-chrome/Default/Bookmarks",
        "darwin": "~/Library/Application Support/Google/Chrome/Default/Bookmarks",
    },
    "edge": {
        "windows": r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Bookmarks",
        "linux": "~/config/microsoft-edge/Default/Bookmarks",
        "darwin": "~/Library/Application Support/Microsoft Edge/Default/Bookmarks",
    },
    "brave": {
        "windows": r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Bookmarks",
        "linux": "~/.config/BraveSoftware/Brave-Browser/Default/Bookmarks",
        "darwin": "~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks",
    },
}

BROWSER_NAMES = tuple(BROWSER_PATHS.keys())
