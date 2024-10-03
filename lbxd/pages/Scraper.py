import streamlit as st
import connection_mongo
import film as scraper

# Set page title
st.title('Letterboxd Scraper')

# Establish MongoDB connection
client = connection_mongo.connect_to_mongo("-", "-")
db = client.get_database("Letterboxd")

# Initialize session state for movie, scraping status, and scrape amount if not already done
if 'movie' not in st.session_state:
    st.session_state['movie'] = ''
if 'scrape_status' not in st.session_state:
    st.session_state['scrape_status'] = 'No movie scraped yet.'
if 'scrape_amount' not in st.session_state:
    st.session_state['scrape_amount'] = ''
if 'film_data' not in st.session_state:
    st.session_state['film_data'] = {}

# User input for movie name
user_input = st.text_input('Enter the movie you want to scrape:', st.session_state['movie'])
st.session_state['movie'] = user_input  # Save movie to session state



# Button to scrape the movie
if st.button('Click to scrape'):
    if user_input:
        film = scraper.Film()
        film.set_film_name(st.session_state['movie'])
        
        # Scrape movie poster
        film_poster = film.scrape_film_poster(film.filmMainSoup, film.filmName)

        # Save film data to session state
        st.session_state['film_data'] = {
            'name': film.filmName,
            'year': film.filmReleaseYear,
            'directors': film.filmDirectors["Directors"],
            'rating': film.filmAverageRating,
            'poster': film_poster
        }

        # Update scraping status
        st.session_state['scrape_status'] = f'Successfully scraped {film.filmName}'

# Display movie information if it exists
if st.session_state['film_data']:
    st.write(f"{st.session_state['film_data']['name']} | {st.session_state['film_data']['year']}")
    st.write(f'Directed by: {st.session_state["film_data"]["directors"]}')
    st.write(f'Rating: {st.session_state["film_data"]["rating"]:.1f} / 10')
    st.write(f'https://letterboxd.com/film/{st.session_state["film_data"]["name"]}/')

    # Display the scraped image
    image_url = st.session_state['film_data']['poster']
    st.markdown(f'<br><div style="text-align:center;"><img src="{image_url}" alt="Movie Image" width="300"></div><br>', unsafe_allow_html=True)

# Text input for scrape amount
st.write("If the movie is not popular recently, it is recommended to scrape more reviews at once, as if the scraper is run again, it will probably scrape the same reviews.")
scrape_amount_input = st.text_input("Number of recent reviews to scrape:", st.session_state['scrape_amount'])
st.session_state['scrape_amount'] = scrape_amount_input  # Save scrape amount to session state

# Button to scrape reviews
if st.button('Scrape Reviews'):
    if st.session_state['scrape_amount'] and st.session_state['film_data']:
        try:
            scrape_amount = int(st.session_state['scrape_amount']) // 12 + (int(st.session_state['scrape_amount']) % 12 > 0)
            st.write(f"Scraping {scrape_amount * 12} recent reviews.")

            # Scrape reviews
            reviews = scraper.Film.FilmReview(st.session_state['film_data']['name'])
            reviews.get_film_reviews(scrape_amount)
            data = reviews.filmReviews
            collection = db[st.session_state['movie']]
            
            for review in data:
                if not collection.find_one({"review_id": review['review_id']}):
                    collection.insert_one(review)
                    print(f"Review with ID {review['review_id']} inserted into the database.")
                else:
                    print(f"Review with ID {review['review_id']} already exists in the database.")

            # Update scraping status
            st.session_state['scrape_status'] = f'Successfully scraped {len(data)} reviews for {st.session_state["film_data"]["name"]}.'


        except ValueError:
            st.error("Please enter a valid number for scraping reviews.")
    else:
        st.warning("Please scrape a movie first before scraping reviews.")

# If scraping was done, display the last scraped movie
if 'scrape_status' in st.session_state and st.session_state['scrape_status'] != 'No movie scraped yet.':
    st.write(f"Last scraped movie: {st.session_state['movie']}")
