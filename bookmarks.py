import hashlib
import json
import os
from utils import error
import platform
from cache import cache

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


class BookmarksFetchError(Exception):
    def __str__(self):
        return error(self.args[0])


class Item:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __str__(self):
        return f"{self.title}"

    def hash(self):
        return hashlib.sha256(self.url.encode()).hexdigest()


class Folder:
    def __init__(self, name):
        self.name = name
        self.items = []

    def __str__(self):
        return f"{self.name}"

    def add_item(self, item):
        self.items.append(item)

    @property
    def urls(self):
        urls = []
        for item in self.items:
            if isinstance(item, Item):
                urls.append(item)
            elif isinstance(item, Folder):
                urls.extend(item.urls)
        return urls

    @property
    def unique_urls(self):
        unique_urls = []
        for url in self.urls:
            hashed_url = url.hash()
            if hashed_url not in cache.known_hashes:
                cache.new_hashes.append(hashed_url)
                unique_urls.append(url)

        return unique_urls


class Bookmarks:
    def __init__(self, browser: str):
        self.folders = []
        self.urls = []
        self.root = None
        self.load_bookmarks(browser)

    def load_bookmarks(self, browser):
        path = self._get_path(browser)

        if not os.path.exists(path):
            raise BookmarksFetchError(f"❌ Bookmarks file not found: {path}")

        with open(path, "r", encoding="utf-8") as file:
            browser_data = json.load(file)

        self.process_root(browser_data)

    def _get_path(self, browser: str) -> str:
        """Returns the path to the bookmarks file for the selected browser."""
        system = platform.system().lower()
        return os.path.expandvars(os.path.expanduser(BROWSER_PATHS[browser][system]))

    def process_root(self, browser_data: dict):
        self.root = Folder("Root")
        for section in ["bookmark_bar", "other", "synced"]:
            if section in browser_data["roots"]:
                subfolder = self.extract_bookmarks(browser_data["roots"][section])
                subfolder.name = section
                self.root.add_item(subfolder)

    def extract_bookmarks(self, bookmark_data) -> Folder:
        folder = Folder(bookmark_data.get("name"))

        for item in bookmark_data.get("children", []):
            if item.get("type") == "folder":
                subfolder = self.extract_bookmarks(item)
                folder.add_item(subfolder)
                self.folders.append(subfolder)
            elif item.get("type") == "url":
                url = Item(title=item["name"], url=item["url"])
                folder.add_item(url)
                self.urls.append(url)
        return folder

    def filter_by_folder(self, folder_name: str):
        for folder in self.folders:
            if folder.name.lower() == folder_name.lower():
                return folder
        return None

    @property
    def unique_urls(self):
        return self.root.unique_urls
