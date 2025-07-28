import requests
import pandas as pd

ODDS_API_KEY = "4228a71c92cda37ef7c36d88d930bc96"
BASE_URL = "https://api.the-odds-api.com/v4/sports"

def odds_to_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return -odds / (-odds + 100)

def fetch_h2h_odds(sport_key="basketball_nba", region="us", bookmaker="pinnacle"):
    url = f"{BASE_URL}/{sport_key}/odds"
    params = {
        "regions": region,
        "markets": "h2h",
        "oddsFormat": "american",
        "bookmakers": bookmaker,
        "apiKey": ODDS_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return pd.DataFrame()

    data = response.json()
    rows = []

    for event in data:
        event_time = event["commence_time"]
        teams = event["teams"]
        home_team = event["home_team"]

        for book in event.get("bookmakers", []):
            for market in book.get("markets", []):
                if market["key"] == "h2h":
                    outcomes = market.get("outcomes", [])
                    for outcome in outcomes:
                        team = outcome["name"]
                        odds = outcome["price"]
                        prob = odds_to_probability(odds)
                        rows.append({
                            "Match": f"{teams[0]} vs {teams[1]}",
                            "Team": team,
                            "Odds": odds,
                            "ImpliedProb": round(prob, 4),
                            "Bookmaker": book["title"],
                            "StartTime": event_time
                        })

    df = pd.DataFrame(rows)
    return df
