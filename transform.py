import sqlite3
import pandas as pd
from config import DB_PATH


def run_transforms(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.executescript("""
        DROP VIEW IF EXISTS vw_growth;
        CREATE VIEW vw_growth AS
        SELECT
            topic,
            category,
            snapshot_date,
            total_repos,
            total_stars,
            total_forks,
            avg_stars,
            top_repo_name,
            top_repo_url,

            LAG(total_stars) OVER (
                PARTITION BY topic ORDER BY snapshot_date
            ) AS prev_stars,

            LAG(total_repos) OVER (
                PARTITION BY topic ORDER BY snapshot_date
            ) AS prev_repos,

            ROUND(
                CASE
                    WHEN LAG(total_stars) OVER (PARTITION BY topic ORDER BY snapshot_date) IS NULL THEN NULL
                    WHEN LAG(total_stars) OVER (PARTITION BY topic ORDER BY snapshot_date) = 0    THEN NULL
                    ELSE (
                        CAST(
                            total_stars - LAG(total_stars) OVER (PARTITION BY topic ORDER BY snapshot_date)
                        AS REAL)
                        / LAG(total_stars) OVER (PARTITION BY topic ORDER BY snapshot_date) * 100
                    )
                END
            , 2) AS star_growth_pct,

            ROUND(
                CASE
                    WHEN LAG(total_repos) OVER (PARTITION BY topic ORDER BY snapshot_date) IS NULL THEN NULL
                    WHEN LAG(total_repos) OVER (PARTITION BY topic ORDER BY snapshot_date) = 0    THEN NULL
                    ELSE (
                        CAST(
                            total_repos - LAG(total_repos) OVER (PARTITION BY topic ORDER BY snapshot_date)
                        AS REAL)
                        / LAG(total_repos) OVER (PARTITION BY topic ORDER BY snapshot_date) * 100
                    )
                END
            , 2) AS repo_growth_pct

        FROM clean_snapshots
        ORDER BY topic, snapshot_date;
    """)


    conn.executescript("""
        DROP VIEW IF EXISTS vw_ranked;
        CREATE VIEW vw_ranked AS
        SELECT
            g.*,

            RANK() OVER (
                PARTITION BY snapshot_date
                ORDER BY total_stars DESC
            ) AS rank_by_stars,

            RANK() OVER (
                PARTITION BY snapshot_date
                ORDER BY total_repos DESC
            ) AS rank_by_repos,

            RANK() OVER (
                PARTITION BY snapshot_date, category
                ORDER BY total_stars DESC
            ) AS rank_by_stars_in_category

        FROM vw_growth g;
    """)

    conn.executescript("""
        DROP VIEW IF EXISTS vw_quadrant;
        CREATE VIEW vw_quadrant AS
        WITH medians AS (
            SELECT
                snapshot_date,
                AVG(total_repos)  AS median_repos,
                AVG(total_stars)  AS median_stars
            FROM vw_ranked
            GROUP BY snapshot_date
        )
        SELECT
            r.*,
            CASE
                WHEN r.total_repos >= m.median_repos AND r.total_stars >= m.median_stars THEN 'Established & Popular'
                WHEN r.total_repos >= m.median_repos AND r.total_stars <  m.median_stars THEN 'Widely Used, Less Celebrated'
                WHEN r.total_repos <  m.median_repos AND r.total_stars >= m.median_stars THEN 'Rising Challenger'
                ELSE 'Niche / Emerging'
            END AS quadrant
        FROM vw_ranked r
        LEFT JOIN medians m ON r.snapshot_date = m.snapshot_date;
    """)

    conn.executescript("""
        DROP TABLE IF EXISTS analysis;
        CREATE TABLE analysis AS
        SELECT * FROM vw_quadrant;
    """)

    conn.executescript("""
        DROP TABLE IF EXISTS category_summary;
        CREATE TABLE category_summary AS
        SELECT
            category,
            snapshot_date,
            COUNT(DISTINCT topic)   AS tool_count,
            SUM(total_repos)        AS total_repos,
            SUM(total_stars)        AS total_stars,
            ROUND(AVG(avg_stars),2) AS avg_stars_per_repo
        FROM vw_quadrant
        GROUP BY category, snapshot_date
        ORDER BY total_stars DESC;
    """)

    conn.commit()
    conn.close()

    conn = sqlite3.connect(db_path)
    for t in ["analysis", "category_summary"]:
        n = pd.read_sql(f"SELECT COUNT(*) AS n FROM {t}", conn).iloc[0]["n"]
        print(f"  {t}: {n} rows")
    conn.close()
    print("Transforms complete.")


if __name__ == "__main__":
    run_transforms()