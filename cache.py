import atexit
import hashlib
import json
import os


class Cache:
    CACHE_FILE = ".cache"

    def __init__(self):
        self.known_hashes = []
        self.new_hashes = []
        self.databases = {}
        self.load_cache()
        atexit.register(self.save_cache)

    def load_cache(self):
        if os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.known_hashes = data.get("known_hashes", [])
                self.databases = data.get("databases", {})

    def save_cache(self):
        with open(self.CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(
                dict(
                    known_hashes=self.known_hashes + self.new_hashes,
                    databases=self.databases,
                ),
                f,
                indent=4,
            )

    def clear(self, urls: list[str]):
        for url in urls:
            self.known_hashes.remove(self.hash(url))

    def hash(self, value:str):
        hashlib.sha256(value.encode()).hexdigest()


cache = Cache()
