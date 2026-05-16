import requests
import sqlite3
import time
import pandas as pd
import os
from datetime import date
from config import HEADERS, GITHUB_SEARCH_URL, ALL_TOPICS, TOPIC_CATEGORY, DB_PATH


def fetch_topic_stats(topic: str, max_pages: int = 5) -> dict:
    """
    Fetches repository data for a given topic from the GitHub Search API.
    Paginates up to 5 pages (500 repos) per topic — enough for meaningful
    aggregation while staying within the API's rate limits across all topics.
    """
    all_repos = []

    for page in range(1, max_pages + 1):
        params = {
            "q": f"topic:{topic}",
            "sort": "stars",
            "order": "desc",
            "per_page": 100,
            "page": page
        }

        try:
            response = requests.get(
                GITHUB_SEARCH_URL, headers=HEADERS, params=params, timeout=15
            )

            # Rate limit hit — sleep until GitHub resets the counter
            if response.status_code == 403:
                reset_time = int(response.headers.get("X-RateLimit-Reset", time.time() + 60))
                sleep_for = max(reset_time - int(time.time()), 10)
                print(f"  Rate limit hit. Sleeping {sleep_for}s...")
                time.sleep(sleep_for)
                continue

            if response.status_code != 200:
                print(f"  Error {response.status_code} on {topic} page {page}. Skipping.")
                break

            data = response.json()
            repos = data.get("items", [])
            if not repos:
                break

            all_repos.extend(repos)
            time.sleep(2)  # always sleep between requests

        except requests.exceptions.Timeout:
            print(f"  Timeout on {topic} page {page}. Moving on.")
            break
        except Exception as e:
            print(f"  Error on {topic} page {page}: {e}")
            break

    if not all_repos:
        return {}

    stars = [r.get("stargazers_count", 0) for r in all_repos]
    forks = [r.get("forks_count", 0) for r in all_repos]
    top   = all_repos[0]

    return {
        "topic":          topic,
        "category":       TOPIC_CATEGORY.get(topic, "Other"),
        "snapshot_date":  str(date.today()),
        "total_repos":    data.get("total_count", 0),
        "total_stars":    sum(stars),
        "total_forks":    sum(forks),
        "avg_stars":      round(sum(stars) / len(stars), 2) if stars else 0,
        "avg_forks":      round(sum(forks) / len(forks), 2) if forks else 0,
        "top_repo_name":  top.get("full_name", ""),
        "top_repo_stars": top.get("stargazers_count", 0),
        "top_repo_url":   top.get("html_url", ""),
    }


def save_to_db(records: list, db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    df = pd.DataFrame(records)
    df.to_sql("raw_snapshots", conn, if_exists="replace", index=False)
    conn.close()
    print(f"\nIngestion complete. {len(records)} topics saved to raw_snapshots.")


if __name__ == "__main__":
    print("Starting ingestion...\n")
    records = []

    for topic in ALL_TOPICS:
        print(f"Fetching: {topic}...")
        stats = fetch_topic_stats(topic)
        if stats:
            records.append(stats)
        else:
            print(f"  No data for {topic}. Skipping.")

    if records:
        save_to_db(records)
    else:
        print("No records collected. Check your GITHUB_TOKEN.")