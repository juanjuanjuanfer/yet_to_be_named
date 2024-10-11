import streamlit as st
import time
import utils
import film
from re import search
import toml

def autoscraper(film_name:str):
    client = utils.login()
    db = client["Letterboxd"]
    collection = db[film_name]
    movie = film.Film.FilmReview(film_name)
    movie.get_film_reviews()
    data = movie.filmReviews
    for review in data:
        if not collection.find_one({"review_id": review['review_id']}):
            collection.insert_one(review)
            st.write(f"Inserted review {review['review_id']} into the database.")
        else:
            st.write(f"Review {review['review_id']} already exists in the database.")


st.markdown("# Autoscraper")
# login to interact
st.markdown("Login to Interact")
user = st.text_input("Enter your username:")
passw = st.text_input("Enter your password:", type="password")
if st.button("Login"):
    # check from secrets.toml
    with open(".streamlit/secrets.toml", "r") as f:
        secrets = f.read()
        secrets_dict = toml.loads(secrets)
        if user == secrets_dict["autoscraper"]["user"] and passw == secrets_dict["autoscraper"]["pass"]:

            film_name = st.text_input("Enter movie name:")
            if st.button("Scrape"):
                for i in range(1000):
                    autoscraper(film_name)
                    time.sleep(5)
        else:
            st.write("Invalid username or password.")
            st.markdown('<img src="https://media1.tenor.com/m/7Rw8rOLsNOEAAAAC/moodeng.gif" width="800"/>', unsafe_allow_html=True)