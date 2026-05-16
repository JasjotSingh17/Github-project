
# 📊 GitHub DA Trend Tracker

A data analytics pipeline that tracks the adoption and popularity of Data Analyst tools, frameworks, and technologies using real GitHub repository data.

The project was built to answer a practical question I kept running into while applying for Data Analyst roles:

> *Which tools are genuinely growing in adoption, and which ones are worth prioritising in the modern data ecosystem?*

---

## 🚀 Key Takeaways

* **Python is in a category of its own** — with 14.2M stars and 683k repositories, it dwarfs every other tool in the dataset and was excluded from the quadrant chart as a statistical outlier
* **SQL and relational databases dominate the DA ecosystem** — MySQL (2.8M stars), PostgreSQL (2.8M stars), and SQL (2.4M stars) occupy the top 3 spots after Python and are the only tools classified as Established & Popular alongside it
* **SQLite is the only Rising Challenger in the dataset** — 1.5M stars but only 29k repositories, signalling strong community interest that has not yet translated into broad mainstream adoption
* **Pipeline & Orchestration has the smallest footprint of any category** — nearly invisible on the radar chart, confirming these tools remain concentrated in engineering-heavy environments rather than general analytics roles
* Delivered insights through a **4-page interactive Power BI dashboard** covering tool rankings, adoption quadrants, category comparisons, and ecosystem trends

---

## 📊 Dashboard Preview

### DA Ecosystem Radar — Stars by Skill Category
<img width="1806" height="1166" alt="image" src="https://github.com/user-attachments/assets/c76c9630-3abc-4e5b-bf0e-1f251deab448" />



### Tool Quadrant — Adoption vs Popularity
<img width="2066" height="1186" alt="image" src="https://github.com/user-attachments/assets/88fec549-a372-4fcb-a11a-89894a4b519a" />


### Top 15 DA Tools by Total Stars
<img width="1978" height="1140" alt="image" src="https://github.com/user-attachments/assets/12500f7c-9b42-4927-b08a-36c54f1c2e4f" />


### Full DA Tool Rankings Table
<img width="1484" height="1188" alt="image" src="https://github.com/user-attachments/assets/c127f76b-ffb1-4357-9edd-fb1fd35d8cd9" />


### Total Stars by Category
<img width="1908" height="1180" alt="image" src="https://github.com/user-attachments/assets/6bb34133-2ab0-4ed8-bf8c-0a9008b31952" />


---

## 📌 Problem

As someone actively applying for Data Analyst roles, I kept running into the same problem: job postings are vague about which tools actually matter, and online advice goes stale quickly. I wanted a data-driven answer to a question I was already asking every week.

> *Which DA tools are genuinely embedded in the ecosystem right now, and which ones are worth prioritising?*

This project builds a full ETL pipeline on top of the GitHub Search API to answer that question — tracking 30 tools across 7 skill categories and delivering the findings through a Power BI dashboard.

---

## 🧠 Approach

### 1. Data Extraction

* Queried the **GitHub Search API** across 30 DA-relevant tools and technologies
* Handled API pagination and automatic rate limit recovery
* Stored all raw snapshots in a **SQLite database** for traceability and reproducibility

### 2. Data Cleaning & Structuring

* Cleaned and validated raw API snapshot data before analysis
* Corrected type inconsistencies and removed failed API responses
* Designed a custom taxonomy grouping tools into 7 functional skill categories for ecosystem-level comparison

### 3. SQL-Based Analytics

All analytical transformations were executed directly in SQL inside SQLite — mirroring workflows commonly used in modern analytics engineering environments.

| Transform | SQL Feature Used | Purpose |
| --- | --- | --- |
| Week-over-week growth | `LAG()` window function | Track adoption momentum |
| Tool rankings | `RANK()` window function | Rank tools overall and within categories |
| Quadrant classification | `CASE WHEN` logic | Classify tools by adoption and popularity |
| Category rollups | `GROUP BY` aggregation | Compare ecosystem segments |

### 4. Power BI Dashboard

Exported analytical datasets into Power BI and built a 4-page interactive dashboard covering:

* Tool rankings
* Adoption vs popularity quadrant analysis
* Category-level comparisons
* Ecosystem trend monitoring

---

## 📈 Key Insights

* **Python is a statistical outlier by every measure** — 14.2M stars and 28,381 avg stars per repository, more than 5x the next closest tool (MySQL at 2.8M stars). Excluded from the quadrant chart so other tools remain readable
* **MySQL and PostgreSQL are the only non-language tools classified as Established & Popular** — both sit at 2.8M stars with 87k–93k repositories, confirming relational databases as the non-negotiable foundation of any DA skill set
* **SQLite is the sole Rising Challenger in the entire dataset** — 1.5M stars against only 29k repositories gives it the highest stars-to-repos ratio outside the top 4, suggesting strong and growing community interest ahead of broader adoption
* **Pandas is the only tool classified as Widely Used, Less Celebrated** — 840k stars across 50k repositories places it above the repo median but below the star median, reflecting how embedded it is in everyday work without commanding the same visibility as database tools
* **Languages and Databases & Querying account for the majority of all stars in the ecosystem** — 16.6M and 8.1M respectively, while the remaining 5 categories combined total under 4M. Pipeline & Orchestration is nearly invisible at under 0.1M, confirming it remains a specialist skill area

---

## ⚙️ Tech Stack

| Tool | Role |
| --- | --- |
| Python (Pandas) | API ingestion, cleaning, and pipeline orchestration |
| GitHub Search API | Repository, star, and fork metadata for 30 DA tools |
| SQL / SQLite | Relational storage and analytical transformations |
| Power BI | Dashboarding and interactive visualisation |

---

## 📁 Repository Structure

```text
github-da-trend-tracker/
├── pipeline/           # API ingestion, cleaning, SQL transforms, CSV export
├── data/processed/     # Dashboard-ready analytical datasets
├── config.py           # Pipeline configuration and taxonomy definitions
└── README.md
```

---

## ▶️ How to Run

```bash
# 1. Clone the repository
git clone https://github.com/JasjotSingh17/github-da-trend-tracker.git
cd github-da-trend-tracker

# 2. Install dependencies
pip install requests pandas

# 3. Add your GitHub token to config.py
# Generate a classic token at:
# https://github.com/settings/tokens

# 4. Run the pipeline
python pipeline/01_ingest.py
python pipeline/02_clean.py
python pipeline/03_transform.py
python pipeline/04_load.py
```

> The pipeline handles API pagination and GitHub rate limits automatically. Full execution takes approximately 15–20 minutes.

---

## 👤 Author

**Jasjot Singh**
University of Waterloo — BMath, Mathematical Studies (Minor: Computer Science)
[LinkedIn](https://linkedin.com/in/your-profile) | [j367sing@uwaterloo.ca](mailto:j367sing@uwaterloo.ca)
