import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def fetch_fbref_table_selenium(url, table_id):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)

        # Explicitly wait for the table to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, table_id)))

        # Now, attempt to fetch the table
        table = driver.find_element(By.ID, table_id)
        if table:
            html = table.get_attribute('outerHTML')
            df = pd.read_html(html)[0]
            return df
        else:
            print(f"❌ Table with ID '{table_id}' not found.")
            return pd.DataFrame()

    finally:
        driver.quit()


# URLs for top 5 European leagues and their corresponding table IDs for all stat types
leagues = {
    "Premier League": {
        "url": "https://fbref.com/en/comps/9/stats/Premier-League-Stats",
        "table_ids": [
            "stats_standard", "stats_passing", "stats_shooting", "stats_possession", 
            "stats_defense", "stats_disciplines", "stats_goalkeeping"
        ]
    },
    "La Liga": {
        "url": "https://fbref.com/en/comps/12/stats/La-Liga-Stats",
        "table_ids": [
            "stats_standard", "stats_passing", "stats_shooting", "stats_possession", 
            "stats_defense", "stats_disciplines", "stats_goalkeeping"
        ]
    },
    "Serie A": {
        "url": "https://fbref.com/en/comps/11/stats/Serie-A-Stats",
        "table_ids": [
            "stats_standard", "stats_passing", "stats_shooting", "stats_possession", 
            "stats_defense", "stats_disciplines", "stats_goalkeeping"
        ]
    },
    "Bundesliga": {
        "url": "https://fbref.com/en/comps/20/stats/Bundesliga-Stats",
        "table_ids": [
            "stats_standard", "stats_passing", "stats_shooting", "stats_possession", 
            "stats_defense", "stats_disciplines", "stats_goalkeeping"
        ]
    },
    "Ligue 1": {
        "url": "https://fbref.com/en/comps/13/stats/Ligue-1-Stats",
        "table_ids": [
            "stats_standard", "stats_passing", "stats_shooting", "stats_possession", 
            "stats_defense", "stats_disciplines", "stats_goalkeeping"
        ]
    }
}

# Scrape each league and stat type, then save to CSV
for league, data in leagues.items():
    print(f"Scraping {league}...")
    
    # For each stat type in the league
    for table_id in data['table_ids']:
        print(f"  - Scraping {table_id}...")
        df = fetch_fbref_table_selenium(data['url'], table_id)

        if not df.empty:
            df.to_csv(f"{league}_{table_id}.csv", index=False)
            print(f"✅ Saved {league} {table_id} to CSV")
        else:
            print(f"❌ Failed to fetch {league} {table_id}")
