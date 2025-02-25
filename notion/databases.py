from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from notion import NotionClient

import errors
from cache import cache
from notion import schemas


async def get_or_create(client: NotionClient) -> tuple[str, bool]:
    fetched_ids = await get(client)
    db_id = cache.databases.get(client.browser)
    if fetched_ids and db_id in fetched_ids:
        print(f"✅ Databases for {client.browser.capitalize()} already exists!")
        return db_id, False

    new_id = await create(client)
    cache.databases[client.browser] = new_id
    return new_id, True


async def get(client: NotionClient) -> list[str]:
    payload = schemas.SEARCH
    payload["filter"]["value"] = "database"

    async with client.session.post(
        client.search_endpoint, headers=client.headers, json=payload
    ) as response:
        data = await response.json()
        return [db["id"] for db in data.get("results", [])]


async def create(client: NotionClient) -> str:
    payload = _get_payload(client.browser)

    async with client.session.post(
        client.database_endpoint, headers=client.headers, json=payload
    ) as response:
        data = await response.json()
        if response.status != 200:
            raise errors.ProcessingError(
                f"❌ Database creating error: {response.status} - {response.reason}"
            )
        print(f"✅ Database for {client.browser.capitalize()} created successfully!")
        return data["id"]


def _get_payload(browser: str) -> str:
    payload = schemas.DATABASE
    payload["title"][0]["text"]["content"] = f"{browser.capitalize()} Bookmarks"
    return payload
