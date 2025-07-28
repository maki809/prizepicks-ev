import pandas as pd

def calculate_ev(prizepicks_df, odds_df, projection_source="sharp"):
    """
    Merge PrizePicks props with sportsbook odds and calculate EV & edge.
    
    Parameters:
        prizepicks_df: DataFrame with PrizePicks props (from scraper.py)
        odds_df: DataFrame with odds and implied probabilities (from odds_fetcher.py)
        projection_source: "sharp" or "custom"

    Returns:
        DataFrame with EV, Edge, ImpliedProb, and merged fields.
    """

    # Standardize names for rough merge — this can be enhanced with fuzzy matching
    prizepicks_df['PlayerLower'] = prizepicks_df['Player'].str.lower().str.replace(".", "").str.strip()
    odds_df['TeamLower'] = odds_df['Team'].str.lower().str.strip()

    # TEMP: simulate projections using sharp odds as proxy
    odds_df['ProjProb'] = odds_df['ImpliedProb']  # Later, plug in your own model here

    # Merge PrizePicks with Book Odds (match by Team or fuzzy player names later)
    merged_df = pd.merge(prizepicks_df, odds_df, left_on='Team', right_on='Team', how='inner')

    # Calculate EV & Edge
    # PrizePicks payout for 2-pick = 3x, 3-pick = 5x, 6-pick = 25x etc. Adjust as needed.
    payout_multiplier = 3.0  # You can change this based on pick combo

    merged_df['EV'] = (merged_df['ProjProb'] * payout_multiplier) - (1 - merged_df['ProjProb'])
    merged_df['Edge'] = merged_df['ProjProb'] - merged_df['ImpliedProb']

    return merged_df[[
        'Player', 'Stat', 'Line', 'Team', 'Sport',
        'Odds', 'ImpliedProb', 'ProjProb', 'EV', 'Edge', 'Bookmaker'
    ]].sort_values(by='EV', ascending=False)
