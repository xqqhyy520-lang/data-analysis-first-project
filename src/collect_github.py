from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import requests
import yaml


GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"


@dataclass(frozen=True)
class GitHubQueryConfig:
    queries: list[str]
    per_query: int = 25


def load_query_config(path: str | Path = "config/topics.yml") -> GitHubQueryConfig:
    with Path(path).open("r", encoding="utf-8") as file:
        raw = yaml.safe_load(file)
    return GitHubQueryConfig(
        queries=list(raw.get("queries", [])),
        per_query=int(raw.get("per_query", 25)),
    )


def github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def normalize_repo(item: dict[str, Any]) -> dict[str, Any]:
    license_info = item.get("license") or {}
    return {
        "name": item.get("name"),
        "full_name": item.get("full_name"),
        "html_url": item.get("html_url"),
        "description": item.get("description") or "",
        "language": item.get("language") or "",
        "stargazers_count": item.get("stargazers_count") or 0,
        "forks_count": item.get("forks_count") or 0,
        "open_issues_count": item.get("open_issues_count") or 0,
        "pushed_at": item.get("pushed_at"),
        "license": license_info.get("spdx_id") or "",
        "topics": ";".join(item.get("topics") or []),
        "has_readme": True,
    }


def search_repositories(query: str, per_page: int = 25) -> list[dict[str, Any]]:
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
    }
    response = requests.get(GITHUB_SEARCH_URL, headers=github_headers(), params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return [normalize_repo(item) for item in payload.get("items", [])]


def collect_repositories(config: GitHubQueryConfig) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for query in config.queries:
        rows.extend(search_repositories(query, per_page=config.per_query))
        time.sleep(0.5)

    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.drop_duplicates(subset=["full_name"]).reset_index(drop=True)
