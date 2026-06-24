from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.pipeline import PROCESSED_PATH, run_pipeline


st.set_page_config(
    page_title="GitHub Data Career Radar",
    page_icon="GD",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    if not PROCESSED_PATH.exists():
        return run_pipeline(use_sample=True)
    return pd.read_csv(PROCESSED_PATH)


def explode_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    temp = df[["full_name", column]].copy()
    temp[column] = temp[column].fillna("").str.split("; ")
    return temp.explode(column).query(f"{column} != ''")


data = load_data()

st.title("GitHub Data Career Radar")
st.caption("Open-source trend analytics for data career planning")

with st.sidebar:
    st.header("Filters")
    min_score = st.slider("Minimum career value score", 0, 100, 50)
    languages = sorted(data["language"].dropna().unique().tolist())
    selected_languages = st.multiselect("Languages", languages, default=languages)
    role_options = sorted(set("; ".join(data["recommended_roles"].fillna("")).split("; ")))
    selected_roles = st.multiselect("Target roles", role_options, default=role_options)

filtered = data[
    (data["career_value_score"] >= min_score)
    & (data["language"].isin(selected_languages))
    & (data["recommended_roles"].fillna("").apply(lambda roles: any(role in roles for role in selected_roles)))
].copy()

metric_cols = st.columns(4)
metric_cols[0].metric("Repositories", f"{len(filtered):,}")
metric_cols[1].metric("Median score", f"{filtered['career_value_score'].median():.1f}" if not filtered.empty else "0")
metric_cols[2].metric("Total stars", f"{int(filtered['stargazers_count'].sum()):,}" if not filtered.empty else "0")
metric_cols[3].metric("Languages", f"{filtered['language'].nunique():,}" if not filtered.empty else "0")

left, right = st.columns((1.2, 1))

with left:
    st.subheader("Top repositories")
    display_columns = [
        "full_name",
        "career_value_score",
        "language",
        "stargazers_count",
        "forks_count",
        "skills",
        "recommended_roles",
        "html_url",
    ]
    st.dataframe(
        filtered[display_columns].sort_values("career_value_score", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

with right:
    st.subheader("Score vs. stars")
    fig = px.scatter(
        filtered,
        x="stargazers_count",
        y="career_value_score",
        color="language",
        size="forks_count",
        hover_name="full_name",
        log_x=True,
    )
    st.plotly_chart(fig, use_container_width=True)

skill_counts = explode_column(filtered, "skills")["skills"].value_counts().reset_index()
skill_counts.columns = ["skill", "repositories"]

role_counts = explode_column(filtered, "recommended_roles")["recommended_roles"].value_counts().reset_index()
role_counts.columns = ["role", "repositories"]

chart_cols = st.columns(2)
with chart_cols[0]:
    st.subheader("Skill demand signals")
    st.plotly_chart(
        px.bar(skill_counts, x="repositories", y="skill", orientation="h", text="repositories"),
        use_container_width=True,
    )

with chart_cols[1]:
    st.subheader("Role relevance")
    st.plotly_chart(
        px.bar(role_counts, x="repositories", y="role", orientation="h", text="repositories"),
        use_container_width=True,
    )

st.subheader("Portfolio interpretation")
st.write(
    "Use the highest-scoring repositories as learning references, not copy targets. "
    "A strong portfolio project should add original analysis, a clear user scenario, "
    "and transparent methodology."
)

if st.button("Rebuild sample dataset"):
    run_pipeline(use_sample=True)
    st.cache_data.clear()
    st.rerun()
