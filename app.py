import streamlit as st
import requests

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

st.set_page_config(page_title="WatchNova", layout="wide")

API_KEY = st.secrets["TMDB_API_KEY"]
BASE_URL = st.secrets["TMDB_BASE_URL"]
IMG = st.secrets["TMDB_IMG_BASE"]
PLAYER = st.secrets["MOVIE_PLAYER"]

# ---------------------------------------------------
# STYLE
# ---------------------------------------------------

st.markdown("""
<style>

.stApp{
background:#071426;
}

/* poster cards */

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

/* section titles */

.section{
color:white;
font-size:26px;
margin-top:30px;
margin-bottom:15px;
}

/* hero */

.hero{
background:linear-gradient(to right,#000,#0b1a32);
padding:40px;
border-radius:14px;
margin-bottom:30px;
}

/* player */

.player-box{
background:#0b1a32;
padding:30px;
border-radius:16px;
margin-bottom:40px;
}

/* play button */

.play-btn button{
width:100%;
background:#e50914;
color:white;
border-radius:8px;
border:none;
}

/* responsive */

@media (max-width:900px){

.stColumn{
min-width:150px !important;
}

}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# API FUNCTIONS
# ---------------------------------------------------

def trending():

    r = requests.get(
        f"{BASE_URL}/trending/movie/week",
        params={"api_key": API_KEY}
    )

    return r.json()["results"]


def search_movies(q):

    r = requests.get(
        f"{BASE_URL}/search/multi",
        params={"api_key": API_KEY, "query": q}
    )

    data = r.json()["results"]

    return [x for x in data if x["media_type"] in ["movie","tv"]]


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
# PLAYER SECTION (TOP)
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

    st.markdown(
        f"""
        <div class="player-box">
        <h2 style="color:white;">{title}</h2>
        <p style="color:#bbb;">{overview}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <iframe
    src="{url}"
    width="100%"
    height="520"
    frameborder="0"
    allowfullscreen>
    </iframe>
    """, unsafe_allow_html=True)

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

    st.markdown('<div class="section">Trending Now</div>', unsafe_allow_html=True)

    movie_grid(trending())

# ---------------------------------------------------
# TRENDING
# ---------------------------------------------------

elif page == "Trending":

    st.markdown('<div class="section">Trending Movies</div>', unsafe_allow_html=True)

    movie_grid(trending())

# ---------------------------------------------------
# SEARCH
# ---------------------------------------------------

elif page == "Search":

    q = st.text_input("Search movies or series")

    if q:

        results = search_movies(q)

        movie_grid(results)

# ---------------------------------------------------
# AUTO SCROLL TO PLAYER
# ---------------------------------------------------

if st.session_state.get("scroll"):

    st.markdown(
        """
        <script>
        window.scrollTo({top:0, behavior:'smooth'});
        </script>
        """,
        unsafe_allow_html=True
    )

    st.session_state["scroll"] = False