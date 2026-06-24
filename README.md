# GitHub Data Career Radar

An analytics project that tracks trending GitHub repositories in data science,
machine learning, data engineering, and AI, then maps open-source signals to
skills commonly required by data-related roles.

This project is designed as a portfolio-ready data project for students and
early-career candidates targeting data analyst, data scientist, data engineer,
BI analyst, and AI data product roles.

## Why this project matters

Many beginner data projects stop at a static CSV analysis. This project uses a
real external data source, builds a repeatable data pipeline, defines a scoring
methodology, and turns the results into a dashboard that can support career
planning decisions.

The core question:

> Which GitHub data and AI projects are worth learning from if I want to prepare
> for competitive data roles?

## Features

- Collects repositories from the GitHub Search API by topic and keyword.
- Builds a clean repository dataset with stars, forks, issues, language, topics,
  license, update recency, and README availability signals.
- Calculates a transparent `career_value_score`.
- Maps repositories to practical skill tags such as Python, SQL, dashboarding,
  machine learning, LLM, RAG, data engineering, and MLOps.
- Recommends suitable target roles for each repository.
- Provides an interactive Streamlit dashboard for exploration.
- Includes tests for the scoring and skill-mapping logic.

## Project structure

```text
.
├── app.py
├── config
│   └── topics.yml
├── data
│   └── sample_repositories.csv
├── src
│   ├── __init__.py
│   ├── collect_github.py
│   ├── features.py
│   └── pipeline.py
├── tests
│   └── test_features.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Quick start

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run the pipeline with the included sample data:

```bash
python -m src.pipeline --use-sample
```

Run the dashboard:

```bash
streamlit run app.py
```

To collect fresh data from GitHub:

```bash
python -m src.pipeline --fresh
```

Optional: set a GitHub token to increase API rate limits.

```bash
set GITHUB_TOKEN=your_token_here
```

## Methodology

The `career_value_score` combines several signals:

- Popularity: stars and forks.
- Activity: recently updated repositories receive higher scores.
- Maintainability: repositories with a license and README signal better learning value.
- Practicality: repositories with role-relevant skill tags receive higher scores.
- Risk control: very high open issue counts slightly reduce the score.

The score is not intended to rank project quality perfectly. It is a practical
screening score for students choosing projects to study, reproduce, and improve.

## Example career use cases

- Find projects worth reading before applying to data analyst internships.
- Identify which tools appear frequently in modern AI/data repositories.
- Select portfolio project ideas with stronger industry relevance.
- Compare data science, data engineering, and AI application directions.

## Ethics and attribution

This project does not copy code from the repositories it analyzes. It only uses
public repository metadata and points users to original repositories for further
study. Always respect each repository's license before reusing code.

## Roadmap

- Add Chinese big-tech job description skill matching.
- Track weekly repository score changes.
- Add natural-language README summaries.
- Add a bilingual project report for portfolio presentation.
