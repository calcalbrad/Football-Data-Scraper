import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, Comment
import pandas as pd


LEAGUES = {
    "Premier League": "https://fbref.com/en/comps/9",
    "La Liga": "https://fbref.com/en/comps/12",
    "Bundesliga": "https://fbref.com/en/comps/20",
    "Serie A": "https://fbref.com/en/comps/11",
    "Ligue 1": "https://fbref.com/en/comps/13"
}


STAT_TYPES = {
    "stats_standard": "stats",
    "stats_passing": "passing",
    "stats_shooting": "shooting",
    "stats_possession": "possession",
    "stats_defense": "defense",
    "stats_misc": "misc"
}


def fetch_fbref_table_selenium(url, table_id):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, table_id)))
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", {"id": table_id})
        if table:
            df = pd.read_html(str(table))[0]
            driver.quit()
            return df

        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            if table_id in comment:
                comment_soup = BeautifulSoup(comment, "html.parser")
                table = comment_soup.find("table", {"id": table_id})
                if table:
                    df = pd.read_html(str(table))[0]
                    driver.quit()
                    return df

        driver.quit()
        return None

    except Exception as e:
        print(f"Error with {table_id}: {e}")
        driver.quit()
        return None


for league_name, base_url in LEAGUES.items():
    print(f"\nScraping {league_name}...")

    for table_id, path in STAT_TYPES.items():
        url = f"{base_url}/{path}/{league_name.replace(' ', '-')}-Stats"
        print(f"  - Scraping {table_id} from {url}...")

        df = fetch_fbref_table_selenium(url, table_id)
        if df is not None:
            os.makedirs("data", exist_ok=True)
            filename = f"data/{league_name.replace(' ', '_')}_{table_id}.csv"
            df.to_csv(filename, index=False)
            print(f"    Saved to {filename}")
        else:
            print(f"    Failed to scrape {table_id}")
