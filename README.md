# Football Data Scraper
Using this tool to scrape data so I can play around with data analysis using football (one of my passions as inspiration).

This project scrapes team-level statistics from FBref.com for Europe's top 5 football leagues using Selenium and pandas. The scraped data is compiled into individual CSV files by league and stat type, and finally merged into a master dataset for analysis (coming soon).

---

## Leagues Covered
- Premier League (England)
- La Liga (Spain)
- Bundesliga (Germany)
- Serie A (Italy)
- Ligue 1 (France)

---

## Stat Types Collected

Each league has the following tables scraped:

| Stat Type        | Description                         |
|------------------|-------------------------------------|
| `stats_standard` | Basic stats (games, wins, goals etc.) |
| `stats_passing`  | Passing metrics                     |
| `stats_shooting` | Shooting statistics                 |
| `stats_possession` | Possession and build-up data      |
| `stats_defense`  | Defensive actions                   |
| `stats_misc`     | Miscellaneous stats (fouls, cards, etc.) |

---

## Output Structure

All data is saved in the `data/` directory:

- Individual files:  
  `Premier_League_stats_standard.csv`, `La_Liga_stats_defense.csv`, etc.

- Merged file:  
  `master_dataset.csv` — a single file combining all leagues and stat types, with two additional columns:
  - `League`: Name of the league
  - `Stat_Type`: Type of stats in that row

---

## How It Works

1. For each league and stat type, a dynamic page is loaded with Selenium.
2. The table is extracted, even if it is wrapped in HTML comments (which FBref uses).
3. Data is saved as individual CSV files.
4. After scraping, all files are merged into `master_dataset.csv`.

---

## Requirements

- Python 3.8+
- Google Chrome
- ChromeDriver (auto-managed via `webdriver-manager`)

### Install dependencies:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```text
selenium
webdriver-manager
pandas
bs4
```

---

## Sample Usage

```python
df = pd.read_csv("data/master_dataset.csv")
# Filter for Premier League shooting stats
pl_shooting = df[(df['League'] == 'Premier League') & (df['Stat_Type'] == 'stats_shooting')]
```

---

## Notes

- This script uses headless Chrome for scraping; ensure Chrome is installed on your system.
- Tables are extracted even if they are embedded inside HTML comments.
- You can easily modify the `LEAGUES` or `STAT_TYPES` dictionaries to scrape other leagues or stats.




## Purpose
Teach myself data analysis using a big dataset, because if I can work on this I believe I can work on anything.
