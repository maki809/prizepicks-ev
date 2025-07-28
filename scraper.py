import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def scrape_prizepicks(sport="nba", num_scrolls=10):
    options = uc.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)
    url = f"https://app.prizepicks.com/"
    driver.get(url)

    time.sleep(5)  # Wait for site to load fully

    # Click the sport tab (NBA, NFL, etc.)
    try:
        sport_tab = driver.find_element(By.XPATH, f"//div[text()='{sport.upper()}']")
        sport_tab.click()
        time.sleep(2)
    except Exception as e:
        print(f"Sport '{sport}' not found. Error: {e}")
        driver.quit()
        return pd.DataFrame()

    # Scroll to load props
    for _ in range(num_scrolls):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(1.5)

    # Scrape all player cards
    props = []
    player_cards = driver.find_elements(By.CLASS_NAME, "player-card")

    for card in player_cards:
        try:
            player_name = card.find_element(By.CLASS_NAME, "name").text.strip()
            stat_category = card.find_element(By.CLASS_NAME, "stat").text.strip()
            prop_line = float(card.find_element(By.CLASS_NAME, "score").text.strip())
            team = card.find_element(By.CLASS_NAME, "team").text.strip()

            props.append({
                "Player": player_name,
                "Stat": stat_category,
                "Line": prop_line,
                "Team": team,
                "Sport": sport.upper()
            })
        except Exception:
            continue

    driver.quit()

    df = pd.DataFrame(props)
    return df
