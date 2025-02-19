import os
from dotenv import load_dotenv

import errors

load_dotenv()


def get_or_rise(env: str) -> str:
    value = os.getenv(env)
    if not value:
        raise errors.EnvironmentError(
            f"Environment variable {env} is not set or invalid."
        )
    return value


OPENAI_API_KEY = get_or_rise("OPENAI_API_KEY")
OPENAI_MODEL_NAME = get_or_rise("OPENAI_MODEL_NAME")
NOTION_API_KEY = get_or_rise("NOTION_API_KEY")
NOTION_DATABASE_ID = get_or_rise("NOTION_DATABASE_ID")
