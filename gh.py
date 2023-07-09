"""
Github Manager
"""
import json

import requests

from gh_types import CommitData, PullRequest


class GHManager:
    """
    Helper functions for github api
    """

    timeout = 120
    cache = ".cache"

    def save_cache(self) -> None:
        """
        Saves last values to the cache
        """
        self.cache_dict[self.api_url] = {
            "last_commit_sha": self.last_commit_sha,
            "last_pull_request_id": self.last_pull_request_id,
        }
        with open(self.cache, "w", encoding="utf-8") as file:
            file.write(json.dumps(self.cache_dict))

    def __init__(self, repo_owner: str, repo_name: str) -> None:
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        try:
            with open(self.cache, "r+", encoding="utf-8") as cache:
                self.cache_dict = json.load(cache)
            # pylint: disable=bare-except
        except:
            self.cache_dict = {
                self.api_url: {
                    "last_commit_sha": None,
                    "last_pull_request_id": None,
                }
            }
        self.last_commit_sha = self.cache_dict[self.api_url]["last_commit_sha"]
        self.last_pull_request_id = self.cache_dict[self.api_url][
            "last_pull_request_id"
        ]

    @property
    def commit_url(self) -> str:
        """
        Returns commit API URL based on current api base URL
        """
        return f"{self.api_url}/commits"

    @property
    def pr_url(self) -> str:
        """
        Returns pr API URL based on current api base URL
        """
        return f"{self.api_url}/pulls"

    def check_new_commit(self) -> CommitData | None:
        """
        Gets the latest commits from the repo and returns details about it
        """
        response = requests.get(self.commit_url, timeout=self.timeout)
        commits = response.json()
        latest_commit = commits[0] if commits else None

        # Check if there's a new commit
        if latest_commit["sha"] != self.last_commit_sha:
            self.last_commit_sha = latest_commit["sha"]
            self.save_cache()
            return latest_commit
        return None

    def check_new_pulls(self) -> PullRequest | None:
        """
        Checks for new PRs and returns it if found
        """
        response = requests.get(self.pr_url, timeout=self.timeout)
        pull_requests = response.json()
        latest_pull_request = pull_requests[0] if pull_requests else None

        # Check if there's a new pull request
        if latest_pull_request["id"] != self.last_pull_request_id:
            self.last_pull_request_id = latest_pull_request["id"]
            self.save_cache()
            return latest_pull_request
        return None
