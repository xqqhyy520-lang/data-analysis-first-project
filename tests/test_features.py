import pandas as pd

from src.features import career_value_score, detect_skills, recommend_roles


def test_detect_skills_from_topics_and_description():
    row = pd.Series(
        {
            "name": "example-rag-dashboard",
            "description": "A Streamlit dashboard for LLM retrieval analytics",
            "language": "Python",
            "topics": "llm;rag;dashboard;python",
        }
    )

    assert "Python" in detect_skills(row)
    assert "Dashboard" in detect_skills(row)
    assert "LLM / RAG" in detect_skills(row)


def test_recommend_roles_from_skills():
    roles = recommend_roles(["SQL", "Dashboard"])

    assert "Data Analyst" in roles
    assert "BI Analyst" in roles
    assert "AI Data Product" not in roles


def test_score_rewards_practical_repository_signals():
    strong_repo = pd.Series(
        {
            "name": "modern-data-stack",
            "description": "Python SQL dashboard data engineering project",
            "language": "Python",
            "topics": "python;sql;dashboard;data-engineering",
            "stargazers_count": 5000,
            "forks_count": 800,
            "open_issues_count": 20,
            "pushed_at": "2026-06-20T00:00:00Z",
            "license": "MIT",
            "has_readme": True,
        }
    )
    weak_repo = pd.Series(
        {
            "name": "old-script",
            "description": "",
            "language": "",
            "topics": "",
            "stargazers_count": 2,
            "forks_count": 0,
            "open_issues_count": 400,
            "pushed_at": "2020-01-01T00:00:00Z",
            "license": "",
            "has_readme": False,
        }
    )

    assert career_value_score(strong_repo) > career_value_score(weak_repo)
