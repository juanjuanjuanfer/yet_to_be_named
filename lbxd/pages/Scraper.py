import streamlit as st
import film as scraper
import utils

st.set_page_config(page_title="Letterboxd Scraper", page_icon="🎬", layout="wide")

# Enhanced CSS with the movie tracker theme
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
    color: #FFFFFF;
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
    display: inline-block;
}

.stTextInput > div > div > input {
    background-color: #1A232C;
    color: #FFFFFF;
    border: 1px solid #3EBDF4;
    border-radius: 5px;
}

.stButton > button {
    background: linear-gradient(
        to right,
        #FF8100,
        #00E153
    );
    color: white;
    border: none;
    border-radius: 5px;
    padding: 0.5rem 2rem;
    transition: transform 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.05);
}

.movie-card {
    background-color: #1A232C;
    padding: 2rem;
    border-radius: 10px;
    margin: 1rem 0;
    border: 1px solid #3EBDF4;
}

.success-message {
    background: linear-gradient(to right, #00E153, #3EBDF4);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}

.warning-message {
    background: linear-gradient(to right, #FF8100, #FF8100);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}

div[data-testid="stProgressBar"] > div {
    background: linear-gradient(to right, #FF8100, #00E153, #3EBDF4);
}
</style>
"""

st.markdown(page_css, unsafe_allow_html=True)

# Initialize MongoDB connection
client = utils.login()
db = client.get_database("Letterboxd")

# Initialize session states
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

# Page Header with gradient text
st.markdown('<h1 class="gradient-text">Letterboxd Scraper</h1>', unsafe_allow_html=True)

# Create two columns for the layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎬 Search Movie")
    user_input = st.text_input('Enter the movie you want to scrape:', st.session_state['movie'])
    st.session_state['movie'] = user_input

    if st.button('Set Movie'):
        if user_input:
            with st.spinner('🔍 Fetching movie information...'):
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
            st.success('✨ Movie information fetched successfully!')

with col2:
    if st.session_state['film_data']:
        st.markdown("""
            <div class="movie-card">
                <div style="text-align: center;">
                    <img src="{}" alt="Movie Poster" style="max-width: 200px; border-radius: 10px;">
                </div>
            </div>
        """.format(st.session_state['film_data']['poster']), unsafe_allow_html=True)

# Movie Information Section
if st.session_state['film_data']:
    st.markdown("""
        <div class="movie-card">
            <h2>{} ({})</h2>
            <p>👤 Directed by: {}</p>
            <p>⭐ Rating: {:.1f} / 10</p>
            <p>🔗 <a href="https://letterboxd.com/film/{}" style="color: #3EBDF4;">View on Letterboxd</a></p>
        </div>
    """.format(
        st.session_state['film_data']['name'],
        st.session_state['film_data']['year'],
        st.session_state['film_data']['directors'],
        st.session_state['film_data']['rating'],
        st.session_state['film_data']['name']
    ), unsafe_allow_html=True)

# Review Scraping Section
st.markdown("### 📊 Review Scraping")
st.markdown("""
    <div class="warning-message">
        ⚠️ Note: For less popular movies, it's recommended to scrape more reviews at once, as subsequent scrapes might yield duplicate reviews.
    </div>
""", unsafe_allow_html=True)

scrape_amount_input = st.text_input("Number of recent reviews to scrape:", st.session_state['scrape_amount'])

# Rest of your scraping logic with updated styling for progress bars and messages
try:
    scrape_amount = int(scrape_amount_input)
    if scrape_amount < 0 or scrape_amount > 5000:
        st.error("Please enter a number between 0 and 5000")
    else:
        if scrape_amount > 500:
            st.markdown("""
                <div class="warning-message">
                    ⚠️ Scraping more than 500 reviews may take a while.
                </div>
            """, unsafe_allow_html=True)
            password = st.text_input("Enter the password to confirm scraping:", type="password")
            if password != "soyadmin":
                st.error("❌ Incorrect password")
            else:
                st.session_state['scrape_amount'] = scrape_amount
                if st.button('Start Scraping'):
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
            st.session_state['scrape_amount'] = scrape_amount
            if st.button('Start Scraping'):
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
except ValueError:
    if scrape_amount_input:
        st.error("❌ Please enter a valid number")

# Display last scraped movie
if 'scrape_status' in st.session_state and st.session_state['scrape_status'] != 'No movie scraped yet.':
    st.markdown(f"""
        <div class="movie-card">
            <p>🎬 Last scraped movie: {st.session_state['movie']}</p>
        </div>
    """, unsafe_allow_html=True)