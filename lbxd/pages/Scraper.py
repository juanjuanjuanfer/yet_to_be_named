import streamlit as st
import film as scraper
import utils

st.set_page_config(page_title="Letterboxd Scraper", page_icon="🎬", layout="wide")

# Enhanced CSS with the movie tracker theme
page_css = """
<style>
/* Base theme colors */
:root {
    --primary-bg: #0F172A;
    --secondary-bg: #1E293B;
    --accent-orange: #F97316;
    --accent-green: #10B981;
    --accent-blue: #CBD5E1;
    --text-primary: #F8FAFC;
    --text-secondary: #CBD5E1;
    --border-color: #334155;
    --card-bg: #1E293B;
    --hover-bg: #2D3B4F;
}

/* Main layout elements */
[data-testid="stHeader"],
[data-testid="stToolbar"] {
    background-color: var(--primary-bg);
}

[data-testid="stMainBlockContainer"],
[data-testid="stMain"] {
    background-color: var(--secondary-bg);
    color: var(--text-primary);
}

[data-testid="stSidebarContent"] {
    background-color: var(--primary-bg);
    border-right: 1px solid var(--border-color);
}

/* Typography */
h1, h2, h3, h4, h5, h6, p, span, div {
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
}

/* Gradient text effect */
.gradient-text {
    background: #CBD5E1;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
    text-align: center;
    padding: 1.5rem 0;
    font-size: 2.5rem;
}



/* Input elements */
.stTextInput > div > div > input {
    background-color: var(--card-bg);
    color: var(--text-primary);
    border: 1px solid var(--accent-blue);
    border-radius: 8px;
    padding: 0.75rem;
    transition: all 0.2s ease;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent-blue);
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
}

/* Buttons */
.stButton > button {
    background: #2D3B4F;
    color: var(--text-primary);
    border: none;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.stButton > button:hover {
/* change color to whiteish blue */
    transform: translateY(-2px) scale(1.02) translateZ(0) !important ; 
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    background: #0F172A;
}

/* Cards */
.movie-card {
    background-color: var(--card-bg);
    padding: 2rem;
    border-radius: 12px;
    margin: 1rem 0;
    border: 1px solid var(--accent-blue);
    transition: all 0.3s ease;
}

.movie-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(56, 189, 248, 0.1);
}

.stats-card {
    background-color: var(--card-bg);
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    border: 1px solid var(--accent-green);
    transition: all 0.3s ease;
}

.sentiment-card {
    background-color: var(--card-bg);
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    border: 1px solid var(--accent-orange);
    transition: all 0.3s ease;
}

/* Messages */
.success-message {
    background: linear-gradient(135deg,
        var(--accent-green) 0%,
        var(--accent-blue) 100%
    );
    color: var(--text-primary);
    padding: 1.25rem;
    border-radius: 8px;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);
}

.warning-message {
    background: #0F172A;
    color: var(--text-primary);
    padding: 1.25rem;
    border-radius: 8px;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(249, 115, 22, 0.1);
}

/* Select boxes */
[data-baseweb="select"],
.stSelectbox > div > div {
    background-color: var(--card-bg);
    color: var(--text-primary);
    border: 1px solid var(--accent-blue);
    border-radius: 8px;
}


/* Progress bars */
div[data-testid="stProgressBar"] {
    border-radius: 8px;
    overflow: hidden;
}

div[data-testid="stProgressBar"] > div {
    background: linear-gradient(135deg,
        var(--accent-orange) 0%,
        var(--accent-green) 50%,
        var(--accent-blue) 100%
    );
}

/* Images */
[data-testid="stImage"] img {
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

[data-testid="stImage"] img:hover {
    transform: scale(1.02);
}

/* DataFrames */
[data-testid="stDataFrame"] {
    background-color: var(--card-bg);
    border-radius: 8px;
    overflow: hidden;
}

.stDataFrame th {
    background-color: var(--primary-bg);
    color: var(--text-primary);
}

.stDataFrame td {
    color: var(--text-secondary);
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: var(--accent-blue);
    font-weight: 700;
}

[data-testid="stMetricDelta"] {
    background-color: rgba(56, 189, 248, 0.1);
    border-radius: 4px;
    padding: 0.25rem 0.5rem;
}

/* Plots */
[data-testid="stPlotlyChart"] > div {
    background-color: var(--card-bg);
    border-radius: 12px;
    padding: 1rem;
}

/* Scrollbar */
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
    background: var(--accent-blue);
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
    st.markdown("Enter the movie you want to scrape and click the button to set the movie.")
    st.markdown("The movie name should be the same as on Letterboxd and with Letterboxd's film slug format. e.g. 'the-substance' for movie 'The Substance'.")
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