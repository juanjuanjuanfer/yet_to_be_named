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
[data-testid="stHeader"] {
    background-color: #0E1217;
    color: #FFFFFF;
}

[data-testid="stMainBlockContainer"] {
    background-color: #202830;
    color: #FFFFFF;
}

[data-testid="stMain"] {
    background-color: #202830;
}

[data-testid="stSidebarContent"] {
    background-color: #0E1217;
    color: #FFFFFF;
}

.gradient-text {
    background: linear-gradient(
        to right,
        #FF8100 0%,
        #FF8100 30%,
        #00E153 35%,
        #00E153 65%,
        #3EBDF4 70%,
        #3EBDF4 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
}

.centered-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

[data-testid="column"] {
    display: flex;
    justify-content: center;
    align-items: center;
}

[data-testid="stImage"] {
    display: block;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
}

.stat-card {
    background-color: #1A232C;
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
}

.action-button {
    background-color: #FF8100;
    border: none;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    margin: 5px;
}
.stTextInput > div > div > input {
    background-color: #FFFFFF;
    color: #000000;
    border: 1px solid #3EBDF4;
    border-radius: 5px;
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
    st.markdown('<h1 class="gradient-text"><pre><pre>Letterboxd Film Tracker</h1>', unsafe_allow_html=True)
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