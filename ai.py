import json
import asyncio
import openai

import config
from bookmarks import Item
import errors

openai_client = openai.AsyncClient(api_key=config.OPENAI_API_KEY)

SYSTEM_PROMPT = """
Provide a short description for each link, 
the seniority level the content is suitable for, 
and a few tags describing the topic. 
Format the response as a JSON array of objects, each containing the following fields:
- "title": The title of the link.
- "url": The URL of the link.
- "description": A short description of the content.
- "seniority": The list of seniority levels the content is suitable for (junior, mid, senior).
- "tags": A list of tags describing the topic.
Do not add ``json or ``` tags around your responses.
"""

async def process_bookmarks(items: list[Item], batch_size: int = 10):
    total_items = len(items)
    batches = [items[i : i + batch_size] for i in range(0, total_items, batch_size)]

    animation_task = asyncio.create_task(dot_animation())
    try:
        tasks = [process(batch) for batch in batches]
        responses = await asyncio.gather(*tasks)
    except openai.AuthenticationError:
        raise errors.EnvironmentError(
            "\r🔑 Authentication error: Make sure your API key is correct."
        )
    finally:
        animation_task.cancel()
        await asyncio.gather(animation_task, return_exceptions=True)

    print("\r🤖 Processing bookmarks... Done!")
    return [item for batch in responses for item in batch]


async def dot_animation():
    while True:
        for dots in range(1, 4):
            print(f"\r🤖 Processing bookmarks{'.' * dots}", end="")
            await asyncio.sleep(0.5)
        print("\r", end="")


async def process(items: list[Item]):
    user_prompt = create_user_prompt(items)
    response_text = await fetch_description(user_prompt)
    return response_text


def create_user_prompt(items: list[Item]) -> str:
    prompt = ""
    for item in items:
        prompt += f"Link: {item.url}\nTitle: {item.title}\n\n"
    return prompt


async def fetch_description(user_prompt: str):
    response = await openai_client.chat.completions.create(
        model=config.OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1500,
        temperature=0.7,
    )
    content =  response.choices[0].message.content.strip()
    return json.loads(content)


# Example usage
async def main():
    urls = [
        Item("GitHub", "https://github.com"),
        Item("Reddit", "https://www.reddit.com"),
        Item("Twitter", "https://twitter.com"),
    ]
    result = await process_bookmarks(urls)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
