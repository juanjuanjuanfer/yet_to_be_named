import streamlit as st
import pandas as pd
import film as scraper
import utils

st.set_page_config(page_title="Letterboxd Film Tracker", page_icon="🎬", layout="wide")

# Enhanced CSS with the movie tracker theme
page_css = """
<style>
/* Set the background color */
.main {
        background-color: #1e1e1e;
    }
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
.st-emotion-cache-s16by7,
li[role="option"].st-emotion-cache-s16by7 {
    background-color: #0F172A !important;
}

.st-emotion-cache-s16by7:hover, 
.st-emotion-cache-s16by7[aria-selected="true"],
li[role="option"].st-emotion-cache-s16by7:hover,
li[role="option"].st-emotion-cache-s16by7[aria-selected="true"] {
    background-color: #10B981 !important;
    color: white !important;
}

/* Ensure text is visible */
.st-emotion-cache-sy3zga {
    color: #F8FAFC !important;
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

# Main title with gradient effect
st.markdown('<h1 class="gradient-text">Letterboxd Dashboard</h1>', unsafe_allow_html=True)

# Initialize session states
if 'movie' not in st.session_state:
    st.session_state['movie'] = ''

# Create two columns for the layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎬 Select Movie")
    st.markdown("Recommended to choose a movie with at least 500 reviews for better insights.")
    # Get base movie names first
    base_movies = db.list_collection_names()
    # Create display names with review counts
    movies_display = [movie + f" ({db[movie].count_documents({})} reviews)" for movie in base_movies]
    # Create a dictionary to map display names back to base names
    movie_map = dict(zip(movies_display, base_movies))
    
    # Use display names in selectbox
    selected_movie_display = st.selectbox('🎥 Select a movie:', options=movies_display, index=0, key='movie_selector')
    
    # Get the actual movie name from our mapping
    actual_movie_name = movie_map[selected_movie_display]

    if st.button('🔄 Update Selection'):
        st.session_state['movie'] = actual_movie_name
        st.markdown(f"""
            <div class="movie-card">
                <h3>🎯 Selected Film: {st.session_state['movie']}</h3>
                <h5> Total Reviews: {db[st.session_state['movie']].count_documents({})} </h5>
            </div>
        """, unsafe_allow_html=True)
if st.session_state['movie']:
    collection = db[st.session_state['movie']]
    
    # Get movie information
    film = scraper.Film()
    film.set_film_name(st.session_state['movie'])
    film_poster = film.scrape_film_poster(film.filmMainSoup, film.filmName)
    film_rating = film.scrape_average_rating(film.filmName)
    
    # Calculate average rating
    film_rating = (sum([key * value for key, value in enumerate(film_rating.values(), start=1)]) / sum(film_rating.values()) * 10).__round__(0)

    # Display movie poster and information
    st.markdown("""
        <div class="movie-card">
            <div style="text-align: center;">
                <img src="{}" alt="Movie Poster" style="max-width: 300px; border-radius: 10px;">
            </div>
        </div>
    """.format(film_poster), unsafe_allow_html=True)

    # Rating gauge
    st.markdown("### ⭐ Rating Overview")
    fig = utils.get_gauge_plot(score=film_rating, range_axis=100, title="Overall Rating")
    st.plotly_chart(fig)

    # Ratings distribution
    data = list(collection.find({'rating': {'$exists': True}}).sort([('$natural', -1)]))
    
    if data:
        st.markdown("### 📊 Ratings Distribution")
        ratings = [x["rating"] for x in data]
        symbol_to_number = {'½': 1, '★': 2, '★½': 3, '★★': 4, '★★½': 5, '★★★': 6, '★★★½': 7, '★★★★': 8, '★★★★½': 9, '★★★★★': 10}
        ratings_mapped = [symbol_to_number.get(r, 0) for r in ratings]
        rating_df = pd.DataFrame({'Ratings': ratings_mapped})
        count_ratings = rating_df['Ratings'].value_counts().sort_index()
        
        with st.container():
            fig2 = utils.get_vertical_bar_chart(count_ratings)
            st.pyplot(fig2)
            st.markdown('</div>', unsafe_allow_html=True)

        # Ratings by date
        st.markdown("### 📅 Ratings Timeline")
        dates = collection.distinct('date', {'rating': {'$exists': True}})
        dates = [x for x in dates if x != ""]

        if dates:
            if 'selected_date' not in st.session_state:
                st.session_state['selected_date'] = None

            st.session_state['selected_date'] = st.selectbox('📆 Select a date to analyze:', options=dates, index=0)

            ratings_2 = list(collection.aggregate([
                {'$match': {'date': st.session_state['selected_date'], 'rating': {'$exists': True}}},
                {'$group': {'_id': '$rating', 'count': {'$sum': 1}}}
            ]))

            ratings_dict = {item['_id']: item['count'] for item in ratings_2}
            ratings_dict = dict(sorted(ratings_dict.items()))

            if ratings_dict:
                ratings_3 = list(ratings_dict.keys())
                counts = list(ratings_dict.values())

                with st.container():
                    st.subheader(f'📊 Ratings for {st.session_state["selected_date"]}')
                    fig_3 = utils.get_horizontal_bar_chart(ratings_3, counts)
                    st.pyplot(fig_3)
                    st.markdown('</div>', unsafe_allow_html=True)

        # Sentiment Analysis Section
        st.markdown("### 🎭 Sentiment Analysis")
        n = st.number_input("📝 Number of recent reviews to analyze:", min_value=1, max_value=1000, value=10, step=1)

        if st.checkbox(f'✨ Analyze last {n} reviews'):
            with st.spinner('Analyzing sentiments...'):
                data = list(collection.find({'rating': {'$exists': True}}).sort([('$natural', -1)]).limit(n))
                result = [x["review_text"] for x in data if "review_text" in x]
                result_date = [x["date"] for x in data if "date" in x]
                
                min_size = min(len(result), len(result_date))
                result = result[:min_size]
                result_date = result_date[:min_size]

                result = [utils.clean_review(str(review)) for review in result]
                sentiment_result = [utils.get_sentimet(str(review)) for review in result]
                result = pd.DataFrame({'Review': result, 'Sentiment': sentiment_result})

                with st.container():
                    st.dataframe(result, width=10000)
                    
                    sentiment_count = result['Sentiment'].value_counts()
                    total = sentiment_count.sum()
                    
                    fig_sentiment = utils.get_sentiment_plot(sentiment_count, total)
                    st.pyplot(fig_sentiment)
                    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
        <div class="movie-card">
            <h3>👋 Welcome to the Letterboxd Dashboard!</h3>
            <p>Enter a movie name above and click 'Update Selection' to begin exploring.</p>
        </div>
    """, unsafe_allow_html=True)
