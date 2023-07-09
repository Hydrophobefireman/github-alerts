"""
A python script to scrape github and post a discord webhook
"""
import os
import time
import json

import dotenv
import requests

from gh import GHManager

dotenv.load_dotenv()

# GitHub repository information
REPO_OWNER = os.environ["REPO_OWNER"]
REPO_NAME = os.environ["REPO_NAME"]
CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", 60))
WEBHOOK_URL_FILE = "urls.json"
# Keep track of the last seen commit and pull request


manager = GHManager(REPO_OWNER, REPO_NAME)


def post_webhook(payload: dict):
    """
    Takes a payload dictionary and posts it to the webhook urls in urls.json list
    """
    with open(WEBHOOK_URL_FILE, "r", encoding="utf-8") as file:
        urls = json.load(file)
        for url in urls:
            print("[webhook] Posting update")
            requests.post(url, json=payload, timeout=120)


def run():
    """
    Driver
    """
    while True:
        print("[manager] Checking for a new commit")
        commit = manager.check_new_commit()
        if commit is None:
            print("[manager] did not find any new commits")
        else:
            print(
                f"[manager] found commit: {commit['sha']} - {commit['commit']['message']}"
            )
            payload = {
                "embeds": [
                    {
                        "title": "New Commit",
                        "description": commit["commit"]["message"],
                        "url": commit["html_url"],
                        "color": 0xFF0000,  # Red color
                        "fields": [
                            {
                                "name": "Author",
                                "value": commit["commit"]["author"]["name"],
                            }
                        ],
                    }
                ]
            }
            post_webhook(payload)

        pull_req = manager.check_new_pulls()
        if pull_req is None:
            print("[manager] did not find any new PRs")
        else:
            print(f"[manager] found PR: {pull_req['id']} - {pull_req['title']}")
            payload = {
                "embeds": [
                    {
                        "title": "New PR",
                        "description": pull_req["title"],
                        "url": pull_req["html_url"],
                        "color": 0xFF0000,
                        "fields": [
                            {"name": "Author", "value": pull_req["user"]["login"]}
                        ],
                    }
                ]
            }
            post_webhook(payload)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run()
