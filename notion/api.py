import aiohttp

import config
from cache import cache
from notion import databases, pages

NOTION_API_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


class NotionClient:
    headers = {
        "Authorization": f"Bearer {config.NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }
    database_endpoint = NOTION_API_URL + "/databases"
    page_endpoint = NOTION_API_URL + "/pages"
    search_endpoint = NOTION_API_URL + "/search"

    def __init__(self, browser: str):
        self.browser = browser
        self.database_id = None

    async def __aenter__(self):
        self.session = await aiohttp.ClientSession().__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.__aexit__(None, None, None)


async def upload_bookmarks(browser: str, bookmarks: list[dict]):
    print(f"\n📚 Uploading bookmarks to Notion")
    async with NotionClient(browser) as client:
        found_pages = await pages.search(client)
        if len(found_pages) == 1:
            await pages.update(client)

        database_id, created = await databases.get_or_create(client)
        client.database_id = database_id

        successes, failures, failed = await pages.bulk_create(client, bookmarks)

    print("\n📊 Statistic:")
    print(f"✅ Added: {successes}")
    print(f"❌ Failed: {failures}")

    if failed:
        print("\n📌 Failed bookmarks:")
        to_clear = []
        for title, url in failed:
            print(f"  - {title}")
            to_clear.append(url)

        cache.clear(to_clear)
