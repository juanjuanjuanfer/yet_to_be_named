import streamlit as st
import pandas as pd
import utils
import film as scraper
import user as lbxd_user
import requests

st.set_page_config(page_title="Letterboxd Film Tracker", page_icon=":chart_with_upwards_trend:", layout="wide")
client = utils.login()
db = client.get_database("Letterboxd")

# Update the CSS to include centering styles
# Update the CSS to include better centering styles
page_css = """
<style>
/* Base theme colors */
:root {
    --primary-bg: #0F172A;
    --secondary-bg: #1E293B;
    --accent-color: #38BDF8;
    --text-primary: #F8FAFC;
    --text-secondary: #CBD5E1;
    --border-color: #334155;
}

/* Main layout elements */
[data-testid="stHeader"] {
    background-color: var(--primary-bg);
}

[data-testid="stMainBlockContainer"] {
    background-color: var(--secondary-bg);
}

[data-testid="stSidebarContent"] {
    background-color: var(--primary-bg);
    border-right: 1px solid var(--border-color);
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
    font-weight: 600;
}

p, span, div {
    color: var(--text-secondary);
    font-family: 'Inter', sans-serif;
}

/* Title styling */
.app-title {
    background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem;
    text-align: center;
    padding: 2rem 0;
    font-weight: 700;
}

/* Cards and containers */
.stat-card {
    background-color: var(--primary-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
    transition: transform 0.2s ease;
}

.stat-card:hover {
    transform: translateY(-2px);
}

/* Metrics and KPIs */
[data-testid="stMetricValue"] {
    color: var(--accent-color) !important;
    font-weight: 600;
}

[data-testid="stMetricDelta"] {
    background-color: rgba(56, 189, 248, 0.1);
    border-radius: 4px;
    padding: 0.25rem 0.5rem;
}

/* Input elements */
.stTextInput > div > div > input {
    background-color: var(--primary-bg);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    color: var(--text-primary);
    padding: 0.75rem;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent-color);
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
}

/* Buttons */
.stButton > button {
    background-color: #38BDF8;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #0EA5E9;
    transform: translateY(-1px) scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    cursor: pointer;
    transition: all 0.5s ease;
}

/* Movie grid */
.movie-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.5rem;
    padding: 1rem 0;
}

.movie-card {
    background-color: var(--primary-bg);
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.2s ease;
}

.movie-card:hover {
    transform: translateY(-4px);
}

/* Centered content */
.centered-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}

/* Images */
[data-testid="stImage"] {
    border-radius: 8px;
    overflow: hidden;
}

/* Select boxes */
.stSelectbox > div > div {
    background-color: var(--primary-bg);
    border: 1px solid var(--border-color);
    border-radius: 6px;
}
.st-emotion-cache-s16by7 {
    background-color: #0F172A !important;
}

.st-emotion-cache-s16by7:hover, 
.st-emotion-cache-s16by7[aria-selected="true"] {
    background-color: #10B981 !important;
}
/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--primary-bg);
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-color);
}
</style>
"""

st.markdown(page_css, unsafe_allow_html=True)

# Logo and Title - using a single column for better centering
st.markdown('<div class="centered-content">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,3,1])
with col2:
    st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True) # add image https://a.ltrbxd.com/logos/letterboxd-logo-v-neg-rgb.svg with markdown to center
    st.markdown('<div style="display: flex; justify-content: center;"><img src="https://a.ltrbxd.com/logos/letterboxd-logo-v-neg-rgb.svg" alt="Letterboxd Logo" style="width: 500px;">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="display: flex; justify-content: center;"><pre><pre>Letterboxd Film Tracker</h1>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# include video tutorial on how to use the app


movie = "the-substance"
collection = db[movie]
# get length of the collection
collection_count = collection.count_documents({})
film = scraper.Film()
film.set_film_name(movie)
film.get_film_data()
film.get_film_genres()
film_genres_str = ", ".join(film.filmGenres)
film.get_film_trailer()


# Movie Stats Section
st.markdown("## 📊 Top Movie Stats")
st.markdown('<br>', unsafe_allow_html=True)
st.markdown(f"### {film.filmRealName}")
col2, col3, col4 = st.columns(3)

with col2:
    st.metric(label="Total Reviews Scraped", value=f"{collection_count} 📈", delta="Around 3 more every 10 seconds")
with col3:
    st.metric(label="Average Rating", value=f"{film.filmAverageRating.__round__(1)}/10 ⭐")
with col4:
    st.metric(label="Film Genres", value= film_genres_str) # insert genres from a list of genres

# include a youtube video of the trailer
st.markdown(f"### 🎥 [Watch the Trailer]({film.filmTrailerLink})")

st.markdown('<br>', unsafe_allow_html=True)
# Quick Actions Section
st.markdown("## 🎯 Quick Actions")
col1, col2 = st.columns(2)
with col1:
    if st.button("Scrape Some Reviews 📝", use_container_width=True):
        # go to /Scraper
        st.switch_page("pages/Scraper.py")

with col2:
    if st.button("Get Some Metrics 📊", use_container_width=True):
        # go to /Metrics
        st.switch_page("pages/Dashboard.py")


# Movie Mood Selector
st.markdown("## Want to see someones letterboxd profile data? 🤔")
st.markdown('<br>', unsafe_allow_html=True)
col_1, col_2, col_3 = st.columns(3)
with col_1:
    data_username = st.text_input("Enter a username", key="username")
    
with col_2:
    show_user = lbxd_user.PyBoxd.user()
    show_user.set_username(data_username)
    show_user.get_profile_stats()
    st.markdown(f"### Total watched films: {show_user.films}")
    st.markdown(f"### Total watched films this year: {show_user.thisYear}")
    st.markdown(f"### Total followers: {show_user.followers}")
    st.markdown(f"### Total following: {show_user.following}")
with col_3:
    st.markdown(f"## Favorite films:")
    for film in show_user.favoriteFilms:
        st.markdown(f"### {film}")

st.markdown("## See the creators' favorite movies below. 😉")
# select an option from a list of users
users = ["Juan Fernandez", "Juliana Ramayo", "Angel Sansores", "Yahir Sulu"]
users_username = ["fer_nwn", "julisramayoc", "asansores16", "yah1rrr"]

st.session_state["Select a user"] = st.selectbox("Select a user", users)
if "Select a user" in st.session_state:
    user_selection = lbxd_user.PyBoxd.user()
    user_selection.set_username(users_username[users.index(st.session_state["Select a user"])])
    user_selection.get_profile_stats()
    fav_films = user_selection.favoriteFilms

    st.markdown(f"### Creator's Favorite Movies")
    fav_movie_col1, fav_movie_col2, fav_movie_col3 , fav_movie_col4 = st.columns(4)
    with fav_movie_col1:
        #initialize the first movie
        fav_movie_1 = scraper.Film()
        fav_movie_1.set_film_name(fav_films[0])
        fav_movie_1.get_film_data()
        # verify if the poster is available
        favpost1 = requests.get(fav_movie_1.filmPoster)
        if favpost1.status_code != 200:
            st.image("https://s.ltrbxd.com/static/img/empty-poster-70.8112b435.png", caption="Sorry, the poster is not available", use_column_width=True)
        else:
            st.image(fav_movie_1.filmPoster, caption=user_selection.favoriteFilms[0], use_column_width=True)
        movie_link = f"https://letterboxd.com/film/{fav_movie_1.filmName}"
        st.markdown(f"[{fav_movie_1.filmRealName}]({movie_link})")

    with fav_movie_col2:
        fav_movie_2 = scraper.Film()
        fav_movie_2.set_film_name(fav_films[1])
        fav_movie_2.get_film_data()
        favpost2 = requests.get(fav_movie_2.filmPoster)
        if favpost2.status_code != 200:
            st.image("https://s.ltrbxd.com/static/img/empty-poster-70.8112b435.png", caption="Sorry, the poster is not available", use_column_width=True)
        else:
            st.image(fav_movie_2.filmPoster, caption=user_selection.favoriteFilms[1], use_column_width=True)
        movie_link2 = f"https://letterboxd.com/film/{fav_movie_2.filmName}"
        st.markdown(f"[{fav_movie_2.filmRealName}]({movie_link2})")
    with fav_movie_col3:
        fav_movie_3 = scraper.Film()
        fav_movie_3.set_film_name(fav_films[2])
        fav_movie_3.get_film_data()
        favpost3 = requests.get(fav_movie_3.filmPoster)
        if favpost1.status_code != 200:
            st.image("https://s.ltrbxd.com/static/img/empty-poster-70.8112b435.png", caption="Sorry, the poster is not available", use_column_width=True)
        else:
            st.image(fav_movie_3.filmPoster, caption=user_selection.favoriteFilms[2], use_column_width=True)
        movie_link3 = f"https://letterboxd.com/film/{fav_movie_3.filmName}"
        st.markdown(f"[{fav_movie_3.filmRealName}]({movie_link3})")
    with fav_movie_col4:
        fav_movie_4 = scraper.Film()
        fav_movie_4.set_film_name(fav_films[3])
        fav_movie_4.get_film_data()
        favpost4 = requests.get(fav_movie_4.filmPoster)
        if favpost4.status_code != 200:
            st.image("https://s.ltrbxd.com/static/img/empty-poster-70.8112b435.png", caption="Sorry, the poster is not available", use_column_width=True)
        else:
            st.image(fav_movie_4.filmPoster, caption=user_selection.favoriteFilms[3], use_column_width=True)
        movie_link4 = f"https://letterboxd.com/film/{fav_movie_4.filmName}"
        st.markdown(f"[{fav_movie_4.filmRealName}]({movie_link4})")

st.markdown('<br>', unsafe_allow_html=True)
st.markdown("## 🎥 Short tutorial on how to use the app.")
VIDEO_URL = "https://youtu.be/jOWh8_mT9jc"
st.video(VIDEO_URL)