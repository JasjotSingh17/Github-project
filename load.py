import pandas as pd
import sqlite3
import os
from config import DB_PATH


def load(table: str, db_path: str = DB_PATH) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df


def export_full_analysis(db_path: str = DB_PATH):
    """
    Full analysis table — primary Power BI data source.
    One row per tool with all metrics, rankings, and quadrant label.
    """
    df = load("analysis", db_path)
    cols = [
        "topic", "category", "snapshot_date",
        "total_repos", "total_stars", "total_forks", "avg_stars",
        "rank_by_stars", "rank_by_repos", "rank_by_stars_in_category",
        "quadrant", "top_repo_name", "top_repo_url"
    ]
    cols = [c for c in cols if c in df.columns]
    df[cols].to_csv("data/processed/full_analysis.csv", index=False)
    print(f"full_analysis.csv: {len(df)} rows")


def export_category_summary(db_path: str = DB_PATH):
    """
    Category-level rollup.
    Used for bar chart and radar chart in Power BI.
    """
    df = load("category_summary", db_path)
    df.to_csv("data/processed/category_summary.csv", index=False)
    print(f"category_summary.csv: {len(df)} rows")


def export_top_per_category(db_path: str = DB_PATH):
    """
    Top 3 tools by total_stars within each category.
    Used for the category leaderboard visual in Power BI.
    Pre-aggregated here so Power BI doesn't need TOPN logic.
    """
    conn = sqlite3.connect(db_path)
    query = """
        SELECT
            topic,
            category,
            total_repos,
            total_stars,
            avg_stars,
            rank_by_stars_in_category,
            quadrant,
            top_repo_name,
            top_repo_url
        FROM analysis
        WHERE rank_by_stars_in_category <= 3
        ORDER BY category, rank_by_stars_in_category;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df.to_csv("data/processed/top_per_category.csv", index=False)
    print(f"top_per_category.csv: {len(df)} rows")


def export_quadrant_summary(db_path: str = DB_PATH):
    """
    Count of tools per quadrant.
    Used for the quadrant donut / summary card in Power BI.
    """
    conn = sqlite3.connect(db_path)
    query = """
        SELECT
            quadrant,
            COUNT(*) AS tool_count,
            SUM(total_repos) AS total_repos,
            SUM(total_stars) AS total_stars
        FROM analysis
        GROUP BY quadrant
        ORDER BY tool_count DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df.to_csv("data/processed/quadrant_summary.csv", index=False)
    print(f"quadrant_summary.csv: {len(df)} rows")


if __name__ == "__main__":
    os.makedirs("data/processed", exist_ok=True)

    export_full_analysis()
    export_category_summary()
    export_top_per_category()
    export_quadrant_summary()

    print("\nAll CSVs exported to data/processed/ — ready for Power BI.")