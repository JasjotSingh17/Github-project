import pandas as pd
import sqlite3
from config import DB_PATH, TOPIC_CATEGORY


def load_raw(db_path: str = DB_PATH) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM raw_snapshots", conn)
    conn.close()
    print(f"Loaded {len(df)} raw rows.")
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    original = len(df)

    df["snapshot_date"]  = pd.to_datetime(df["snapshot_date"])
    df["total_repos"]    = pd.to_numeric(df["total_repos"],    errors="coerce").fillna(0).astype(int)
    df["total_stars"]    = pd.to_numeric(df["total_stars"],    errors="coerce").fillna(0).astype(int)
    df["total_forks"]    = pd.to_numeric(df["total_forks"],    errors="coerce").fillna(0).astype(int)
    df["avg_stars"]      = pd.to_numeric(df["avg_stars"],      errors="coerce").fillna(0)
    df["avg_forks"]      = pd.to_numeric(df["avg_forks"],      errors="coerce").fillna(0)
    df["top_repo_stars"] = pd.to_numeric(df["top_repo_stars"], errors="coerce").fillna(0).astype(int)


    before = len(df)
    df = df[~((df["total_repos"] == 0) & (df["total_stars"] == 0))]
    print(f"Dropped {before - len(df)} zero-value rows.")

    df["category"] = df["topic"].map(TOPIC_CATEGORY).fillna("Other")

    df["topic"]         = df["topic"].str.strip().str.lower()
    df["top_repo_name"] = df["top_repo_name"].str.strip()
    df["top_repo_url"]  = df["top_repo_url"].str.strip()

    df = df.reset_index(drop=True)
    print(f"Cleaning complete. {original} → {len(df)} rows retained.")
    return df


def save_clean(df: pd.DataFrame, db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    df.to_sql("clean_snapshots", conn, if_exists="replace", index=False)
    conn.close()
    print(f"clean_snapshots saved: {len(df)} rows.")


if __name__ == "__main__":
    raw = load_raw()
    cleaned = clean(raw)
    save_clean(cleaned)