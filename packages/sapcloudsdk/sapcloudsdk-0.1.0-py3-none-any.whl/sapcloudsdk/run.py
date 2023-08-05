from timeit import default_timer
import sys
import json
from typing import Any
from time import sleep
from sapcloudsdk.github import (
    committers,
    languages,
    last_commit,
    search_code,
)
from sapcloudsdk.sdk import print_results
from sapcloudsdk.arguments import args


def print_time(step: str, since: float):
    if "-v" in sys.argv:
        new_timer = default_timer()
        print(step, new_timer - since, "seconds")
        return new_timer
    return since


def format_repo(repository: Any) -> dict[str, Any]:
    sleep(0.1)
    owner = repository["owner"]["login"]
    repo = repository["name"]
    if "-v" in sys.argv:
        print(f"Loading data for {owner}/{repo}")
    return {
        "repository": repository,
        "last_commit": last_commit(owner, repo),
        "committers": committers(owner, repo),
        "languages": languages(owner, repo),
    }


def main():

    try:
        with open(args.from_file, "r", encoding="utf8") as search_file:
            results = json.load(search_file)
    except FileNotFoundError:
        results = [
            format_repo(result["repository"])
            for result in search_code(
                f"{args.search}+filename:{args.filename}+-org:cloudsdk"
            )
        ]

    if args.save:
        with open(args.to_file, "w") as search_file:
            json.dump(
                results,
                search_file,
                indent=2,
            )
            if args.verbose >= 1:
                print("Search results saved to file")
    print_results(results)
