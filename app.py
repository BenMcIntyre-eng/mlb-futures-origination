from __future__ import annotations
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import requests
from datetime import datetime, date

st.set_page_config(page_title="MLB Futures Origination", page_icon="⚾",
                   layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Roboto+Condensed:wght@400;700&family=Source+Code+Pro:wght@400;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Roboto Condensed', sans-serif;
    background-color: #f5f0e8;
    color: #1a2e1a;
}
.stApp { background-color: #f5f0e8; }

/* ── Subtle diamond/stitch texture overlay ── */
.stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image:
        radial-gradient(circle at 25px 25px, rgba(26,46,26,0.04) 2px, transparent 2px),
        radial-gradient(circle at 75px 75px, rgba(26,46,26,0.04) 2px, transparent 2px);
    background-size: 100px 100px;
}

/* ── Title ── */
h1 { font-family: 'Playfair Display', serif !important; font-size: 2.2rem !important;
     font-weight: 900 !important; color: #1a2e1a !important; letter-spacing: -0.02em;
     text-transform: uppercase; border-bottom: 3px solid #1a2e1a; padding-bottom: 8px;
     margin-bottom: 4px !important; }
h2, h3 { font-family: 'Playfair Display', serif !important; color: #1a2e1a !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #1a2e1a !important;
    border-right: 4px solid #c8a84b;
}
[data-testid="stSidebar"] * { color: #f5f0e8 !important; }
[data-testid="stSidebar"] h2 {
    font-family: 'Playfair Display', serif !important;
    color: #c8a84b !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
[data-testid="stSidebar"] .stSlider [data-testid="stMarkdownContainer"] p {
    font-family: 'Source Code Pro', monospace !important;
    font-size: 0.75rem !important;
    color: #a8c5a8 !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: #c8a84b !important;
    color: #1a2e1a !important;
    border: 2px solid #c8a84b !important;
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-radius: 4px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #e8c86a !important;
    border-color: #e8c86a !important;
}

/* ── Section header in sidebar ── */
.section-header {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.65rem; font-weight: 600; color: #c8a84b;
    text-transform: uppercase; letter-spacing: 0.15em;
    margin: 20px 0 10px; padding-bottom: 6px;
    border-bottom: 1px solid rgba(200,168,75,0.35);
}

/* ── Metric cards ── */
.metric-card {
    background: #fff8ee;
    border: 1.5px solid #1a2e1a;
    border-radius: 4px;
    padding: 12px 16px; margin-bottom: 8px;
    box-shadow: 3px 3px 0 #1a2e1a;
}
.metric-label {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.6rem; color: #5a7a5a;
    text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 4px;
}
.metric-value {
    font-family: 'Source Code Pro', monospace;
    font-size: 1.15rem; font-weight: 600; color: #1a2e1a;
}

/* ── Status indicators ── */
.status-ok  { color: #2a6a2a; font-family: 'Source Code Pro', monospace; font-size: .8rem; }
.status-err { color: #8b2020; font-family: 'Source Code Pro', monospace; font-size: .8rem; }

/* ── Main Refresh button ── */
.stButton > button {
    background: #1a2e1a;
    color: #f5f0e8;
    border: 2px solid #1a2e1a;
    border-radius: 4px;
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 9px 20px;
    width: 100%;
    transition: all 0.15s;
    box-shadow: 2px 2px 0 #c8a84b;
}
.stButton > button:hover {
    background: #c8a84b;
    border-color: #c8a84b;
    color: #1a2e1a;
    box-shadow: 2px 2px 0 #1a2e1a;
}

/* ── Market group radio pill strip ── */
div[role="radiogroup"] { display:flex; gap:6px; flex-wrap:wrap; margin-bottom:16px; }
/* Market group pills */
div[role="radiogroup"] { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:16px; }
div[role="radiogroup"] > label {
    display: flex !important; align-items: center; justify-content: center;
    background: #2a4a2a; border: 2px solid #1a2e1a; border-radius: 8px;
    padding: 10px 28px; min-width: 160px;
    font-family: 'Playfair Display', serif;
    font-size: 0.88rem !important; font-weight: 700 !important;
    color: #ffffff !important; cursor: pointer; margin: 0 !important;
    text-transform: uppercase; letter-spacing: 0.08em;
    box-shadow: 3px 3px 0 rgba(0,0,0,0.3);
    transition: all 0.12s;
}
/* Hide the radio dot entirely */
div[role="radiogroup"] > label > div:first-child { display:none !important; }
div[role="radiogroup"] > label svg { display:none !important; }
div[role="radiogroup"] input[type="radio"] { display:none !important; }
/* Per-button colours */
div[role="radiogroup"] > label:nth-child(1) { background:#2a4a2a; border-color:#1a2e1a; box-shadow:3px 3px 0 #0d1a0d; }
div[role="radiogroup"] > label:nth-child(2) { background:#1e3a5f; border-color:#0f1e3a; box-shadow:3px 3px 0 #0a1428; }
div[role="radiogroup"] > label:nth-child(3) { background:#5f1e1e; border-color:#3a0f0f; box-shadow:3px 3px 0 #2a0a0a; }
div[role="radiogroup"] > label:hover { filter:brightness(1.15); transform:translateY(-1px); }
/* Force text inside label to be white */
div[role="radiogroup"] > label p,
div[role="radiogroup"] > label span,
div[role="radiogroup"] > label div { color: #ffffff !important; }

/* ── Collapse gap between margin number_input and the HTML panel below it ── */
/* Target: the element-container holding the column with number_input, zero its bottom margin */
.stTabs [data-baseweb="tab-panel"] .stColumn:first-child .stNumberInput {
    margin-bottom: 0 !important;
}
.stTabs [data-baseweb="tab-panel"] .stColumn:first-child .element-container {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}
/* Also collapse the columns container row itself */
.stTabs [data-baseweb="tab-panel"] .stHorizontalBlock {
    margin-bottom: -12px !important;
    gap: 0 !important;
}
/* Pull the stHtml element up */
.stTabs [data-baseweb="tab-panel"] .stHtml {
    margin-top: 0 !important;
}

/* ── Inner market tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: transparent;
    border-bottom: 2px solid #1a2e1a;
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    background: #e8e0d0;
    border: 1.5px solid #1a2e1a;
    border-bottom: none;
    border-radius: 4px 4px 0 0;
    color: #5a7a5a;
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 0.82rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.05em;
    padding: 6px 16px;
}
.stTabs [aria-selected="true"] {
    background: #1a2e1a !important;
    border-color: #1a2e1a !important;
    color: #c8a84b !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: #d0c8b8 !important;
    color: #1a2e1a !important;
}

/* ── Dataframe / table ── */
[data-testid="stDataFrame"] {
    border: 1.5px solid #1a2e1a !important;
    border-radius: 4px !important;
    overflow: hidden;
}
[data-testid="stDataFrame"] thead th {
    background: #1a2e1a !important;
    color: #c8a84b !important;
    font-family: 'Source Code Pro', monospace !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stDataFrame"] tbody td {
    font-family: 'Source Code Pro', monospace !important;
    font-size: 0.82rem !important;
    color: #1a2e1a !important;
    background: #fff8ee !important;
}
[data-testid="stDataFrame"] tbody tr:nth-child(even) td {
    background: #f0e8d8 !important;
}
[data-testid="stDataFrame"] tbody tr:hover td {
    background: #e8c86a33 !important;
}

/* ── Margin slider ── */
.stSlider [data-testid="stThumbValue"] {
    font-family: 'Source Code Pro', monospace !important;
    font-size: 0.75rem !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  ODDS LADDER  (columns U/V from spreadsheet)
# ═══════════════════════════════════════════════════════════
DEC_LADDER = [
    1.0001,1.0002,1.0005,1.001,1.002,1.005,1.005263158,1.005555556,1.005882353,
    1.00625,1.006666667,1.007142857,1.007692308,1.008333333,1.009090909,1.01,
    1.010526316,1.011111111,1.011764706,1.0125,1.013333333,1.014285714,1.015384615,
    1.016666667,1.018181818,1.02,1.021052632,1.022222222,1.023529412,1.025,
    1.026666667,1.028571429,1.030769231,1.033333333,1.034482759,1.035714286,
    1.037037037,1.038461538,1.04,1.041666667,1.043478261,1.045454545,1.047619048,
    1.05,1.052631579,1.055555556,1.058823529,1.0625,1.066666667,1.071428571,
    1.076923077,1.083333333,1.090909091,1.095238095,1.1,1.102564103,1.105263158,
    1.108108108,1.111111111,1.112359551,1.113636364,1.114942529,1.11627907,
    1.117647059,1.119047619,1.120481928,1.12195122,1.12345679,1.125,1.126582278,
    1.128205128,1.12987013,1.131578947,1.133333333,1.135135135,1.136986301,
    1.138888889,1.14084507,1.142857143,1.144927536,1.147058824,1.149253731,
    1.151515152,1.153846154,1.15625,1.158730159,1.161290323,1.163934426,
    1.166666667,1.168067227,1.169491525,1.170940171,1.172413793,1.173913043,
    1.175438596,1.17699115,1.178571429,1.18018018,1.181818182,1.183486239,
    1.185185185,1.186915888,1.188679245,1.19047619,1.192307692,1.194174757,
    1.196078431,1.198019802,1.2,1.202020202,1.204081633,1.206185567,1.208333333,
    1.210526316,1.212765957,1.215053763,1.217391304,1.21978022,1.222222222,
    1.224719101,1.227272727,1.229885057,1.23255814,1.235294118,1.238095238,
    1.240963855,1.243902439,1.24691358,1.25,1.253164557,1.256410256,1.25974026,
    1.263157895,1.266666667,1.285714286,1.289855072,1.294117647,1.298507463,
    1.303030303,1.307692308,1.3125,1.317460317,1.322580645,1.327868852,
    1.333333333,1.350877193,1.357142857,1.363636364,1.37037037,1.377358491,
    1.384615385,1.392156863,1.4,1.408163265,1.416666667,1.425531915,1.434782609,
    1.444444444,1.454545455,1.465116279,1.476190476,1.487804878,1.5,1.512820513,
    1.526315789,1.540540541,1.555555556,1.571428571,1.588235294,1.606060606,
    1.625,1.64516129,1.666666667,1.689655172,1.714285714,1.740740741,1.769230769,
    1.8,1.833333333,1.869565217,1.909090909,1.952380952,2.0,2.05,2.1,2.15,2.2,
    2.25,2.3,2.35,2.4,2.45,2.5,2.55,2.6,2.65,2.7,2.75,2.8,2.85,2.9,2.95,3.0,
    3.05,3.1,3.15,3.2,3.25,3.3,3.35,3.4,3.45,3.5,3.55,3.6,3.65,3.7,3.75,3.8,
    3.85,3.9,3.95,4.0,4.05,4.1,4.15,4.2,4.25,4.3,4.35,4.4,4.45,4.5,4.55,4.6,
    4.65,4.7,4.75,4.8,4.85,4.9,4.95,5.0,5.05,5.1,5.15,5.2,5.25,5.3,5.35,5.4,
    5.45,5.5,5.55,5.6,5.65,5.7,5.75,5.8,5.85,5.9,5.95,6.0,6.05,6.1,6.15,6.2,
    6.25,6.3,6.35,6.4,6.45,6.5,6.55,6.6,6.65,6.7,6.75,6.8,6.85,6.9,6.95,7.0,
    7.1,7.2,7.3,7.4,7.5,7.6,7.7,7.8,7.9,8.0,8.1,8.2,8.3,8.4,8.5,8.6,8.7,8.8,
    8.9,9.0,9.1,9.2,9.3,9.4,9.5,9.6,9.7,9.8,9.9,10.0,10.25,10.5,10.75,11.0,
    11.25,11.5,11.75,12.0,13.0,14.0,15.0,16.0,17.0,18.0,18.5,19.0,20.0,21.0,
    22.0,23.0,23.5,24.0,25.0,26.0,27.0,28.0,29.0,30.0,31.0,33.5,36.0,38.5,
    41.0,43.5,46.0,48.5,51.0,56.0,61.0,66.0,71.0,76.0,81.0,86.0,91.0,96.0,
    101.0,111.0,121.0,131.0,141.0,151.0,161.0,171.0,181.0,191.0,201.0,251.0,
    301.0,401.0,501.0,601.0,701.0,801.0,901.0,1001.0,
]

def snap_decimal(true_price) -> float | None:
    """Snap true price to nearest ladder decimal odds (1/true_price → nearest ladder value)."""
    try:
        p = float(true_price)
    except Exception:
        return None
    if not np.isfinite(p) or p <= 0:
        return None
    target = 1.0 / p
    return min(DEC_LADDER, key=lambda x: abs(x - target))

def dec_to_american(dec: float) -> str:
    if dec is None or dec <= 1:
        return "—"
    v = round((dec - 1) * 100) if dec >= 2 else round(-100 / (dec - 1))
    return f"+{v}" if v > 0 else str(v)

# ═══════════════════════════════════════════════════════════
#  TEAM NAME NORMALISATION
# ═══════════════════════════════════════════════════════════
_ALIASES: dict[str, list[str]] = {
    "Los Angeles Dodgers":    ["LA Dodgers","LAD","Dodgers"],
    "New York Yankees":       ["NY Yankees","NYY","Yankees"],
    "Atlanta Braves":         ["ATL Braves","ATL","Braves"],
    "Seattle Mariners":       ["SEA Mariners","SEA","Mariners"],
    "Philadelphia Phillies":  ["PHI Phillies","PHI","Phillies"],
    "Detroit Tigers":         ["DET Tigers","DET","Tigers"],
    "New York Mets":          ["NY Mets","NYM","Mets"],
    "Texas Rangers":          ["TEX Rangers","TEX","Rangers"],
    "Baltimore Orioles":      ["BAL Orioles","BAL","Orioles"],
    "Chicago Cubs":           ["CHI Cubs","CHC","Cubs"],
    "Boston Red Sox":         ["BOS Red Sox","BOS","Red Sox"],
    "Pittsburgh Pirates":     ["PIT Pirates","PIT","Pirates"],
    "Toronto Blue Jays":      ["TOR Blue Jays","TOR","Blue Jays"],
    "Milwaukee Brewers":      ["MIL Brewers","MIL","Brewers"],
    "Tampa Bay Rays":         ["TB Rays","TBR","Rays"],
    "Houston Astros":         ["HOU Astros","HOU","Astros"],
    "San Diego Padres":       ["SD Padres","SDP","Padres"],
    "Kansas City Royals":     ["KC Royals","KCR","Royals"],
    "Minnesota Twins":        ["MIN Twins","MIN","Twins"],
    "Cleveland Guardians":    ["CLE Guardians","CLE","Guardians"],
    "Arizona Diamondbacks":   ["ARI Diamondbacks","ARI","Diamondbacks"],
    "Cincinnati Reds":        ["CIN Reds","CIN","Reds"],
    "Athletics":              ["Athletics","ATH","OAK"],
    "San Francisco Giants":   ["SF Giants","SFG","Giants"],
    "Los Angeles Angels":     ["LA Angels","LAA","Angels"],
    "Miami Marlins":          ["MIA Marlins","MIA","Marlins"],
    "St. Louis Cardinals":    ["STL Cardinals","STL","Cardinals"],
    "Chicago White Sox":      ["CHI White Sox","CHW","White Sox"],
    "Washington Nationals":   ["WAS Nationals","WSN","Nationals"],
    "Colorado Rockies":       ["COL Rockies","COL","Rockies"],
}
_LOOKUP: dict[str, str] = {}
for canon, aliases in _ALIASES.items():
    _LOOKUP[canon.lower()] = canon
    for a in aliases:
        _LOOKUP[a.lower()] = canon

def norm(name: str) -> str:
    return _LOOKUP.get(str(name).strip().lower(), str(name).strip())

# ═══════════════════════════════════════════════════════════
#  SCRAPER CONFIG
# ═══════════════════════════════════════════════════════════
FD_API_KEY = (st.secrets.get("FD_API_KEY", None) or "FhMFpcPWXMeyZxOx")  # override via secrets.toml in prod

MARKETS = {
    "World Series":    {"fd_tabs":[("mlb-futures","world-series-winner"),("mlb","world-series-winner")],
                        "dk_ids":["17279"],"fg_col":"Win WS %"},
    "AL Winner":       {"fd_tabs":[("mlb-futures","league-winner"),("mlb","al-pennant-winner")],
                        "dk_ids":["17172"],"fg_col":"Win LCS %","league":"AL"},
    "NL Winner":       {"fd_tabs":[("mlb-futures","league-winner"),("mlb","nl-pennant-winner")],
                        "dk_ids":["17172"],"fg_col":"Win LCS %","league":"NL"},
    "AL East":         {"fd_tabs":[("mlb-futures","division-winner"),("mlb","division-winner")],
                        "dk_ids":["17290"],"fg_col":"Win Div %","division":"AL East"},
    "AL Central":      {"fd_tabs":[("mlb-futures","division-winner"),("mlb","division-winner")],
                        "dk_ids":["17290"],"fg_col":"Win Div %","division":"AL Central"},
    "AL West":         {"fd_tabs":[("mlb-futures","division-winner"),("mlb","division-winner")],
                        "dk_ids":["17290"],"fg_col":"Win Div %","division":"AL West"},
    "NL East":         {"fd_tabs":[("mlb-futures","division-winner"),("mlb","division-winner")],
                        "dk_ids":["17290"],"fg_col":"Win Div %","division":"NL East"},
    "NL Central":      {"fd_tabs":[("mlb-futures","division-winner"),("mlb","division-winner")],
                        "dk_ids":["17290"],"fg_col":"Win Div %","division":"NL Central"},
    "NL West":         {"fd_tabs":[("mlb-futures","division-winner"),("mlb","division-winner")],
                        "dk_ids":["17290"],"fg_col":"Win Div %","division":"NL West"},
    "Make Playoffs AL":{"fd_tabs":[("mlb-futures","to-make-the-playoffs"),("mlb","make-playoffs")],
                        "dk_ids":["17184"],"fg_col":"Make Playoffs %","league":"AL"},
    "Miss Playoffs AL":{"fd_tabs":[("mlb-futures","to-miss-the-playoffs"),("mlb","miss-playoffs")],
                        "dk_ids":["17184"],"fg_col":"Miss Playoffs %","league":"AL"},
    "Make Playoffs NL":{"fd_tabs":[("mlb-futures","to-make-the-playoffs"),("mlb","make-playoffs")],
                        "dk_ids":["17184"],"fg_col":"Make Playoffs %","league":"NL"},
    "Miss Playoffs NL":{"fd_tabs":[("mlb-futures","to-miss-the-playoffs"),("mlb","miss-playoffs")],
                        "dk_ids":["17184"],"fg_col":"Miss Playoffs %","league":"NL"},
}

DIV_TEAMS = {
    "AL East":    ["New York Yankees","Baltimore Orioles","Boston Red Sox","Toronto Blue Jays","Tampa Bay Rays"],
    "AL Central": ["Detroit Tigers","Minnesota Twins","Cleveland Guardians","Kansas City Royals","Chicago White Sox"],
    "AL West":    ["Seattle Mariners","Texas Rangers","Houston Astros","Athletics","Los Angeles Angels"],
    "NL East":    ["Atlanta Braves","Philadelphia Phillies","New York Mets","Miami Marlins","Washington Nationals"],
    "NL Central": ["Pittsburgh Pirates","Chicago Cubs","Milwaukee Brewers","Cincinnati Reds","St. Louis Cardinals"],
    "NL West":    ["Los Angeles Dodgers","San Diego Padres","Arizona Diamondbacks","San Francisco Giants","Colorado Rockies"],
}
AL_TEAMS = set(t for d in ["AL East","AL Central","AL West"] for t in DIV_TEAMS[d])
NL_TEAMS = set(t for d in ["NL East","NL Central","NL West"] for t in DIV_TEAMS[d])

# DK market IDs — stable for 2026 season, used instead of name matching
DK_MARKET_ID_MAP = {
    "286076444": "World Series",
    "287265157": "AL Winner",
    "287265753": "NL Winner",
    "301102608": "AL East",
    "301102693": "AL Central",
    "301102810": "AL West",
    "301102845": "NL East",
    "301102886": "NL Central",
    "301103051": "NL West",
    # Make/Miss Playoffs: per-team markets, routed by outcome_type
}

FD_MKT_KEYS = {
    "World Series":  ["world series 2026 winner","world series winner"],
    "AL Winner":     ["american league 2026 winner","american league winner"],
    "NL Winner":     ["national league 2026 winner","national league winner"],
    "AL East":       ["al east 2026 winner"],
    "AL Central":    ["al central 2026 winner"],
    "AL West":       ["al west 2026 winner"],
    "NL East":       ["nl east 2026 winner"],
    "NL Central":    ["nl central 2026 winner"],
    "NL West":       ["nl west 2026 winner"],
    "Make Playoffs AL": ["to make the playoffs","make playoffs"],
    "Miss Playoffs AL": ["to miss the playoffs","miss playoffs"],
    "Make Playoffs NL": ["to make the playoffs","make playoffs"],
    "Miss Playoffs NL": ["to miss the playoffs","miss playoffs"],
}

# ═══════════════════════════════════════════════════════════
#  MATH HELPERS
# ═══════════════════════════════════════════════════════════
def remove_margin(s: pd.Series) -> pd.Series:
    t = s.sum()
    return s / t if t > 0 else s

def fmt_pct(x) -> str:
    try:
        return f"{float(x):.2%}" if pd.notna(x) else "—"
    except Exception:
        return "—"

# ═══════════════════════════════════════════════════════════
#  SCRAPERS
# ═══════════════════════════════════════════════════════════
@st.cache_data(ttl=300, show_spinner=False)
def scrape_fanduel(state: str) -> pd.DataFrame:
    base = f"https://sbapi.{state}.sportsbook.fanduel.com/api/content-managed-page"
    rows = []
    all_pages = set()
    for cfg in MARKETS.values():
        for p, t in cfg["fd_tabs"]:
            all_pages.add((p, t))

    session = requests.Session()
    session.headers["Accept"] = "application/json"
    for page, tab in all_pages:
        params = {"betexRegion":"GBR","capiJurisdiction":"intl","currencyCode":"USD",
                  "exchangeLocale":"en_US","includePrices":"true","language":"en",
                  "regionCode":"NAMERICA","_ak":FD_API_KEY,"page":"CUSTOM",
                  "customPageId":page,"tab":tab}
        try:
            r = session.get(base, params=params, timeout=15)
            if r.status_code != 200:
                continue
            data = r.json()
        except Exception:
            continue
        for m in data.get("attachments",{}).get("markets",{}).values():
            mname = (m.get("marketName") or m.get("name") or "").strip()
            for runner in m.get("runners",[]):
                wo = runner.get("winRunnerOdds") or {}
                dec = ((wo.get("trueOdds") or {}).get("decimalOdds",{}).get("decimalOdds")
                       or (wo.get("decimalDisplayOdds") or {}).get("decimalOdds"))
                team = runner.get("runnerName","").strip()
                if team and dec:
                    try:
                        rows.append({"team":norm(team),"market":mname.lower(),"dec":float(dec)})
                    except Exception:
                        pass
    return pd.DataFrame(rows) if rows else pd.DataFrame(columns=["team","market","dec"])


@st.cache_data(ttl=300, show_spinner=False)
def scrape_fangraphs() -> pd.DataFrame:
    today = date.today().strftime("%Y-%m-%d")
    api_url = ("https://www.fangraphs.com/api/playoff-odds/odds"
               f"?dateEnd={today}&dateDelta=&projectionMode=2&standingsType=div")
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.fangraphs.com/standings/playoff-odds",
        "Origin": "https://www.fangraphs.com",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
    }
    # Visit the page first to get cookies, then hit the API
    session = requests.Session()
    session.headers.update(headers)
    try:
        session.get("https://www.fangraphs.com/standings/playoff-odds",
                    timeout=15, allow_redirects=True)
    except Exception:
        pass
    resp = session.get(api_url, timeout=20)
    resp.raise_for_status()
    if not resp.text.strip():
        raise ValueError("FanGraphs returned empty response")
    raw = resp.json()
    rows = []
    dl = {"E":"East","C":"Central","W":"West"}
    for t in raw:
        lg = (t.get("league") or "").upper()
        dv = (t.get("division") or "").upper()
        division = f"{lg} {dl.get(dv,dv)}".strip()
        ed = t.get("endData") or {}
        def fp(v):
            try:
                x = float(v)
                return x/100 if x > 1 else x
            except Exception:
                return np.nan
        # Convert miss playoffs am odds → probability
        def _am_to_prob(odds_val):
            try:
                o = float(odds_val)
                if o < 0: return abs(o) / (abs(o) + 100)
                return 100 / (o + 100)
            except Exception: return np.nan
        rows.append({"team":norm(t.get("shortName","")),"division":division,
                     "Win WS %":fp(ed.get("wsWin")),"Win LCS %":fp(ed.get("csWin")),
                     "Win Div %":fp(ed.get("divTitle")),"Make Playoffs %":fp(ed.get("poffTitle")),
                     "Miss Playoffs %":_am_to_prob(t.get("missPlayoffsOdds"))
                     if t.get("missPlayoffsOdds") is not None
                     else (1 - fp(ed.get("poffTitle"))) if fp(ed.get("poffTitle")) is not None else np.nan})
    return pd.DataFrame(rows)


@st.cache_data(ttl=300, show_spinner=False)
def scrape_draftkings() -> pd.DataFrame:
    all_ids = set(sid for cfg in MARKETS.values() for sid in cfg["dk_ids"])
    headers = {"Accept":"application/json,text/html,*/*","Accept-Language":"en-US,en;q=0.9","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36","sec-fetch-dest":"empty","sec-fetch-mode":"cors","sec-fetch-site":"same-site"}
    rows = []
    DK_LEAGUE = "84240"
    for sub_id in all_ids:
        url = ("https://sportsbook-nash.draftkings.com/sites/US-SB/api/sportscontent"
               "/controldata/league/leagueSubcategory/v1/markets")
        params = {
            "isBatchable":"false","templateVars":f"{DK_LEAGUE},{sub_id}",
            "eventsQuery":f"$filter=leagueId eq '{DK_LEAGUE}' AND clientMetadata/Subcategories/any(s: s/Id eq '{sub_id}')",
            "marketsQuery":f"$filter=clientMetadata/subCategoryId eq '{sub_id}' AND tags/all(t: t ne 'SportcastBetBuilder')",
            "include":"Events","entity":"events",
        }
        try:
            r = requests.get(url, params=params, headers=headers, timeout=15)
            if r.status_code != 200:
                continue
            data = r.json()
        except Exception:
            continue
        mmap = {m["id"]: m["name"] for m in data.get("markets",[])}
        for sel in data.get("selections",[]):
            dec = (sel.get("displayOdds") or {}).get("decimal")
            team = sel.get("label","").strip()
            mid  = str(sel.get("marketId","")).split(".")[0]
            mname = mmap.get(sel.get("marketId"),"")
            otype = sel.get("outcomeType","")
            if team and dec:
                try:
                    rows.append({"team":norm(team),"market":mname.lower(),
                                 "market_id":mid,"dec":float(dec),"outcome_type":otype})
                except Exception:
                    pass
    return pd.DataFrame(rows) if rows else pd.DataFrame(columns=["team","market","market_id","dec","outcome_type"])


# ═══════════════════════════════════════════════════════════
#  BUILD ONE MARKET TABLE
#  Replicates spreadsheet formula exactly:
#    H  = FG true prob (raw, already normalised by FG)
#    L  = FD true prob = (1/FD_dec) / sum(1/FD_dec)
#    P  = DK true prob = (1/DK_dec) / sum(1/DK_dec)
#    G  = raw blend    = (H*6 + L*2 + P*2) / 10
#    F  = true price   = MAX(G/sum(G)*1.225, 1/501)
#    D  = ladder-snapped decimal  (nearest to 1/F)
#    C  = ladder-snapped american (from D)
# ═══════════════════════════════════════════════════════════
def build_market(mkt_name: str, cfg: dict,
                 fd_df: pd.DataFrame, fg_df: pd.DataFrame,
                 dk_df: pd.DataFrame,
                 margin_mult: float = 1.225) -> pd.DataFrame | None:
    invert = cfg.get("invert", False)

    # ── FanGraphs ──────────────────────────────────────────
    fg_col = cfg["fg_col"]
    fg = fg_df[["team", fg_col, "division"]].copy().rename(columns={fg_col: "fg_raw"})
    fg["fg_raw"] = pd.to_numeric(fg["fg_raw"], errors="coerce")

    if "division" in cfg:
        fg = fg[fg["team"].isin(DIV_TEAMS.get(cfg["division"], []))]
    elif "league" in cfg:
        fg = fg[fg["team"].isin(AL_TEAMS if cfg["league"] == "AL" else NL_TEAMS)]

    fg = fg[fg["fg_raw"].notna() & (fg["fg_raw"] >= 0)].copy()
    if fg.empty:
        return None

    # For mutual-exclusivity markets (WS/league/div), re-normalise FG.
    # For binary per-team playoffs, each prob is independent — use as-is.
    _is_playoffs = mkt_name in ("Make Playoffs AL","Miss Playoffs AL",
                               "Make Playoffs NL","Miss Playoffs NL")
    fg["H"] = fg["fg_raw"] if _is_playoffs else remove_margin(fg["fg_raw"])

    # ── FanDuel → L ────────────────────────────────────────
    fd_keys = FD_MKT_KEYS.get(mkt_name, [])
    fd_sub = fd_df[fd_df["market"].apply(lambda m: any(k in m for k in fd_keys))].copy()
    if not fd_sub.empty:
        fd_grp = fd_sub.groupby("team")["dec"].mean().reset_index()
        fd_grp = fd_grp[fd_grp["team"].isin(fg["team"])]  # fg already filtered by league
        fd_grp["implied"] = 1.0 / fd_grp["dec"]
        # L = implied / SUM(implied)  — normalise per market
        total_fd = fd_grp["implied"].sum()
        # For mutually-exclusive markets: L = K / sum(K), sums to 1.0
        # For playoff markets: L = K / $K$133 where $K$133 ≈ 1.057
        #   (the NL West FD overround — a fixed normaliser in the spreadsheet)
        #   We compute it as total_fd / n_teams so that sum(L) ≈ n_teams / 1.057
        #   The constant 1.057 is approximated per-team by dividing by expected playoff count
        _PLAYOFF_FD_CONST = 1.057  # matches $K$133 from spreadsheet
        _fd_denom = _PLAYOFF_FD_CONST if _is_playoffs else total_fd
        fd_grp["L"] = fd_grp["implied"] / _fd_denom if _fd_denom > 0 else fd_grp["implied"]
        fd_map      = dict(zip(fd_grp["team"], fd_grp["L"]))
        fd_impl_map = dict(zip(fd_grp["team"], fd_grp["implied"]))  # raw K
        fd_overround = total_fd  # sum(K) = overround
    else:
        fd_map = {}
        fd_impl_map = {}
        fd_overround = np.nan

    # ── DraftKings → P ─────────────────────────────────────
    if mkt_name in ("Make Playoffs AL","Miss Playoffs AL","Make Playoffs NL","Miss Playoffs NL"):
        # DK: one market per team e.g. "mlb 2026 - ny yankees to make the playoffs"
        # outcome_type is "Yes" for make, "No" for miss
        outcome = "Yes" if mkt_name.startswith("Make") else "No"
        league  = "AL" if "AL" in mkt_name else "NL"
        league_teams = AL_TEAMS if league == "AL" else NL_TEAMS
        dk_sub = dk_df[
            dk_df["market"].apply(lambda m: "to make the playoffs" in m) &
            (dk_df["outcome_type"] == outcome)
        ].copy()
        if not dk_sub.empty:
            def _team_from_mkt(m):
                m = m.lower()
                start = m.find(" - ") + 3 if " - " in m else 0
                end   = m.find(" to make the playoffs")
                return norm(m[start:end].strip()) if end > start else ""
            dk_sub = dk_sub.copy()
            dk_sub["team"] = dk_sub["market"].apply(_team_from_mkt)
            dk_sub = dk_sub[dk_sub["team"].isin(league_teams)]
    else:
        # Use market ID for exact routing — eliminates all name-matching ambiguity
        target_id = {v: k for k, v in DK_MARKET_ID_MAP.items()}.get(mkt_name)
        if target_id and "market_id" in dk_df.columns:
            dk_sub = dk_df[dk_df["market_id"] == target_id].copy()
        else:
            dk_sub = pd.DataFrame(columns=dk_df.columns)

    if not dk_sub.empty:
        dk_grp = dk_sub.groupby("team")["dec"].mean().reset_index()
        dk_grp = dk_grp[dk_grp["team"].isin(fg["team"])]
        dk_grp["implied"] = 1.0 / dk_grp["dec"]
        total_dk = dk_grp["implied"].sum()
        _PLAYOFF_DK_CONST = 1.071  # matches $O$133 from spreadsheet
        _dk_denom = _PLAYOFF_DK_CONST if _is_playoffs else total_dk
        dk_grp["P"] = dk_grp["implied"] / _dk_denom if _dk_denom > 0 else dk_grp["implied"]
        dk_map      = dict(zip(dk_grp["team"], dk_grp["P"]))
        dk_impl_map = dict(zip(dk_grp["team"], dk_grp["implied"]))  # raw O
        dk_overround = total_dk  # sum(O) = overround
    else:
        dk_map = {}
        dk_impl_map = {}
        dk_overround = np.nan

    # ── Blend: G = (H*6 + L*2 + P*2) / 10 ────────────────
    # Also store raw dec odds for FD/DK display
    fd_dec_map = {t: 1.0/v if v > 0 else np.nan for t, v in fd_impl_map.items()}
    dk_dec_map = {t: 1.0/v if v > 0 else np.nan for t, v in dk_impl_map.items()}

    records = []
    for _, row in fg.iterrows():
        team = row["team"]
        H = row["H"]
        L = fd_map.get(team, np.nan)
        P = dk_map.get(team, np.nan)

        # Weighted blend — if source missing, redistribute weight to FG
        # FG weight always counts (even if H=0) so zero-prob teams are preserved
        sources = [(H, 6), (L, 2), (P, 2)]
        tw, wp = 0.0, 0.0
        for val, w in sources:
            try:
                vf = float(val)
                if np.isfinite(vf) and vf >= 0:
                    # Only count source if it's FG (always valid) or a book (only if > 0)
                    if w == 6 or vf > 0:
                        wp += vf * w
                        tw += w
            except Exception:
                pass
        G = wp / tw if tw > 0 else 0.0  # zero blend → floor will handle it
        K = fd_impl_map.get(team, np.nan)   # raw FD implied = 1/FD_dec
        O = dk_impl_map.get(team, np.nan)   # raw DK implied = 1/DK_dec
        fd_dec = fd_dec_map.get(team, np.nan)
        dk_dec = dk_dec_map.get(team, np.nan)
        records.append({"team": team, "H": H, "L": L, "P": P, "G": G,
                        "K": K, "O": O, "fd_dec": fd_dec, "dk_dec": dk_dec})

    out = pd.DataFrame(records)
    if out.empty or out["G"].isna().all():
        return None

    # ── True price ─────────────────────────────────────────
    # Mutual-exclusivity markets: F = MAX(G/SUM(G)*margin, 1/501)
    # Playoffs: F = MIN(MAX(G/WS_sum*1.055, 1/501), 0.999)
    #   where WS_sum = sum of G column for 30 World Series teams
    if _is_playoffs:
        # New spreadsheet: F = MIN(MAX(G/SUM(own_G)*mult, 1/501), 99.9/100)
        # Divides by the playoff market's OWN G sum, then multiplies by large factor
        # (6.3 for Make, 9.45/9.4 for Miss). The margin_mult slider holds that factor.
        # e.g. Make AL: G/sum(G)*6.3  →  default margin_mult = 7.3 (530%+1)
        sum_G = out["G"].sum()
        if sum_G <= 0:
            return None
        out["F"] = (out["G"] / sum_G * margin_mult).clip(lower=1/501, upper=0.999)
    else:
        sum_G = out["G"].sum()
        if sum_G <= 0:
            return None
        out["F"] = (out["G"] / sum_G * margin_mult).clip(lower=1/501)

    # ── Ladder-snap decimal & american ─────────────────────
    out["Blended Dec"] = out["F"].apply(snap_decimal)
    out["Blended Am"]  = out["Blended Dec"].apply(
        lambda d: dec_to_american(d) if (d is not None and isinstance(d, float) and np.isfinite(d)) else "—")

    # ── FBG Margin = 1/D (implied from ladder-snapped dec) ─
    out["E"] = out["Blended Dec"].apply(lambda d: 1.0/d if d and d > 0 else np.nan)

    # Store market-level overrounds for metric cards
    out.attrs["fd_overround"]  = fd_overround
    out.attrs["dk_overround"]  = dk_overround
    out.attrs["fbg_overround"] = out["E"].sum()

    out = out.sort_values("F", ascending=False).reset_index(drop=True)
    out.index = range(1, len(out) + 1)

    # Convert FD/DK raw implied back to american odds for display
    def _am(dec):
        try:
            d = float(dec)
            if not np.isfinite(d) or d <= 1: return np.nan
            return round((d-1)*100) if d >= 2 else round(-100/(d-1))
        except Exception:
            return np.nan

    out["fd_am"]  = out["fd_dec"].apply(_am)
    out["dk_am"]  = out["dk_dec"].apply(_am)

    # Rename to match spreadsheet columns exactly
    # Spreadsheet: Team | DK Name | FBG Am | FBG Dec | FBG Margin | FBG True Price |
    #              Raw Blend | FG True Prob | FD Am | FD Dec | FD Margin | FD True Prob |
    #              DK Am | DK Dec | DK Margin | DK True Prob
    out = out.rename(columns={
        "H": "FG True Prob",
        "L": "FD True Prob",  "K": "FD Margin",  "fd_dec": "FD Dec", "fd_am": "FD Am Odds",
        "P": "DK True Prob",  "O": "DK Margin",  "dk_dec": "DK Dec", "dk_am": "DK Am Odds",
        "G": "True Price",
        "E": "FBG Margin",
        "F": "_true_price_internal",  # keep for sorting/floor but not displayed
    })
    return out[["team",
                "Blended Am", "Blended Dec",
                "FD Am Odds", "FD Dec",
                "DK Am Odds", "DK Dec",
                # keep for attrs / overround calcs
                "FBG Margin", "True Price", "FG True Prob",
                "FD Margin", "FD True Prob", "DK Margin", "DK True Prob"]]


# ═══════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════
for k, v in [("last_refresh",None),("tables",{}),("status",{}),("errors",{}),
             ("raw_fg",None),("raw_fd",None),("raw_dk",None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════
#  SIDEBAR  (no FD state field)
# ═══════════════════════════════════════════════════════════
TEAM_NICKNAMES = {
    "New York Yankees": "Yankees",    "Baltimore Orioles": "Orioles",
    "Boston Red Sox": "Red Sox",      "Tampa Bay Rays": "Rays",
    "Toronto Blue Jays": "Blue Jays", "Chicago White Sox": "White Sox",
    "Cleveland Guardians": "Guardians","Detroit Tigers": "Tigers",
    "Kansas City Royals": "Royals",   "Minnesota Twins": "Twins",
    "Houston Astros": "Astros",       "Los Angeles Angels": "Angels",
    "Athletics": "Athletics",         "Seattle Mariners": "Mariners",
    "Texas Rangers": "Rangers",       "Atlanta Braves": "Braves",
    "Miami Marlins": "Marlins",       "New York Mets": "Mets",
    "Philadelphia Phillies": "Phillies","Washington Nationals": "Nationals",
    "Chicago Cubs": "Cubs",           "Cincinnati Reds": "Reds",
    "Milwaukee Brewers": "Brewers",   "Pittsburgh Pirates": "Pirates",
    "St. Louis Cardinals": "Cardinals","Arizona Diamondbacks": "D-backs",
    "Colorado Rockies": "Rockies",    "Los Angeles Dodgers": "Dodgers",
    "San Diego Padres": "Padres",     "San Francisco Giants": "Giants",
}

# Per-market margin defaults — overround% convention: margin_mult = pct/100
# WS: 123% → 1.23x, Divisions: 111% → 1.11x, Make PO: 630% → 6.3x
MARKET_MARGIN_DEFAULTS = {
    "World Series":     123.0,
    "AL Winner":        117.5, "NL Winner":        117.0,
    "AL East":          111.0, "AL Central":       111.0, "AL West":        111.0,
    "NL East":          111.0, "NL Central":       111.0, "NL West":        106.0,
    "Make Playoffs AL": 630.0, "Miss Playoffs AL": 945.0,
    "Make Playoffs NL": 630.0, "Miss Playoffs NL": 940.0,
}

# Declare the bidirectional margin component from local HTML file
import os as _os
_COMPONENT_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "margin_component")
_margin_ctrl = components.declare_component("margin_panel", path=_COMPONENT_DIR)

def _margin_component(panel_html: str, margin_pct: float, input_key: str, n_rows: int):
    """Render odds panel with interactive margin controls via declared component.
    Returns new margin value when changed by user, else None."""
    row_h = 44
    height = 98 + (n_rows * row_h) + 34
    result = _margin_ctrl(
        panel_html=panel_html,
        margin_pct=margin_pct,
        input_key=input_key,
        key=f"mc_{input_key}",
        default=None,
        height=height,
    )
    if result is not None:
        try:
            return float(result)
        except (TypeError, ValueError):
            return None
    return None


# Reset stale margin session state (old convention: 1+pct/100, new: pct/100)
# If a WS margin is stored as 23 instead of 123, reset it
for _mk, _def in MARKET_MARGIN_DEFAULTS.items():
    _sk = f"margin_{_mk.replace(' ','_')}"
    if _sk in st.session_state:
        _sv = float(st.session_state[_sk])
        if _sv < _def * 0.5 or _sv > _def * 2.0:
            st.session_state[_sk] = _def

with st.sidebar:
    st.markdown("""
    <div style="padding:8px 0 12px;">
      <div style="font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:900;
                  color:#c8a84b;text-transform:uppercase;letter-spacing:0.06em;">
        ⚾ Futures
      </div>
      <div style="font-family:'Source Code Pro',monospace;font-size:0.6rem;
                  color:#7a9a7a;letter-spacing:0.15em;text-transform:uppercase;
                  margin-top:2px;">Origination Desk</div>
    </div>
    <hr style="border:none;border-top:1px solid rgba(200,168,75,0.4);margin:0 0 12px;">
    """, unsafe_allow_html=True)
    st.markdown('<div class="section-header">Blend Weights</div>', unsafe_allow_html=True)
    w_fg = st.slider("FanGraphs",  0.0, 1.0, 0.60, 0.05)
    w_fd = st.slider("FanDuel",    0.0, 1.0, 0.20, 0.05)
    w_dk = st.slider("DraftKings", 0.0, 1.0, 0.20, 0.05)

    # Weights must sum to 1 for the 6/2/2 ratio to stay correct
    total_w = round(w_fg + w_fd + w_dk, 4)
    if abs(total_w - 1.0) > 0.01:
        st.warning(f"Weights sum to {total_w:.2f} — auto-normalised.")
    # Convert to /10 parts matching spreadsheet
    w_parts = {"fg": w_fg/total_w*10 if total_w else 6,
               "fd": w_fd/total_w*10 if total_w else 2,
               "dk": w_dk/total_w*10 if total_w else 2}

    st.markdown("---")
    refresh_btn = st.button("🔄  Refresh All Sources")

    if st.session_state["status"]:
        st.markdown('<div class="section-header">Source Status</div>', unsafe_allow_html=True)
        for src, ok in st.session_state["status"].items():
            cls  = "status-ok" if ok else "status-err"
            icon = "✓" if ok else "✗"
            st.markdown(f'<span class="{cls}">{icon} {src}</span>', unsafe_allow_html=True)
        if st.session_state["errors"]:
            with st.expander("Errors"):
                for s, m in st.session_state["errors"].items():
                    st.code(f"{s}: {m}")
    if st.session_state["last_refresh"]:
        st.markdown("---")
        st.caption(f"Last refresh: {st.session_state['last_refresh']}")

# ═══════════════════════════════════════════════════════════
#  REFRESH
# ═══════════════════════════════════════════════════════════
def do_refresh():
    errors, status = {}, {}

    try:
        fg_df = scrape_fangraphs()
        status["FanGraphs"] = not fg_df.empty
    except Exception as e:
        fg_df = pd.DataFrame()
        status["FanGraphs"] = False
        errors["FanGraphs"] = str(e)

    if fg_df.empty:
        st.session_state.update({"status": status, "errors": errors})
        return

    try:
        fd_df = scrape_fanduel("nj")
        status["FanDuel"] = not fd_df.empty
    except Exception as e:
        fd_df = pd.DataFrame(columns=["team","market","dec"])
        status["FanDuel"] = False
        errors["FanDuel"] = str(e)

    try:
        dk_df = scrape_draftkings()
        status["DraftKings"] = not dk_df.empty
    except Exception as e:
        dk_df = pd.DataFrame(columns=["team","market","dec","outcome_type"])
        status["DraftKings"] = False
        errors["DraftKings"] = str(e)

    # Store raw dfs — tables are rebuilt live per-market using per-tab margin sliders
    st.session_state.update({
        "raw_fg": fg_df, "raw_fd": fd_df, "raw_dk": dk_df,
        "status": status, "errors": errors,
        "last_refresh": datetime.now().strftime("%Y-%m-%d  %H:%M:%S"),
        "tables": {},  # cleared — rebuilt on render
    })

if refresh_btn:
    with st.spinner("Scraping FanGraphs · FanDuel · DraftKings…"):
        do_refresh()
    st.rerun()

# ═══════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div style="display:flex;align-items:baseline;gap:16px;margin-bottom:2px;">
  <span style="font-family:'Playfair Display',serif;font-size:2.1rem;font-weight:900;
               color:#1a2e1a;text-transform:uppercase;letter-spacing:-0.02em;
               border-bottom:3px solid #1a2e1a;padding-bottom:4px;">
    ⚾ MLB Futures Origination
  </span>
</div>
""", unsafe_allow_html=True)



raw_fg = st.session_state.get("raw_fg")
raw_fd = st.session_state.get("raw_fd")
raw_dk = st.session_state.get("raw_dk")
have_data = raw_fg is not None and not raw_fg.empty

if not have_data:
    st.info("👈  Hit **Refresh All Sources** to scrape live data.")
else:
    TAB_GROUPS = {
        "World Series":    ["World Series"],
        "American League": ["AL Winner","AL East","AL Central","AL West",
                            "Make Playoffs AL","Miss Playoffs AL"],
        "National League": ["NL Winner","NL East","NL Central","NL West",
                            "Make Playoffs NL","Miss Playoffs NL"],
    }

    # Outer group selector — styled radio as horizontal pills
    group_labels = list(TAB_GROUPS.keys())
    selected_group = st.radio(
        "Market group", group_labels, horizontal=True,
        label_visibility="collapsed", key="market_group"
    )
    mkt_list = TAB_GROUPS[selected_group]

    # Inner market tabs
    inner_tabs = st.tabs(mkt_list)
    for itab, mkt_name in zip(inner_tabs, mkt_list):
        with itab:
            if True:  # keep indentation consistent
                    cfg = MARKETS[mkt_name]
                    _is_playoffs_tab = mkt_name in ("Make Playoffs AL","Miss Playoffs AL",
                                                    "Make Playoffs NL","Miss Playoffs NL")

                    # ── Margin from session state ──
                    input_key = f"margin_{mkt_name.replace(' ','_')}"
                    if input_key not in st.session_state:
                        st.session_state[input_key] = MARKET_MARGIN_DEFAULTS[mkt_name]
                    margin_pct = float(st.session_state[input_key])
                    margin_mult = margin_pct / 100.0

                    # ── Build table live using current slider ───────────
                    try:
                        df = build_market(mkt_name, cfg,
                                          raw_fd if raw_fd is not None else pd.DataFrame(columns=["team","market","dec"]),
                                          raw_fg,
                                          raw_dk if raw_dk is not None else pd.DataFrame(columns=["team","market","market_id","dec","outcome_type"]),
                                          margin_mult=margin_mult)
                    except Exception as e:
                        st.error(f"Error building {mkt_name}: {e}")
                        df = None

                    if df is None or df.empty:
                        st.info("No data — hit Refresh All Sources.")
                        continue

                    # ── Build unified HTML panel ─────────────────────────
                    fbg_or = df.attrs.get("fbg_overround", np.nan)
                    fd_or  = df.attrs.get("fd_overround",  np.nan)
                    dk_or  = df.attrs.get("dk_overround",  np.nan)
                    _or_fd_lbl = "FD O/R"
                    _or_dk_lbl = "DK O/R"
                    n_src  = sum([
                        df["FG True Prob"].notna().any() if "FG True Prob" in df.columns else False,
                        df["FD True Prob"].notna().any() if "FD True Prob" in df.columns else False,
                        df["DK True Prob"].notna().any() if "DK True Prob" in df.columns else False,
                    ])

                    def _or_pct(v):
                        try:
                            f = float(v)
                            return f"{f*100:.1f}%" if np.isfinite(f) else "—"
                        except Exception: return "—"

                    def _fmt_am(x):
                        if pd.isna(x) if not isinstance(x, str) else False: return "—"
                        if isinstance(x, str): return x
                        try:
                            v = int(float(x)); return f"+{v}" if v > 0 else str(v)
                        except Exception: return "—"

                    def _fmt_dec(x):
                        try: return f"{float(x):.3f}" if pd.notna(x) else "—"
                        except Exception: return "—"

                    # rows built inline below

                    # Build panel with CSS classes — inline styles get stripped by Streamlit
                    _CSS = """
                    <style>
                    .odds-table{width:100%;border-collapse:collapse;table-layout:fixed;}
                    .odds-table td,.odds-table th{padding:10px 14px;text-align:center;white-space:nowrap;}
                    .col-team{padding:10px 12px!important;text-align:left!important;
                      font-family:'Roboto Condensed',sans-serif;font-size:1rem;font-weight:700;
                      color:#1a2e1a;border-right:3px solid #1a2e1a;background:#fff8ee;
                      width:120px;min-width:80px;max-width:140px;
                      white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
                    .col-b-am{font-family:"Source Code Pro",monospace;font-size:1rem;font-weight:700;
                      color:#1a3a1a;background:#dff0df;}
                    .col-b-dec{font-family:"Source Code Pro",monospace;font-size:0.9rem;
                      color:#2a5a2a;background:#dff0df;border-right:3px solid #c8b898;}
                    .col-fd-am{font-family:"Source Code Pro",monospace;font-size:1rem;font-weight:700;
                      color:#0a2a50;background:#daeaf8;}
                    .col-fd-dec{font-family:"Source Code Pro",monospace;font-size:0.9rem;
                      color:#1a4a70;background:#daeaf8;border-right:3px solid #c8b898;}
                    .col-dk-am{font-family:"Source Code Pro",monospace;font-size:1rem;font-weight:700;
                      color:#5a0a0a;background:#f5dada;}
                    .col-dk-dec{font-family:"Source Code Pro",monospace;font-size:0.9rem;
                      color:#7a2a2a;background:#f5dada;}
                    .odds-table tr:nth-child(odd) .col-b-am,.odds-table tr:nth-child(odd) .col-b-dec{background:#cee8ce;}
                    .odds-table tr:nth-child(odd) .col-fd-am,.odds-table tr:nth-child(odd) .col-fd-dec{background:#c8dff5;}
                    .odds-table tr:nth-child(odd) .col-dk-am,.odds-table tr:nth-child(odd) .col-dk-dec{background:#eecece;}
                    .odds-table tr:nth-child(odd) .col-team{background:#f5f0e8;}
                    .th-team{padding:8px 16px!important;text-align:left!important;
                      font-family:'Source Code Pro',monospace;font-size:0.68rem;
                      text-transform:uppercase;letter-spacing:0.09em;font-weight:600;
                      background:#e8dfc8;color:#3a5a3a;border-right:3px solid #1a2e1a;}
                    .th-blend{font-family:"Source Code Pro",monospace;font-size:0.68rem;
                      text-transform:uppercase;letter-spacing:0.09em;font-weight:600;
                      background:#1a2e1a;color:#c8a84b;}
                    .th-blend-dec{background:#1a2e1a;color:#a8c8a8;border-right:3px solid #c8b898;}
                    .th-fd{background:#1e3a5f;color:#90c8f0;
                      font-family:'Source Code Pro',monospace;font-size:0.68rem;
                      text-transform:uppercase;letter-spacing:0.09em;font-weight:600;}
                    .th-fd-dec{background:#1e3a5f;color:#7aaad0;border-right:3px solid #c8b898;}
                    .th-dk{background:#5f1e1e;color:#f0a0a0;
                      font-family:'Source Code Pro',monospace;font-size:0.68rem;
                      text-transform:uppercase;letter-spacing:0.09em;font-weight:600;}
                    .th-dk-dec{background:#5f1e1e;color:#d07a7a;}
                    .or-team{padding:10px 16px!important;background:#fff8ee;
                      border-right:3px solid #1a2e1a;vertical-align:middle;
                      font-family:'Source Code Pro',monospace;}
                    .or-blend{padding:10px 16px!important;background:#1a2e1a;text-align:center!important;
                      border-right:3px solid #c8b898;font-family:'Source Code Pro',monospace;}
                    .or-fd{padding:10px 16px!important;background:#1e3a5f;text-align:center!important;
                      border-right:3px solid #c8b898;font-family:'Source Code Pro',monospace;}
                    .or-dk{padding:10px 16px!important;background:#5f1e1e;text-align:center!important;
                      font-family:'Source Code Pro',monospace;}
                    /* Margin control cell */
                    .ctrl-cell{background:#fff8ee;border-right:3px solid #1a2e1a;
                      padding:8px 12px;vertical-align:middle;white-space:nowrap;}
                    .ctrl-label{font-family:"Source Code Pro",monospace;font-size:0.58rem;
                      color:#5a7a5a;text-transform:uppercase;letter-spacing:0.1em;
                      display:block;margin-bottom:5px;}
                    .ctrl-row{display:flex;align-items:center;gap:4px;}
                    .ctrl-input{display:none;}
                    .ctrl-val{font-family:"Source Code Pro",monospace;font-weight:700;
                      font-size:1rem;color:#1a2e1a;min-width:52px;text-align:center;
                      padding:2px 4px;}
                    .ctrl-btn{font-family:"Source Code Pro",monospace;font-weight:700;
                      font-size:0.9rem;color:#1a2e1a;background:#e8dfc8;
                      border:1.5px solid #1a2e1a;border-radius:3px;
                      width:24px;height:24px;cursor:pointer;padding:0;
                      display:flex;align-items:center;justify-content:center;}
                    .ctrl-btn:hover{background:#1a2e1a;color:#c8a84b;}
                    </style>"""

                    # ── Render panel via component — margin controls inside or-team cell ──
                    # Replace the static or-team cell with the placeholder for the component
                    or_team_cell = (
                        '<td class="or-team-placeholder"></td>'
                    )

                    parts = [
                        _CSS,
                        '<div style="border:2px solid #1a2e1a;border-radius:6px;'
                        'overflow:hidden;box-shadow:4px 4px 0 #1a2e1a;margin-bottom:20px;">',
                        '<table class="odds-table">',
                        '<thead>',
                        '<tr>',
                        or_team_cell,
                        ('<td class="or-blend" colspan="2">'
                         '<span style="display:block;font-size:0.72rem;color:#7a9a7a;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:3px;">Blended O/R</span>'
                         '<span style="display:block;font-size:1.3rem;font-weight:700;color:#c8a84b;">'
                         + _or_pct(fbg_or) + '</span></td>'),
                        ('<td class="or-fd" colspan="2">'
                         '<span style="display:block;font-size:0.72rem;color:#7aaad0;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:3px;">FD O/R</span>'
                         '<span style="display:block;font-size:1.3rem;font-weight:700;color:#d0e8ff;">'
                         + _or_pct(fd_or) + '</span></td>'),
                        ('<td class="or-dk" colspan="2">'
                         '<span style="display:block;font-size:0.72rem;color:#d07a7a;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:3px;">DK O/R</span>'
                         '<span style="display:block;font-size:1.3rem;font-weight:700;color:#ffd0d0;">'
                         + _or_pct(dk_or) + '</span></td>'),
                        '</tr>',
                        '<tr>',
                        '<th class="th-team">Team</th>',
                        '<th class="th-blend">Am</th>',
                        '<th class="th-blend th-blend-dec">Dec</th>',
                        '<th class="th-fd">FD Am</th>',
                        '<th class="th-fd th-fd-dec">FD Dec</th>',
                        '<th class="th-dk">DK Am</th>',
                        '<th class="th-dk th-dk-dec">DK Dec</th>',
                        '</tr>',
                        '</thead><tbody>',
                    ]

                    DISPLAY_COLS2 = ["team","Blended Am","Blended Dec","FD Am Odds","FD Dec","DK Am Odds","DK Dec"]
                    for _, row in df[[c for c in DISPLAY_COLS2 if c in df.columns]].iterrows():
                        parts += [
                            '<tr>',
                            '<td class="col-team">'  + TEAM_NICKNAMES.get(str(row.get("team","")), str(row.get("team",""))) + '</td>',
                            '<td class="col-b-am">'  + _fmt_am(row.get("Blended Am","—"))         + '</td>',
                            '<td class="col-b-dec">' + _fmt_dec(row.get("Blended Dec","—"))       + '</td>',
                            '<td class="col-fd-am">' + _fmt_am(row.get("FD Am Odds","—"))         + '</td>',
                            '<td class="col-fd-dec">'+ _fmt_dec(row.get("FD Dec","—"))            + '</td>',
                            '<td class="col-dk-am">' + _fmt_am(row.get("DK Am Odds","—"))         + '</td>',
                            '<td class="col-dk-dec">'+ _fmt_dec(row.get("DK Dec","—"))            + '</td>',
                            '</tr>',
                        ]

                    parts.append(
                        '<tr>'
                        '<td style="padding:6px 16px;font-family:\'Source Code Pro\',monospace;'
                        'font-size:0.7rem;color:#5a7a5a;text-transform:uppercase;'
                        'letter-spacing:0.1em;background:#f0e8d8;border-top:1px solid #c8b898;'
                        'border-right:3px solid #1a2e1a;">'
                        + str(len(df)) + ' teams</td>'
                        '<td colspan="6" style="background:#f0e8d8;border-top:1px solid #c8b898;"></td>'
                        '</tr>'
                    )
                    parts += ['</tbody>', '</table>', '</div>']

                    _panel_html = "".join(parts)
                    _new_margin = _margin_component(_panel_html, margin_pct, input_key, len(df))
                    if _new_margin is not None and abs(_new_margin - margin_pct) > 0.001:
                        st.session_state[input_key] = round(_new_margin, 1)
                        st.rerun()

                    # ── Raw data expander ──────────────────────────────────────────
                    with st.expander("📊 Raw true prices", expanded=False):
                        _raw_cols = [
                            ("Team",         "team"),
                            ("Blend True%",  "True Price"),
                            ("Blend Margin%","FBG Margin"),
                            ("FG True%",     "FG True Prob"),
                            ("FD True%",     "FD True Prob"),
                            ("FD Margin%",   "FD Margin"),
                            ("DK True%",     "DK True Prob"),
                            ("DK Margin%",   "DK Margin"),
                        ]
                        _disp_cols = {label: col for label, col in _raw_cols if col in df.columns}
                        _raw_df = df[[col for col in _disp_cols.values()]].copy()
                        _raw_df.columns = list(_disp_cols.keys())
                        if "Team" in _raw_df.columns:
                            _raw_df["Team"] = _raw_df["Team"].apply(
                                lambda t: TEAM_NICKNAMES.get(str(t), str(t)))
                        for _pc in ["Blend True%","Blend Margin%","FG True%","FD True%","FD Margin%","DK True%","DK Margin%"]:
                            if _pc in _raw_df.columns:
                                _raw_df[_pc] = _raw_df[_pc].apply(
                                    lambda v: f"{float(v)*100:.2f}%" if pd.notna(v) and v != "—" else "—")
                        st.dataframe(
                            _raw_df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Team":          st.column_config.TextColumn("Team",         width="small"),
                                "Blend True%":   st.column_config.TextColumn("Blend True%",  width="small"),
                                "Blend Margin%": st.column_config.TextColumn("Blend Margin%",width="small"),
                                "FG True%":      st.column_config.TextColumn("FG True%",     width="small"),
                                "FD True%":      st.column_config.TextColumn("FD True%",     width="small"),
                                "FD Margin%":    st.column_config.TextColumn("FD Margin%",   width="small"),
                                "DK True%":      st.column_config.TextColumn("DK True%",     width="small"),
                                "DK Margin%":    st.column_config.TextColumn("DK Margin%",   width="small"),
                            }
                        )
