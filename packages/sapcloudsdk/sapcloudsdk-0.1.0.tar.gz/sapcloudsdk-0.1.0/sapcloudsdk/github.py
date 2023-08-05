import os
import json
from pprint import pprint
from time import sleep
from typing import Any, Callable
import requests
from requests.auth import HTTPBasicAuth
from sapcloudsdk.arguments import args

auth = HTTPBasicAuth(os.getenv(args.user), os.getenv(args.token))


def get_items(x: dict[str, Any]):
    return x["items"]


def get_login(contributors: list[dict[str, Any]]):
    return [contributor["login"] for contributor in contributors]


def get_commit(commits: list[dict[str, Any]]):
    return [
        {
            "author": c["commit"]["author"]["name"],
            "email": c["commit"]["author"]["email"],
            "date": c["commit"]["author"]["date"],
            "message": c["commit"]["message"],
        }
        for c in commits
    ]


def identity(x: Any):
    return x


def get(
    url: str,
    accessor: Callable[[Any], Any] = identity,
    sleep_between_requests: int = 1,
    retry_counter: int = 0,
    next_counter: int = 0,
    next_limit: int = 100,
    load_next: bool = True,
) -> Any:
    if url == "":
        print("Called with empty URL. Something bad happened!")
        return []

    if args.verbose >= 1:
        print(f"Getting data from {url}")

    res = requests.get(url, auth=auth, verify=args.verify)

    if res.status_code >= 400:
        if retry_counter < 3:
            print(f"Retrying after {sleep_between_requests * 10} seconds")
            sleep(sleep_between_requests * 10)
            return get(url, accessor, sleep_between_requests, retry_counter + 1)
        else:
            print(f"Getting data from {url} returned error code {res.status_code}")
            pprint(res.json())
    if res.links.get("next") and load_next and next_counter < next_limit:
        sleep(sleep_between_requests)
        if int(res.headers.get("X-RateLimit-Remaining", 0)) < 5:
            if args.verbose >= 1:
                print("Rate limit is getting close...")
            sleep(5)
        return accessor(res.json()) + get(
            res.links.get("next", {}).get("url", ""),
            accessor,
            sleep_between_requests,
            next_limit=next_limit,
            next_counter=next_counter + 1,
        )
    return accessor(res.json())


def last_commit(owner: str, repo: str) -> list[Any]:
    try:
        result = get(
            f"{args.api}/repos/{owner}/{repo}/commits?per_page=100",
            get_commit,
            next_limit=5,
        )
        if args.verbose >= 2:
            pprint(result)
        return result
    except:
        return []


def committers(owner: str, repo: str) -> list[Any]:
    try:
        result = get(
            f"{args.api}/repos/{owner}/{repo}/contributors",
            get_login,
            load_next=False,
        )
        if args.verbose >= 2:
            pprint(result)
        return result
    except:
        return []


def languages(owner: str, repo: str) -> dict[str, Any]:
    try:
        result = get(f"{args.api}/repos/{owner}/{repo}/languages", load_next=False)
        if args.verbose >= 2:
            pprint(result)
        return result
    except:
        return {}


def search_code(query: str):
    return get(f"{args.api}/search/code?q={query}&per_page=100", get_items, 10)


def get_issue(owner: str, repo: str, number: str) -> dict[str, Any]:
    return get(f"{args.api}/repos/{owner}/{repo}/issues/{number}")


def get_issues(owner: str, repo: str) -> list[dict[str, Any]]:
    try:
        with open("issues.json", "r", encoding="utf8") as issue_file:
            issues = json.load(issue_file)
            if len(issues):
                if args.verbose >= 1:
                    print("Issues loaded from file")
                    print(len(issues))
                # TODO load new items from API
                return issues
    except FileNotFoundError:
        print("Error opening `issues.json`. File not present?")

    issues = get(f"{args.api}/repos/{owner}/{repo}/issues?state=all&per_page=100")

    if args.verbose >= 1:
        print("Issues loaded from API")

    with open("issues.json", "w", encoding="utf8") as issue_file:
        json.dump(issues, issue_file, indent=2)
        if args.verbose >= 1:
            print("Issues saved to file")

    print(len(issues))
    return issues


def get_comments(owner: str, repo: str) -> list[dict[str, Any]]:
    try:
        with open("comments.json", "r", encoding="utf8") as issue_file:
            comments = json.load(issue_file)
            if len(comments):
                if args.verbose >= 1:
                    print("Comments loaded from file")
                    print(len(comments))
                # TODO load new items from API
                return comments
    except FileNotFoundError:
        print("Error opening `comments.json`. File not present.")

    comments = get(
        f"{args.api}/repos/{owner}/{repo}/issues/comments?state=all&per_page=100"
    )
    if args.verbose >= 1:
        print("Comments loaded from API")
        print(len(comments))

    with open("comments.json", "w") as issue_file:
        json.dump(comments, issue_file, indent=2)
        if args.verbose >= 1:
            print("Comments saved to file")

    return comments
