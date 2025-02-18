import os
from dotenv import load_dotenv

from utils import error

load_dotenv()

def get_or_rise(env: str) -> str:
    value = os.getenv(env)
    if not value:
        raise EnvironmentError(error(f"Environment variable {env} is not set or invalid."))
    return value


OPENAI_API_KEY = get_or_rise("OPENAI_API_KEY")
NOTION_API_KEY=get_or_rise("NOTION_API_KEY")
NOTION_DATABASE_ID=get_or_rise("NOTION_DATABASE_ID")
