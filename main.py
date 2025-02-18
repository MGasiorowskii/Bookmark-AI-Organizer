#!/usr/bin/env python3

import asyncio
import argparse
import subprocess
import sys

import ai
from bookmarks import BROWSER_PATHS, Bookmarks, BookmarksFetchError
from utils import error


async def main():
    parser = argparse.ArgumentParser(
        description="Export bookmarks from the browser to a CSV file."
    )
    parser.add_argument(
        "--browser",
        choices=BROWSER_PATHS.keys(),
        default="chrome",
        help="Choose a browser.",
    )
    parser.add_argument(
        "--folder",
        type=str,
        help="Filter bookmarks by folder name (e.g., 'Programming').",
    )
    args = parser.parse_args()

    print(f"📚 Exporting bookmarks from {args.browser.capitalize()}.")
    bookmarks = Bookmarks(args.browser)
    if not bookmarks.urls:
        print(error("⚠️ Not found any bookmarks."))
    print(f"🔍 Found: {len(bookmarks.urls)} bookmarks.")

    if args.folder:
        directory = bookmarks.filter_by_folder(args.folder)
        print(
            f"🔍 Found: {len(directory.urls)} bookmarks in the folder '{directory.name}'."
        )
        if not directory.urls:
            return

    urls = directory.urls if args.folder else bookmarks.urls
    bookmark_summaries = await ai.process_bookmarks(urls)
    print(bookmark_summaries)


def install_requirements():
    print("📦 Installing required packages...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        stdout = subprocess.PIPE,
        stderr=subprocess.PIPE
    )

if __name__ == "__main__":
    install_requirements()
    try:
        asyncio.run(main())
    except (BookmarksFetchError, EnvironmentError) as e:
        print(e)
