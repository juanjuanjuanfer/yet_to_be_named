import streamlit as st
import connection_mongo
import film as scraper

# Set page title
st.title('Letterboxd Scraper')

page_css = """
<style>
[data-testid="stHeader"]{
    background-color: #0E1217;
}
[id="letterboxd-scraper"] {
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
    color: transparent;
    display: inline-block;
}
[data-testid="stSidebarContent"]{
    background-color: #0E1217;
    color: #FFFFFF;
}
[data-testid="stMainBlockContainer"]{
    background-color: #202830;
}
[data-testid="stMain"]{
    background-color: #202830;
    color: #FFFFFF;
}
[aria-label="Enter the movie you want:"]{
    background-color: #FFFFFF;
    color: #000000;
}
[data-testid="stBaseButton-secondary"]{
    background-color: #FFFFFF;
    color: #000000;
    border: 2px solid #28a745 !important;  /* Green border */
    transition: all 0.3s ease;  /* Smooth transition for hover effect */
}
[data-testid="stBaseButton-secondary"]:hover {
    border-color: #00E153 !important;  /* Red border on hover */
    transform: scale(1.3);  /* Slightly enlarge button on hover */
    color: #00E153;
}
[aria-label="Enter the movie you want to scrape:"], [aria-label="Number of recent reviews to scrape:"]{
    background-color: #FFFFFF;
    color: #000000;
    border: 1px solid #000000;
    secondaryBackgroundColor= #FFFFFF;
}
.success-message {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #28a745;
    color: white;
    margin: 1rem 0;
}
</style>
"""

st.markdown(page_css, unsafe_allow_html=True)

# Establish MongoDB connection
client = connection_mongo.connect_to_mongo("-", "-")
db = client.get_database("Letterboxd")

# Initialize session state
if 'movie' not in st.session_state:
    st.session_state['movie'] = ''
if 'scrape_status' not in st.session_state:
    st.session_state['scrape_status'] = 'No movie scraped yet.'
if 'scrape_amount' not in st.session_state:
    st.session_state['scrape_amount'] = ''
if 'film_data' not in st.session_state:
    st.session_state['film_data'] = {}
if 'progress' not in st.session_state:
    st.session_state['progress'] = 0

# User input for movie name
user_input = st.text_input('Enter the movie you want to scrape:', st.session_state['movie'])
st.session_state['movie'] = user_input

# Button to scrape the movie
if st.button('Click to set movie'):
    if user_input:
        with st.spinner('Fetching movie information...'):
            film = scraper.Film()
            film.set_film_name(st.session_state['movie'])
            film_poster = film.scrape_film_poster(film.filmMainSoup, film.filmName)
            
            st.session_state['film_data'] = {
                'name': film.filmName,
                'year': film.filmReleaseYear,
                'directors': film.filmDirectors["Directors"],
                'rating': film.filmAverageRating,
                'poster': film_poster
            }
            
            st.session_state['scrape_status'] = f'Successfully scraped {film.filmName}'
        st.success('Movie information fetched successfully! ✅')

# Display movie information if it exists
if st.session_state['film_data']:
    st.write(f"{st.session_state['film_data']['name']} | {st.session_state['film_data']['year']}")
    st.write(f'Directed by: {st.session_state["film_data"]["directors"]}')
    st.write(f'Rating: {st.session_state["film_data"]["rating"]:.1f} / 10')
    st.write(f'https://letterboxd.com/film/{st.session_state["film_data"]["name"]}/')
    
    image_url = st.session_state['film_data']['poster']
    st.markdown(f'<br><div style="text-align:center;"><img src="{image_url}" alt="Movie Image" width="300"></div><br>', unsafe_allow_html=True)

st.write("If the movie is not popular recently, it is recommended to scrape more reviews at once, as if the scraper is run again, it will probably scrape the same reviews.")
scrape_amount_input = st.text_input("Number of recent reviews to scrape:", st.session_state['scrape_amount'])
st.session_state['scrape_amount'] = scrape_amount_input

# Button to scrape reviews
if st.button('Scrape Reviews'):
    if st.session_state['scrape_amount'] and st.session_state['film_data']:
        try:
            scrape_amount = int(st.session_state['scrape_amount']) // 12 + (int(st.session_state['scrape_amount']) % 12 > 0)
            st.write(f"Scraping {scrape_amount * 12} recent reviews.")
            
            # Create a progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Scrape reviews
            with st.spinner('Scraping reviews...'):
                reviews = scraper.Film.FilmReview(st.session_state['film_data']['name'])
                reviews.get_film_reviews(scrape_amount)
                data = reviews.filmReviews
                collection = db[st.session_state['movie']]
                
                # Initialize counters
                total_reviews = len(data)
                processed_reviews = 0
                new_reviews = 0
                
                for review in data:
                    if not collection.find_one({"review_id": review['review_id']}):
                        collection.insert_one(review)
                        new_reviews += 1
                        status_text.text(f"Inserting new review {new_reviews}")
                    
                    processed_reviews += 1
                    progress = int(processed_reviews / total_reviews * 100)
                    progress_bar.progress(progress)
                
                # Show completion message
                st.markdown(f"""
                    <div class="success-message">
                        ✅ Scraping completed successfully!<br>
                        • Total reviews processed: {processed_reviews}<br>
                        • New reviews added: {new_reviews}<br>
                        • Movie: {st.session_state["film_data"]["name"]}
                    </div>
                """, unsafe_allow_html=True)
                
                st.session_state['scrape_status'] = f'Successfully scraped {len(data)} reviews for {st.session_state["film_data"]["name"]}.'

        except ValueError:
            st.error("Please enter a valid number for scraping reviews.")
    else:
        st.warning("Please scrape a movie first before scraping reviews.")

# If scraping was done, display the last scraped movie
if 'scrape_status' in st.session_state and st.session_state['scrape_status'] != 'No movie scraped yet.':
    st.write(f"Last scraped movie: {st.session_state['movie']}")