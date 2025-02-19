#!/usr/bin/env python3

import asyncio
import argparse
import subprocess
import sys

import ai
from bookmarks import BROWSER_PATHS, Bookmarks
import errors


async def main(args: argparse.Namespace):
    print(f"📚 Exporting bookmarks from {args.browser.capitalize()}.")
    bookmarks = Bookmarks(args.browser)
    print(f"🔍 Found: {len(bookmarks.urls)} bookmarks.")

    urls = bookmarks.urls
    if args.folder:
        directory = bookmarks.filter_by_folder(args.folder)
        print(
            f"🔍 Found: {len(directory.urls)} bookmarks in the folder '{directory.name}'."
        )
        urls = directory.urls
        if not urls:
            return

    # bookmark_summaries = await ai.process_bookmarks(urls)
    bookmark_summaries = [{'title': 'GitHub', 'url': 'https://github.com', 'description': 'A platform for version control using Git, allowing developers to collaborate on projects and manage code repositories.', 'seniority': ['junior', 'mid', 'senior'], 'tags': ['version control', 'collaboration', 'software development']}, {'title': 'Reddit', 'url': 'https://www.reddit.com', 'description': 'A social news aggregation and discussion website where users can submit content and engage in conversations on various topics.', 'seniority': ['junior', 'mid', 'senior'], 'tags': ['social media', 'community', 'discussion']}, {'title': 'Twitter', 'url': 'https://twitter.com', 'description': 'A microblogging platform that allows users to post and interact with short messages known as tweets.', 'seniority': ['junior', 'mid', 'senior'], 'tags': ['social media', 'communication', 'news']}]
    print("📝 Saving bookmarks to a CSV file...")



def install_requirements(if_install: bool):
    if not if_install:
        print("📦 Skipping installation of required packages.")
        return

    print("📦 Installing required packages...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

def parse_args():
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
    parser.add_argument(
        "--install",
        type=bool,
        default=True,
        help="Install required packages."
    )
    return parser.parse_args()


if __name__ == "__main__":
    user_args = parse_args()
    install_requirements(user_args.install)
    try:
        asyncio.run(main(user_args))
    except (errors.ProcessingError, errors.EnvironmentError) as e:
        print(e)
