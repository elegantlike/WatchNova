import streamlit as st
import requests
import streamlit.components.v1 as components

# ---------------------------------------------------
# CONFIG (SECURE VIA SECRETS)
# ---------------------------------------------------

st.set_page_config(page_title="WatchNova", layout="wide")

API_KEY = st.secrets["TMDB_API_KEY"]
BASE_URL = st.secrets["TMDB_BASE_URL"]
IMG = st.secrets["TMDB_IMG_BASE"]
PLAYER = st.secrets["MOVIE_PLAYER"]

# ---------------------------------------------------
# GLOBAL ADS (POPUNDER)
# ---------------------------------------------------

st.markdown("""
<script src="https://pl28911001.effectivegatecpm.com/3a/71/db/3a71db8145b2db0756eb64092929f733.js"></script>
<script src="https://pl28911102.effectivegatecpm.com/5b/79/7b/5b797b21587feb30c918fe8ed648990a.js"></script>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# STYLE
# ---------------------------------------------------

st.markdown("""
<style>

.stApp{
background:#071426;
}

.poster-box{
width:100%;
aspect-ratio:2/3;
overflow:hidden;
border-radius:12px;
}

.poster-img{
width:100%;
height:100%;
object-fit:cover;
border-radius:12px;
transition:0.25s;
}

.poster-img:hover{
transform:scale(1.05);
}

.title{
color:white;
text-align:center;
font-size:14px;
margin-top:6px;
min-height:40px;
}

.section{
color:white;
font-size:26px;
margin-top:30px;
margin-bottom:15px;
}

.hero{
background:linear-gradient(to right,#000,#0b1a32);
padding:40px;
border-radius:14px;
margin-bottom:30px;
}

.player-box{
background:#0b1a32;
padding:30px;
border-radius:16px;
margin-bottom:40px;
}

.play-btn button{
width:100%;
background:#e50914;
color:white;
border-radius:8px;
border:none;
}

@media (max-width:900px){
.stColumn{
min-width:150px !important;
}
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# ADS (NATIVE BANNER)
# ---------------------------------------------------

def native_banner():
    components.html("""
<script async="async" data-cfasync="false"
src="//pl28911019.effectivegatecpm.com/623f51e846d84c614f530915212dd6e4/invoke.js"></script>
<div id="container-623f51e846d84c614f530915212dd6e4"></div>
""", height=120)

# ---------------------------------------------------
# API FUNCTIONS
# ---------------------------------------------------

def safe_get(url, params):
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except:
        return {}

def trending():
    data = safe_get(f"{BASE_URL}/trending/movie/week", {"api_key": API_KEY})
    return data.get("results", [])

def search_movies(q):
    data = safe_get(f"{BASE_URL}/search/multi", {"api_key": API_KEY, "query": q})
    return [x for x in data.get("results", []) if x.get("media_type") in ["movie","tv"]]

# ---------------------------------------------------
# MOVIE GRID
# ---------------------------------------------------

def movie_grid(data):

    cols = st.columns(6)

    for i,m in enumerate(data[:18]):

        with cols[i % 6]:

            if m.get("poster_path"):

                poster = IMG + m["poster_path"]
                title = m.get("title") or m.get("name")

                st.markdown(
                    f"""
<div class="poster-box">
<img class="poster-img" src="{poster}">
</div>
""",
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="title">{title}</div>',
                    unsafe_allow_html=True
                )

                if st.button("▶ Play", key=f"play_{m['id']}"):

                    st.session_state["movie"] = m
                    st.session_state["scroll"] = True
                    st.rerun()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.image(
"https://cdn-icons-png.flaticon.com/512/1179/1179120.png",
width=100
)

st.sidebar.title("WatchNova")

page = st.sidebar.radio(
"Explore",
["Home","Trending","Search"]
)

# ---------------------------------------------------
# PLAYER SECTION
# ---------------------------------------------------

if "movie" in st.session_state:

    m = st.session_state["movie"]

    title = m.get("title") or m.get("name")
    overview = m.get("overview","")

    if m["media_type"] == "movie":
        url = f"{PLAYER}/movie/{m['id']}"
    else:
        season = st.number_input("Season",1,20,1)
        episode = st.number_input("Episode",1,20,1)
        url = f"{PLAYER}/tv/{m['id']}/{season}/{episode}"

    st.markdown(f"""
<div class="player-box">
<h2 style="color:white;">{title}</h2>
<p style="color:#bbb;">{overview}</p>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<iframe
src="{url}"
width="100%"
height="520"
frameborder="0"
allowfullscreen>
</iframe>
""", unsafe_allow_html=True)

    native_banner()

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

if page == "Home":

    st.markdown("""
<div class="hero">
<h1 style="color:white;">WatchNova</h1>
<p style="color:white;">Discover trending movies and TV shows instantly.</p>
</div>
""", unsafe_allow_html=True)

    native_banner()

    st.markdown('<div class="section">Trending Now</div>', unsafe_allow_html=True)

    movie_grid(trending())

    native_banner()

# ---------------------------------------------------
# TRENDING
# ---------------------------------------------------

elif page == "Trending":

    st.markdown('<div class="section">Trending Movies</div>', unsafe_allow_html=True)

    native_banner()

    movie_grid(trending())

    native_banner()

# ---------------------------------------------------
# SEARCH
# ---------------------------------------------------

elif page == "Search":

    q = st.text_input("Search movies or series")

    if q:
        native_banner()
        movie_grid(search_movies(q))
        native_banner()

# ---------------------------------------------------
# AUTO SCROLL
# ---------------------------------------------------

if st.session_state.get("scroll"):

    st.markdown("""
<script>
window.scrollTo({top:0, behavior:'smooth'});
</script>
""", unsafe_allow_html=True)

    st.session_state["scroll"] = False