from typing import Any
from datetime import datetime, timedelta
from collections import Counter
from sapcloudsdk.arguments import args


def get_last_commit_date(commit_list: list[Any]):
    try:
        return datetime.fromisoformat(commit_list[0]["date"].rstrip("Z"))
    except:
        return datetime.min


def print_results(results: list[Any]):
    keys: list[str] = []
    filtered: list[Any] = []
    for result in results:
        if result["repository"]["full_name"] not in keys:
            keys.append(result["repository"]["full_name"])
            filtered.append(result)
    active = [
        result
        for result in filtered
        if datetime.utcnow() - timedelta(days=14)
        < get_last_commit_date(result["last_commit"])
    ]
    relevant = [
        result
        for result in active
        if len(result["last_commit"]) > 5
        and any(l in args.languages for l in result["languages"])
    ]
    maintained = [
        result
        for result in filtered
        if datetime.utcnow() - timedelta(days=240)
        < get_last_commit_date(result["last_commit"])
        and result not in relevant
        and len(result["last_commit"]) > 5
    ]
    inactive = [
        result
        for result in filtered
        if result not in maintained and result not in relevant
    ]

    print(f"## Active projects ({len(relevant)} of {len(filtered)} repos)")
    for r in sorted(relevant, key=lambda r: r["repository"]["full_name"]):
        commit_counter = Counter([c["email"] for c in r["last_commit"][:100]])
        top_committers = ", ".join([c[0] for c in commit_counter.most_common()[:4]])

        print(f"- [{r['repository']['full_name']}]({r['repository']['html_url']})")
        print(f"  - {len(r['committers'])} committers ({top_committers})")
        print(f"  - {len(r['last_commit'])} commits")
        print(f"  - {' & '.join(list(r['languages'].keys())[:3])}")

    print()
    print(f"## Maintained projects ({len(maintained)} of {len(filtered)} repos)")
    for r in sorted(maintained, key=lambda r: r["repository"]["full_name"]):
        commit_counter = Counter([c["email"] for c in r["last_commit"][:100]])
        top_committers = ", ".join([c[0] for c in commit_counter.most_common()[:4]])

        print(f"- [{r['repository']['full_name']}]({r['repository']['html_url']})")
        print(f"  - {len(r['committers'])} committers ({top_committers})")
        print(f"  - {len(r['last_commit'])} commits")
        print(f"  - {' & '.join(list(r['languages'].keys())[:3])}")

    print()
    print(f"## Inactive projects ({len(inactive)} of {len(filtered)} repos)")
    for r in sorted(inactive, key=lambda r: r["repository"]["full_name"]):
        commit_counter = Counter([c["email"] for c in r["last_commit"][:100]])
        top_committers = ", ".join([c[0] for c in commit_counter.most_common()[:4]])

        print(f"- [{r['repository']['full_name']}]({r['repository']['html_url']})")
        print(f"  - {len(r['committers'])} committers ({top_committers})")
        print(f"  - {len(r['last_commit'])} commits")
        print(f"  - {' & '.join(list(r['languages'].keys())[:3])}")
