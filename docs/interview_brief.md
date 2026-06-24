# Interview Brief

## Project pitch

GitHub Data Career Radar is a data analytics project that collects public
metadata from GitHub repositories related to data science, machine learning,
data engineering, BI, and AI applications. It transforms repository signals into
a career-value score and maps each project to data-related roles.

The project helps early-career candidates answer a practical question:

> Which open-source projects are worth studying if I want to prepare for data
> roles in large technology companies?

## What I built

- A GitHub data collection pipeline using the GitHub Search API.
- A data-cleaning and feature-engineering module for repository metadata.
- A transparent scoring model based on popularity, activity, documentation,
  licensing, and skill relevance.
- A role-mapping system for Data Analyst, Data Scientist, Data Engineer, BI
  Analyst, and AI Data Product roles.
- An interactive Streamlit dashboard for ranking and exploration.
- Unit tests for the scoring and skill-mapping logic.

## Why it is different from a beginner project

This project is not a static CSV exercise. It uses live public data, has a
repeatable pipeline, defines a scoring methodology, and presents results through
an interactive product-style dashboard. It also connects technical analysis with
career decision-making, which makes it easier to explain in interviews.

## Skills demonstrated

- Python data analysis with pandas.
- API data collection and JSON normalization.
- Feature engineering and scoring design.
- Data visualization with Plotly and Streamlit.
- Basic software engineering practices: modular code, requirements, tests, and
  project documentation.
- Product thinking for data career planning.

## Possible interview answer

I built GitHub Data Career Radar because I wanted to choose portfolio projects
based on real open-source trends instead of guessing what is popular. The system
collects repositories from the GitHub Search API, cleans the metadata, detects
skill tags from descriptions and topics, calculates a career-value score, and
maps each repository to data-related roles. I also built a Streamlit dashboard so
users can filter repositories by score, language, and target role.

The most important design decision was making the score transparent. I combined
stars, forks, update recency, README/license signals, skill relevance, and an
issue penalty. The result is not a perfect quality ranking, but it is useful for
screening projects that are active, popular, and relevant to job preparation.

## Next improvements

- Add job description scraping for Chinese big-tech data roles.
- Compare repository skills with job description skills.
- Track weekly score changes.
- Add natural-language summaries for each repository README.
- Deploy the dashboard publicly.

## 中文面试讲法

这个项目叫 GitHub Data Career Radar，目标是帮助数据岗位求职者从真实开源趋势中选择值得学习和改进的项目。我用 GitHub Search API 采集数据科学、机器学习、数据工程、BI 和 AI 应用相关的仓库元数据，然后做清洗、特征工程和评分。

评分体系不是只看 star，而是综合考虑 star、fork、更新时间、README、license、技能相关性和 issue 风险。最后我用 Streamlit 做了一个交互式 dashboard，可以按照岗位方向、语言和分数筛选项目。

这个项目体现了我的数据获取、数据清洗、指标设计、可视化、产品化表达和基础工程能力。它也和我的求职目标相关：我希望进入数据相关岗位，所以这个项目既是一个技术作品，也是一个辅助职业规划的数据工具。
