from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.collect_github import collect_repositories, load_query_config
from src.features import enrich_repositories


RAW_PATH = Path("data/raw/repositories.csv")
PROCESSED_PATH = Path("data/processed/repository_scores.csv")
SAMPLE_PATH = Path("data/sample_repositories.csv")


def load_sample() -> pd.DataFrame:
    return pd.read_csv(SAMPLE_PATH)


def run_pipeline(use_sample: bool = False, fresh: bool = False) -> pd.DataFrame:
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)

    if use_sample:
        raw = load_sample()
    elif fresh or not RAW_PATH.exists():
        config = load_query_config()
        raw = collect_repositories(config)
        raw.to_csv(RAW_PATH, index=False)
    else:
        raw = pd.read_csv(RAW_PATH)

    enriched = enrich_repositories(raw)
    enriched.to_csv(PROCESSED_PATH, index=False)
    return enriched


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build GitHub repository career-value scores.")
    parser.add_argument("--use-sample", action="store_true", help="Use the bundled sample dataset.")
    parser.add_argument("--fresh", action="store_true", help="Collect fresh data from the GitHub API.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    result = run_pipeline(use_sample=args.use_sample, fresh=args.fresh)
    print(result[["full_name", "career_value_score", "skills", "recommended_roles"]].head(10))
