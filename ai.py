import asyncio
import openai

import config
import errors

from bookmarks import Item
from models import BookmarkSummaries
from utils import dot_animation

openai_client = openai.AsyncClient(api_key=config.OPENAI_API_KEY)

SYSTEM_PROMPT = """
Provide a short description for each link, 
the seniority level the content is suitable for, 
and a few tags describing the topic. 
"""


async def process_bookmarks(items: list[Item], batch_size: int = 10):
    print("\n🤖 Generating descriptions for bookmarks by AI.")
    total_items = len(items)
    batches = [items[i : i + batch_size] for i in range(0, total_items, batch_size)]

    animation_task = asyncio.create_task(dot_animation())
    try:
        tasks = [process(batch) for batch in batches]
        responses = await asyncio.gather(*tasks)
    except openai.AuthenticationError:
        raise errors.EnvError(
            "\r🔑 Authentication error: Make sure your API key is correct."
        )
    finally:
        animation_task.cancel()
        await asyncio.gather(animation_task, return_exceptions=True)

    print("\r🤖 Processing bookmarks... Done!")
    return [item for batch in responses for item in batch]


async def process(items: list[Item]):
    user_prompt = create_user_prompt(items)
    response_text = await fetch_description(user_prompt)
    return response_text


def create_user_prompt(items: list[Item]) -> str:
    prompt = ""
    for item in items:
        prompt += f"Link: {item.url}\nTitle: {item.title}\n\n"
    return prompt


async def fetch_description(user_prompt: str) -> BookmarkSummaries:
    response = await openai_client.beta.chat.completions.parse(
        model=config.OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1500,
        temperature=0.7,
        response_format=BookmarkSummaries,
    )
    return response.choices[0].message.parsed
