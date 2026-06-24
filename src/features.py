from __future__ import annotations

from datetime import datetime, timezone
from math import log1p
from typing import Iterable

import pandas as pd


SKILL_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Python": ("python", "pandas", "numpy", "scikit", "fastapi", "streamlit", "gradio"),
    "SQL": ("sql", "duckdb", "postgres", "database", "warehouse", "dbt"),
    "Dashboard": ("dashboard", "visualization", "streamlit", "plotly", "superset", "bi"),
    "Machine Learning": ("machine-learning", "ml", "modeling", "scikit", "statistics"),
    "LLM / RAG": ("llm", "rag", "agent", "langchain", "retrieval", "generative-ai"),
    "Data Engineering": ("data-engineering", "etl", "workflow", "orchestration", "airflow"),
    "MLOps": ("mlops", "deployment", "monitoring", "pipeline", "production"),
}

def split_topics(value: object) -> list[str]:
    if value is None or pd.isna(value):
        return []
    if isinstance(value, list):
        return [str(item).strip().lower() for item in value if str(item).strip()]
    return [item.strip().lower() for item in str(value).split(";") if item.strip()]


def repository_text(row: pd.Series) -> str:
    parts: Iterable[str] = (
        row.get("name", ""),
        row.get("full_name", ""),
        row.get("description", ""),
        row.get("language", ""),
        " ".join(split_topics(row.get("topics", ""))),
    )
    return " ".join(str(part).lower() for part in parts if part)


def detect_skills(row: pd.Series) -> list[str]:
    text = repository_text(row)
    skills: list[str] = []
    for skill, keywords in SKILL_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            skills.append(skill)
    return skills


def recommend_roles(skills: Iterable[str]) -> list[str]:
    skill_set = set(skills)
    roles: list[str] = []

    if {"SQL", "Dashboard"}.intersection(skill_set):
        roles.append("Data Analyst")
    if "Machine Learning" in skill_set and "Python" in skill_set:
        roles.append("Data Scientist")
    if "Data Engineering" in skill_set or {"SQL", "Python"}.issubset(skill_set):
        roles.append("Data Engineer")
    if {"SQL", "Dashboard"}.issubset(skill_set):
        roles.append("BI Analyst")
    if "LLM / RAG" in skill_set:
        roles.append("AI Data Product")

    return roles or ["General Data Portfolio"]


def days_since_push(pushed_at: object, now: datetime | None = None) -> int:
    if now is None:
        now = datetime.now(timezone.utc)
    if pushed_at is None or pd.isna(pushed_at):
        return 3650
    parsed = pd.to_datetime(pushed_at, utc=True, errors="coerce")
    if pd.isna(parsed):
        return 3650
    return max((now - parsed.to_pydatetime()).days, 0)


def career_value_score(row: pd.Series) -> float:
    stars = max(float(row.get("stargazers_count", 0) or 0), 0)
    forks = max(float(row.get("forks_count", 0) or 0), 0)
    issues = max(float(row.get("open_issues_count", 0) or 0), 0)
    skills = detect_skills(row)
    recency_days = days_since_push(row.get("pushed_at"))

    popularity = min(log1p(stars) / log1p(120_000), 1.0) * 35
    community = min(log1p(forks) / log1p(30_000), 1.0) * 15
    recency = max(0.0, 1 - min(recency_days, 365) / 365) * 20
    learning_value = min(len(skills), 5) / 5 * 20
    documentation = 5 if bool(row.get("has_readme", False)) else 0
    licensing = 5 if str(row.get("license", "")).strip() else 0
    issue_penalty = min(log1p(issues) / log1p(5_000), 1.0) * 8

    return round(popularity + community + recency + learning_value + documentation + licensing - issue_penalty, 2)


def enrich_repositories(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    enriched["skills"] = enriched.apply(lambda row: "; ".join(detect_skills(row)), axis=1)
    enriched["recommended_roles"] = enriched["skills"].apply(lambda value: "; ".join(recommend_roles(value.split("; "))))
    enriched["days_since_push"] = enriched["pushed_at"].apply(days_since_push)
    enriched["career_value_score"] = enriched.apply(career_value_score, axis=1)
    return enriched.sort_values("career_value_score", ascending=False).reset_index(drop=True)
