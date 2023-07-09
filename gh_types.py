# pylint: skip-file
from typing import TypedDict


class CommitAuthor(TypedDict):
    name: str
    email: str
    date: str


class Tree(TypedDict):
    sha: str
    url: str


class Verification(TypedDict):
    verified: bool
    reason: str
    signature: str
    payload: str


class Commit(TypedDict):
    author: CommitAuthor
    committer: CommitAuthor
    message: str
    tree: Tree
    url: str
    comment_count: int
    verification: Verification


class Author(TypedDict):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool


class Committer(TypedDict):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool


class Parent(TypedDict):
    sha: str
    url: str
    html_url: str


class CommitData(TypedDict):
    sha: str
    node_id: str
    commit: Commit
    url: str
    html_url: str
    comments_url: str
    author: Author
    committer: Committer
    parents: list[Parent]


class PullRequest(TypedDict):
    url: str
    id: int
    node_id: str
    html_url: str
    diff_url: str
    patch_url: str
    issue_url: str
    number: int
    state: str
    locked: bool
    title: str
    user: dict
    body: str
    created_at: str
    updated_at: str
    closed_at: str | None
    merged_at: str | None
    merge_commit_sha: str
    assignee: dict | None
    assignees: list[dict]
    requested_reviewers: list[dict]
    requested_teams: list[dict]
    labels: list[dict]
    milestone: dict | None
    draft: bool
    commits_url: str
    review_comments_url: str
    review_comment_url: str
    comments_url: str
    statuses_url: str
    head: dict
    base: dict
    _links: dict
