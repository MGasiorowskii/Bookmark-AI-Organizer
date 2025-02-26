#!/usr/bin/env python3

import asyncio
import argparse
import subprocess
import sys

import ai
import notion
import config
import errors

from bookmarks import Bookmarks
from cache import cache


async def main(args: argparse.Namespace):
    print(f"📚 Exporting bookmarks from {args.browser.capitalize()}.")
    bookmarks = Bookmarks(args.browser)
    print(f"🔍 Found: {len(bookmarks.urls)} bookmarks.")

    if args.folder:
        directory = bookmarks.filter_by_folder(args.folder)
        print(
            f"🔍 Found: {len(directory.urls)} bookmarks in the folder '{directory.name}'."
        )
        urls = directory.unique_urls
    else:
        urls = bookmarks.unique_urls

    if not urls:
        return print("📚 No unique bookmarks to process.")

    bookmark_summaries = await ai.process_bookmarks(urls)
    await notion.upload_bookmarks(args.browser, bookmark_summaries)


def install_requirements(if_install: bool):
    if not if_install:
        print("📦 Skipping installation of required packages.")
        return

    print("📦 Installing required packages...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
    )
    print("📦 Required packages installed successfully.\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Export bookmarks from the browser to the Notion."
    )
    parser.add_argument(
        "--browser",
        choices=config.BROWSER_NAMES,
        default="chrome",
        help="Choose a browser.",
    )
    parser.add_argument(
        "--folder",
        type=str,
        help="Filter bookmarks by folder name (e.g., 'Programming').",
    )
    parser.add_argument(
        "--install", type=bool, default=True, help="Install required packages."
    )
    return parser.parse_args()


if __name__ == "__main__":
    user_args = parse_args()
    install_requirements(user_args.install)
    try:
        asyncio.run(main(user_args))
    except (errors.ProcessingError, errors.EnvError) as e:
        cache.clear_all()
        print(e)
