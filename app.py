import pickle
import streamlit as st
import requests

st.set_page_config(
    page_title="CINMATCH — Film Intelligence",
    page_icon="🎞",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&family=DM+Serif+Display:ital@1&display=swap');

/* ══════ VARIABLES ══════ */
:root {
    --bg:       #07070f;
    --surface:  #0e0e1a;
    --card:     #11111d;
    --border:   rgba(255,255,255,0.07);
    --red:      #e8412a;
    --red2:     #ff6650;
    --text:     #edeae4;
    --muted:    rgba(237,234,228,0.4);
    --W:        1280px;
}

/* ══════ KILL ALL STREAMLIT DEFAULT SPACING ══════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body { background: var(--bg) !important; }

[data-testid="stApp"],
[data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    padding-top: 0 !important;
    margin-top: 0 !important;
}

[data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
section[data-testid="stSidebar"] { margin-top: 0 !important; }

.main > div:first-child { padding-top: 0 !important; }

.main .block-container {
    padding: 0 !important;
    margin: 0 auto !important;
    max-width: 100% !important;
    min-height: 0 !important;
}

[data-testid="stVerticalBlock"] > div { gap: 0 !important; }

/* ══════ HIDE CHROME ══════ */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stAppViewContainer"] > section:first-child { display: none !important; }

/* Ambient glow */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 50vh;
    background: radial-gradient(ellipse 80% 60% at 50% -10%, rgba(232,65,42,0.10) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ══════ PAGE WRAPPER ══════ */
.page {
    max-width: var(--W);
    margin: 0 auto;
    padding: 0 3rem;
    position: relative;
    z-index: 1;
}

/* ══════ NAVBAR ══════ */
.nb {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.2rem 3rem;
    margin: 0 -3rem;
    border-bottom: 1px solid var(--border);
    background: rgba(7,7,15,0.85);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    position: sticky;
    top: 0;
    z-index: 500;
}

.nb-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.55rem;
    letter-spacing: 0.1em;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.nb-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--red);
    flex-shrink: 0;
    animation: throb 2s ease-in-out infinite;
}

@keyframes throb {
    0%,100% { box-shadow: 0 0 0 0 rgba(232,65,42,0.7); }
    50%      { box-shadow: 0 0 0 7px rgba(232,65,42,0); }
}

.nb-pill {
    font-size: 0.57rem;
    font-weight: 500;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: var(--muted);
    border: 1px solid var(--border);
    padding: 0.28rem 0.85rem;
    border-radius: 30px;
}

/* ══════ HERO ══════ */
.hero {
    display: grid;
    grid-template-columns: 1fr 280px;
    align-items: center;
    gap: 2rem;
    padding: 3.5rem 0 2.8rem;
    border-bottom: 1px solid var(--border);
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.56rem;
    font-weight: 500;
    letter-spacing: 0.38em;
    text-transform: uppercase;
    color: var(--red2);
    margin-bottom: 1rem;
}
.hero-eyebrow::before {
    content: '';
    display: block;
    width: 20px; height: 1px;
    background: var(--red);
    flex-shrink: 0;
}

.hero-h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.2rem, 6vw, 5.8rem);
    line-height: 0.9;
    letter-spacing: 0.02em;
    color: var(--text);
    margin-bottom: 1.2rem;
}
.hero-h1 .red { color: var(--red); display: block; }

.hero-body {
    font-family: 'DM Serif Display', serif;
    font-style: italic;
    font-size: 0.98rem;
    line-height: 1.75;
    color: var(--muted);
    max-width: 420px;
    margin-bottom: 1.8rem;
}

.hero-stats {
    display: flex;
    align-items: center;
    gap: 0;
}

.hs-item { padding-right: 1.8rem; }
.hs-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.04em;
    color: var(--text);
    line-height: 1;
}
.hs-lbl {
    font-size: 0.54rem;
    font-weight: 400;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 0.18rem;
}
.hs-sep {
    width: 1px;
    height: 32px;
    background: var(--border);
    margin-right: 1.8rem;
    flex-shrink: 0;
}

/* Film strip */
.film-strip {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.65rem;
    height: 100%;
}

.fs-frame {
    border-radius: 8px;
    background: var(--surface);
    border: 1px solid rgba(255,255,255,0.07);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    color: rgba(255,255,255,0.06);
    flex-shrink: 0;
    position: relative;
    overflow: hidden;
}
.fs-frame::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(232,65,42,0.07), transparent 60%);
}
.fs-frame:nth-child(1) { width: 76px;  height: 112px; transform: translateY(6px); }
.fs-frame:nth-child(2) { width: 86px;  height: 130px; border-color: rgba(232,65,42,0.2); }
.fs-frame:nth-child(3) { width: 72px;  height: 106px; transform: translateY(8px); }

/* ══════ SEARCH SECTION ══════ */
.search-hd {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2rem 0 0.7rem;
}

.search-hd-left {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
    letter-spacing: 0.1em;
    color: var(--text);
}
.search-hd-left::before {
    content: '';
    display: block;
    width: 3px; height: 17px;
    background: var(--red);
    border-radius: 2px;
}

.search-hd-right {
    font-size: 0.68rem;
    font-weight: 300;
    color: var(--muted);
}

/* ══════ STREAMLIT COLUMN WRAPPER FIX ══════ */
[data-testid="stHorizontalBlock"] {
    align-items: stretch !important;
    gap: 0 !important;
    width: 100% !important;
}

[data-testid="column"] { padding: 0 !important; }
[data-testid="column"]:first-child { padding-right: 0.6rem !important; }

/* ══════ SELECTBOX ══════ */
[data-testid="stSelectbox"] { width: 100% !important; }
[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] > label { display: none !important; }
[data-testid="stSelectbox"] > div { background: transparent !important; }

[data-testid="stSelectbox"] > div > div,
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: var(--surface) !important;
    border: 1.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    min-height: 52px !important;
    transition: border-color 0.2s, box-shadow 0.2s, background 0.2s !important;
    padding-left: 0.9rem !important;
}
[data-testid="stSelectbox"] > div > div:hover,
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--red) !important;
    background: rgba(232,65,42,0.05) !important;
    box-shadow: 0 0 0 3px rgba(232,65,42,0.12), 0 4px 20px rgba(0,0,0,0.35) !important;
}

[data-testid="stSelectbox"] *:not(svg):not(path) { color: var(--text) !important; }
[data-testid="stSelectbox"] input,
[data-testid="stSelectbox"] input:focus {
    color: var(--text) !important;
    background: transparent !important;
    caret-color: var(--red) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 400 !important;
}
[data-testid="stSelectbox"] [class*="placeholder"] {
    color: rgba(237,234,228,0.28) !important;
    font-size: 0.92rem !important;
    font-style: italic !important;
}
[data-testid="stSelectbox"] [class*="singleValue"],
[data-testid="stSelectbox"] [class*="Input"] {
    color: var(--text) !important;
    font-size: 0.92rem !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSelectbox"] [class*="indicatorSeparator"] { display: none !important; }
[data-testid="stSelectbox"] [class*="indicatorContainer"] svg { fill: rgba(237,234,228,0.3) !important; }

[data-testid="stSelectbox"] [class*="menu"],
[data-testid="stSelectbox"] [class*="MenuList"],
[data-testid="stSelectbox"] ul {
    background: #191926 !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 10px !important;
    box-shadow: 0 20px 60px rgba(0,0,0,0.65) !important;
}
[data-testid="stSelectbox"] [class*="option"],
[data-testid="stSelectbox"] li {
    color: rgba(237,234,228,0.68) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.87rem !important;
    padding: 0.65rem 1rem !important;
    background: transparent !important;
}
[data-testid="stSelectbox"] [class*="option"]:hover,
[data-testid="stSelectbox"] [class*="option--is-focused"] {
    background: rgba(232,65,42,0.13) !important;
    color: var(--text) !important;
}
[data-testid="stSelectbox"] [class*="option--is-selected"] {
    background: rgba(232,65,42,0.22) !important;
    color: var(--red2) !important;
}

/* ══════ BUTTON ══════ */
[data-testid="stButton"] { width: 100% !important; }
[data-testid="stButton"] > button {
    width: 100% !important;
    height: 52px !important;
    background: linear-gradient(145deg, var(--red), #bf3420) !important;
    border: none !important;
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 6px 22px rgba(232,65,42,0.4) !important;
    white-space: nowrap !important;
    padding: 0 !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px rgba(232,65,42,0.55) !important;
    filter: brightness(1.1) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
    filter: brightness(0.95) !important;
}

/* ══════ DIVIDER ══════ */
.div-line {
    width: 100%; height: 1px;
    background: var(--border);
    margin: 1.5rem 0 0;
}

/* ══════ RESULTS HEADER ══════ */
.res-hd {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2.5rem 0 1.5rem;
}

.res-hd-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 0.06em;
    color: var(--text);
}
.res-hd-title span { color: var(--red); }

.res-hd-badge {
    font-size: 0.6rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--muted);
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    padding: 0.35rem 0.85rem;
    border-radius: 30px;
}

/* ══════ POSTER CARDS ══════ */
[data-testid="column"]:not(:first-child) { padding-left: 0.55rem !important; }
[data-testid="column"]:not(:last-child)  { padding-right: 0.55rem !important; }

.pc {
    border-radius: 10px;
    overflow: hidden;
    background: var(--card);
    border: 1px solid var(--border);
    transition: transform 0.3s cubic-bezier(0.34,1.15,0.64,1),
                border-color 0.25s, box-shadow 0.3s;
    animation: rise 0.45s cubic-bezier(0.34,1.15,0.64,1) both;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    height: 100%;
}

.pc:nth-child(1){animation-delay:0.04s}
.pc:nth-child(2){animation-delay:0.09s}
.pc:nth-child(3){animation-delay:0.14s}
.pc:nth-child(4){animation-delay:0.19s}
.pc:nth-child(5){animation-delay:0.24s}

@keyframes rise {
    from { opacity:0; transform:translateY(30px) scale(0.97); }
    to   { opacity:1; transform:translateY(0)     scale(1); }
}

.pc:hover {
    transform: translateY(-8px) scale(1.02) !important;
    border-color: rgba(232,65,42,0.45) !important;
    box-shadow: 0 24px 56px rgba(0,0,0,0.65),
                0 0 0 1px rgba(232,65,42,0.15),
                0 0 40px rgba(232,65,42,0.08) !important;
}

.pc-img {
    position: relative;
    width: 100%;
    aspect-ratio: 2/3;
    overflow: hidden;
    flex-shrink: 0;
}
.pc-img img {
    width:100%; height:100%;
    object-fit:cover; display:block;
    transition: transform 0.5s ease;
}
.pc:hover .pc-img img { transform: scale(1.05); }

.pc-rank {
    position:absolute; top:8px; left:8px;
    width:26px; height:26px;
    background:var(--red);
    border-radius:6px;
    display:flex; align-items:center; justify-content:center;
    font-family:'Bebas Neue',sans-serif;
    font-size:0.9rem; color:#fff;
    box-shadow:0 3px 10px rgba(232,65,42,0.6);
    z-index:2;
}

.pc-chip {
    position:absolute; top:8px; right:8px;
    background:rgba(7,7,15,0.85);
    backdrop-filter:blur(6px);
    border:1px solid rgba(255,255,255,0.1);
    border-radius:5px;
    padding:0.18rem 0.4rem;
    display:flex; align-items:center; gap:4px;
    font-size:0.55rem; font-weight:500;
    color:var(--text); z-index:2;
}
.pc-chip-dot { width:5px;height:5px;border-radius:50%;background:#22c55e;flex-shrink:0; }

.pc-overlay {
    position:absolute; inset:0;
    background:linear-gradient(to top,
        rgba(7,7,15,0.97) 0%,
        rgba(7,7,15,0.5) 38%,
        transparent 68%);
    padding:0.9rem;
    display:flex; flex-direction:column; justify-content:flex-end;
    opacity:0; transition:opacity 0.28s ease; z-index:1;
}
.pc:hover .pc-overlay { opacity:1; }

.pc-ov-tag {
    font-size:0.48rem; font-weight:600;
    letter-spacing:0.3em; text-transform:uppercase;
    color:var(--red2); margin-bottom:0.22rem;
}
.pc-ov-title {
    font-family:'Bebas Neue',sans-serif;
    font-size:1rem; letter-spacing:0.04em;
    color:var(--text); line-height:1.1;
}
.pc-ov-cta {
    font-size:0.6rem; font-weight:500;
    color:var(--red2); margin-top:0.38rem;
}

.pc-foot {
    padding:0.75rem 0.85rem 0.8rem;
    background:var(--card);
    border-top:1px solid var(--border);
    flex:1;
}
.pc-foot-title {
    font-size:0.77rem; font-weight:500;
    color:var(--text);
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
    line-height:1.3;
}
.pc-foot-sub {
    font-size:0.6rem; font-weight:300;
    color:var(--muted); margin-top:0.15rem;
}

/* ══════ FOOTER ══════ */
.site-foot {
    margin-top: 4rem;
    position: relative;
}

/* glowing top border */
.site-foot::before {
    content: '';
    display: block;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(232,65,42,0.5) 30%,
        rgba(232,65,42,0.5) 70%,
        transparent 100%);
}

.foot-inner {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 2rem;
    padding: 2.2rem 0 2.8rem;
}

/* — LEFT: brand — */
.foot-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.12em;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-bottom: 0.35rem;
}
.foot-logo-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--red);
    flex-shrink: 0;
    box-shadow: 0 0 8px rgba(232,65,42,0.8);
}
.foot-tagline {
    font-size: 0.65rem;
    font-weight: 400;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(237,234,228,0.5); /* BRIGHTENED */
}
.foot-stack {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}
.foot-stack-chip {
    font-size: 0.55rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(237,234,228,0.75); /* BRIGHTENED */
    background: rgba(255,255,255,0.03); /* ADDED BG */
    border: 1px solid rgba(255,255,255,0.15); /* STRONGER BORDER */
    border-radius: 6px;
    padding: 0.3rem 0.6rem;
}

/* — CENTER: credit — */
.foot-credit {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.8rem;
}

.foot-credit-eyebrow {
    font-size: 0.55rem;
    font-weight: 500;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: rgba(237,234,228,0.45); /* BRIGHTENED */
}

.foot-author-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.foot-avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--red) 0%, #7a1508 100%);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
    color: #fff;
    flex-shrink: 0;
    box-shadow: 0 0 0 2px rgba(232,65,42,0.3), 0 4px 14px rgba(232,65,42,0.35);
}
.foot-author-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.25rem;
    letter-spacing: 0.12em;
    color: var(--text);
    line-height: 1;
}

.foot-gh-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    text-decoration: none !important; /* REMOVED UNDERLINE */
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.15); /* STRONGER BORDER */
    border-radius: 9px;
    padding: 0.6rem 1.2rem 0.6rem 0.9rem;
    transition: all 0.28s cubic-bezier(0.34,1.15,0.64,1);
}
.foot-gh-btn:hover {
    background: rgba(232,65,42,0.09);
    border-color: rgba(232,65,42,0.38);
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(232,65,42,0.18);
}
.foot-gh-icon {
    color: rgba(237,234,228,0.7); /* BRIGHTENED */
    flex-shrink: 0;
    transition: color 0.25s;
}
.foot-gh-btn:hover .foot-gh-icon { color: var(--red2); }
.foot-gh-label {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}
.foot-gh-repo {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: rgba(237,234,228,0.9); /* BRIGHTENED */
    line-height: 1;
    text-decoration: none !important; /* REMOVED UNDERLINE */
}
.foot-gh-sub {
    font-size: 0.55rem;
    font-weight: 400;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(237,234,228,0.5); /* BRIGHTENED */
    line-height: 1;
    text-decoration: none !important; /* REMOVED UNDERLINE */
}

/* — RIGHT: meta — */
.foot-meta {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.5rem;
}
.foot-powered {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.6rem;
    font-weight: 400;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: rgba(237,234,228,0.5); /* BRIGHTENED */
}
.foot-sep {
    width: 3px; height: 3px;
    border-radius: 50%;
    background: rgba(237,234,228,0.3); /* BRIGHTENED */
    flex-shrink: 0;
}
.foot-copy {
    font-size: 0.55rem;
    font-weight: 400;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(237,234,228,0.3); /* BRIGHTENED */
}

/* ══════ MISC ══════ */
::-webkit-scrollbar { width:3px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:rgba(232,65,42,0.35); border-radius:2px; }

[data-testid="stSpinner"]>div { border-top-color:var(--red)!important; }

div[data-testid="stVerticalBlock"] > div[style] { min-height: 0 !important; }
.element-container { margin: 0 !important; padding: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ─── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    with open('movies.pkl', 'rb') as f:
        movies = pickle.load(f)
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
    return movies, similarity

movies, similarity = load_data()

def fetch_poster(movie_id):
    try:
        url  = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url, timeout=6).json()
        path = data.get('poster_path', '')
        if path: return "https://image.tmdb.org/t/p/w500" + path
    except: pass
    return "https://placehold.co/500x750/11111d/e8412a?text=NO+POSTER"

def recommend(movie):
    idx       = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[idx]), reverse=True, key=lambda x: x[1])
    names, posters = [], []
    for i in distances[1:6]:
        mid = movies.iloc[i[0]].movie_id
        posters.append(fetch_poster(mid))
        names.append(movies.iloc[i[0]].title)
    return names, posters


# ══════════════════════════════════════════════════════════════
#  PAGE STARTS HERE
# ══════════════════════════════════════════════════════════════

# ── NAVBAR ─────────────────────────────────────────────────
st.markdown("""
<div class="page">
<nav class="nb">
<div class="nb-logo">CINMATCH <span class="nb-dot"></span></div>
<span class="nb-pill">Film Intelligence Engine</span>
</nav>
""", unsafe_allow_html=True)

# ── HERO ───────────────────────────────────────────────────
st.markdown("""
<div class="hero">
<div>
<div class="hero-eyebrow">AI-Powered Movie Discovery</div>
<h1 class="hero-h1">Find Your<span class="red">Next Film.</span></h1>
<p class="hero-body">Tell us one movie you love — our intelligence engine maps the entire cinematic universe around it.</p>
<div class="hero-stats">
<div class="hs-item"><div class="hs-num">5K+</div><div class="hs-lbl">Films Indexed</div></div>
<div class="hs-sep"></div>
<div class="hs-item"><div class="hs-num">AI</div><div class="hs-lbl">Similarity Engine</div></div>
<div class="hs-sep"></div>
<div class="hs-item"><div class="hs-num">∞</div><div class="hs-lbl">Discoveries</div></div>
</div>
</div>
<div class="film-strip">
<div class="fs-frame">🎬</div>
<div class="fs-frame">🎞</div>
<div class="fs-frame">🍿</div>
</div>
</div>
""", unsafe_allow_html=True)

# ── SEARCH HEADER ──────────────────────────────────────────
st.markdown("""
<div class="search-hd">
<span class="search-hd-left">Pick a Film</span>
<span class="search-hd-right">Type to search from 5,000+ titles</span>
</div>
""", unsafe_allow_html=True)

# ── SEARCH ROW ─────────────────────────────────────────────
col_sel, col_btn = st.columns([5, 1])
with col_sel:
    selected_movie = st.selectbox(
        label="Movie",
        options=movies['title'].values,
        index=None,
        label_visibility="collapsed",
        placeholder="e.g.  Inception, The Dark Knight, Parasite…"
    )
with col_btn:
    discover = st.button("⚡  Find Similar")

st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)

# ── RESULTS ────────────────────────────────────────────────
if discover:
    if selected_movie:
        with st.spinner("Mapping the cinematic universe…"):
            names, posters = recommend(selected_movie)

        short = selected_movie[:28] + ("…" if len(selected_movie) > 28 else "")
        st.markdown(f"""
<div class="res-hd">
<div class="res-hd-title">Because you liked &nbsp;<span>"{short}"</span></div>
<span class="res-hd-badge">5 Recommendations</span>
</div>
        """, unsafe_allow_html=True)

        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"""
<div class="pc">
<div class="pc-img">
<img src="{posters[i]}" alt="{names[i]}" loading="lazy"/>
<div class="pc-rank">{i+1}</div>
<div class="pc-chip"><span class="pc-chip-dot"></span> Match</div>
<div class="pc-overlay">
<div class="pc-ov-tag">AI Recommended</div>
<div class="pc-ov-title">{names[i]}</div>
<div class="pc-ov-cta">▶ View Details →</div>
</div>
</div>
<div class="pc-foot">
<div class="pc-foot-title">{names[i]}</div>
<div class="pc-foot-sub">AI matched · Similar to your pick</div>
</div>
</div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Please select a movie from the list before searching.", icon="⚠️")

# ── FOOTER ─────────────────────────────────────────────────
st.markdown("""
<div class="site-foot">
<div class="foot-inner">

<div>
<div class="foot-logo">CINMATCH <span class="foot-logo-dot"></span></div>
<div class="foot-tagline">Film Intelligence Engine</div>
<div class="foot-stack">
<span class="foot-stack-chip">Python</span>
<span class="foot-stack-chip">scikit-learn</span>
<span class="foot-stack-chip">TF-IDF</span>
<span class="foot-stack-chip">Streamlit</span>
<span class="foot-stack-chip">TMDB API</span>
</div>
</div>

<div class="foot-credit">
<span class="foot-credit-eyebrow">Crafted with ❤ by</span>
<div class="foot-author-row">
<div class="foot-avatar">A</div>
<div class="foot-author-name">ANISH</div>
</div>
<a class="foot-gh-btn" href="https://github.com/anish-devgit/content-recommender-ml" target="_blank" rel="noopener noreferrer">
<svg class="foot-gh-icon" width="17" height="17" viewBox="0 0 24 24" fill="currentColor">
<path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405 c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
</svg>
<div class="foot-gh-label">
<span class="foot-gh-repo">content-recommender-ml</span>
<span class="foot-gh-sub">Open source · Contribute on GitHub</span>
</div>
</a>
</div>

<div class="foot-meta">
<div class="foot-powered">
Powered by TMDB
<span class="foot-sep"></span>
AI Engine
<span class="foot-sep"></span>
Cosine Similarity
</div>
<div class="foot-copy">© 2025 CINMATCH — All rights reserved</div>
</div>

</div>
</div>
</div>""", unsafe_allow_html=True)