import atexit
import json
import os


class Cache:
    CACHE_FILE = ".cache"

    def __init__(self):
        self.known_hashes = self.load_cache()
        self.new_hashes = []
        atexit.register(self.save_cache)

    def load_cache(self):
        if os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("known_hashes", [])
        return []

    def save_cache(self):
        with open(self.CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(
                dict(known_hashes=self.known_hashes + self.new_hashes), f, indent=4
            )


cache = Cache()
