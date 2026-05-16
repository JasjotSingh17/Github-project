import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "my_token")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"

DB_PATH = "da_trends.db"


DA_TOPICS = {
    "Languages": [
        "python", "r-language", "sql", "julia"
    ],
    "Data Manipulation": [
        "pandas", "numpy", "polars", "dplyr", "tidyverse"
    ],
    "Visualisation": [
        "matplotlib", "seaborn", "plotly", "ggplot2",
        "tableau", "powerbi", "looker"
    ],
    "Databases & Querying": [
        "postgresql", "mysql", "sqlite", "duckdb",
        "bigquery", "snowflake", "dbt"
    ],
    "Pipeline & Orchestration": [
        "airflow", "prefect", "dagster", "luigi"
    ],
    "ML & Stats (DA-adjacent)": [
        "scikit-learn", "statsmodels", "xgboost", "lightgbm"
    ],
    "Cloud & Big Data": [
        "spark", "hadoop", "azure-data-factory", "aws-glue"
    ]
}

ALL_TOPICS = [topic for topics in DA_TOPICS.values() for topic in topics]

TOPIC_CATEGORY = {
    topic: category
    for category, topics in DA_TOPICS.items()
    for topic in topics
}