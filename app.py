import streamlit as st
from scraper import scrape_prizepicks
from odds_fetcher import fetch_h2h_odds
from ev_model import calculate_ev

st.set_page_config(page_title="PrizePicks +EV Optimizer", layout="wide")

st.title("🎯 PrizePicks +EV Optimizer")
st.caption("Live edge tool using sharp sportsbook odds")

# Sidebar options
sport = st.sidebar.selectbox("Choose a Sport", ["nba", "nfl", "mlb", "wnba"])
edge_threshold = st.sidebar.slider("Minimum Edge (%)", 0.0, 0.25, 0.05, 0.01)
max_picks = st.sidebar.slider("Max Picks to Build Combo", 2, 6, 6)

# Step 1: Scrape PrizePicks props
with st.spinner("Scraping PrizePicks..."):
    pp_df = scrape_prizepicks(sport=sport, num_scrolls=10)

# Step 2: Get sharp odds
with st.spinner("Fetching sharp odds..."):
    odds_df = fetch_h2h_odds(sport_key=f"{sport}_nba" if sport == "nba" else f"{sport}")

# Step 3: Calculate EV
ev_df = calculate_ev(pp_df, odds_df)

# Step 4: Filter +EV picks
ev_df = ev_df[ev_df["Edge"] >= edge_threshold]

st.subheader("📈 +EV PrizePicks Props")
st.dataframe(ev_df, use_container_width=True)

# Combo builder
st.subheader(f"🧮 Build {max_picks}-Pick Combo")
combo_df = ev_df.head(max_picks)

if not combo_df.empty:
    st.table(combo_df[["Player", "Stat", "Line", "EV", "Edge"]])
    ev_total = (combo_df["ProjProb"].prod()) * 25  # 6-pick payout logic (25x)
    st.success(f"Projected 6-Pick EV: {ev_total:.2f}x return")

# Download as CSV
csv = ev_df.to_csv(index=False)
st.download_button("Download Picks CSV", csv, file_name="ev_picks.csv", mime="text/csv")
