from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from notion import NotionClient

import asyncio
import errors
from http import HTTPStatus

import config
from models import Bookmark
from notion import schemas
from utils import dot_animation


RETRY_DELAY = 5
SEM_LIMIT = 10
semaphore = asyncio.Semaphore(SEM_LIMIT)


async def search(client: NotionClient) -> list[dict]:
    payload = schemas.SEARCH
    payload["filter"]["value"] = "page"

    async with client.session.post(
        client.search_endpoint, headers=client.headers, json=payload
    ) as response:
        data = await response.json()
        return data.get("results", [])


async def update(client: NotionClient):
    payload = schemas.UPDATE

    endpoint = f"{client.page_endpoint}/{config.NOTION_DATABASE_ID}"
    async with client.session.patch(
        endpoint, headers=client.headers, json=payload
    ) as response:
        data = await response.json()
        if response.status != HTTPStatus.OK:
            print(data)
            raise errors.ProcessingError(
                f"❌ Page tittle updating error: {response.status} - {response.reason}"
            )
        print("✅ Page title updated successfully!")


async def bulk_create(
    client: NotionClient, data: list[Bookmark]
) -> tuple[int, int, list[Bookmark]]:
    successes = 0
    failures = 0
    failed = []

    animation_task = asyncio.create_task(dot_animation())
    tasks = [create(client, item) for item in data]

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result, item in zip(results, data):
        if isinstance(result, Exception):
            failures += 1
            failed.append(item)
        else:
            successes += 1

    animation_task.cancel()
    await asyncio.gather(animation_task, return_exceptions=True)
    print("\r🤖 Processing bookmarks... Done!")
    return successes, failures, failed


async def create(client: NotionClient, data: Bookmark):
    payload = _get_payload(client.database_id, data)

    async with semaphore:
        async with client.session.post(
            client.page_endpoint, headers=client.headers, json=payload
        ) as response:
            if response.status == HTTPStatus.OK:
                return await response.json()
            elif response.status == HTTPStatus.TOO_MANY_REQUESTS:
                retry_after = response.headers.get("Retry-After")
                delay = retry_after or RETRY_DELAY
                print(f"⚠️ Rate limit reached, retrying in {delay} seconds...")
                await asyncio.sleep(delay)

            raise errors.ProcessingError(
                f"❌ Page creating error: {response.status} - {response.reason}"
            )


def _get_payload(database_id: str, data: Bookmark) -> dict:
    payload = schemas.PAGE
    payload["parent"]["database_id"] = database_id
    payload["properties"]["Name"]["title"][0]["text"]["content"] = data.title
    payload["properties"]["Description"]["rich_text"][0]["text"][
        "content"
    ] = data.description
    payload["properties"]["URL"]["url"] = data.url
    payload["properties"]["Seniority"]["multi_select"] = [
        {"name": s.value} for s in data.seniority
    ]
    payload["properties"]["Tags"]["multi_select"] = [{"name": t} for t in data.tags]
    return payload
