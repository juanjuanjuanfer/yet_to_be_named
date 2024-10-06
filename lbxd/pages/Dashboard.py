import streamlit as st
import pandas as pd
import film as scraper
import utils

st.set_page_config(page_title="Letterboxd Film Tracker", page_icon="🎬", layout="wide")

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

.stats-card {
    background-color: #1A232C;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    border: 1px solid #00E153;
}

.sentiment-card {
    background-color: #1A232C;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    border: 1px solid #FF8100;
}

[data-baseweb="select"] {
    background-color: #1A232C;
    color: #FFFFFF;
    border: 1px solid #3EBDF4;
    border-radius: 5px;
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

# Main title with gradient effect
st.markdown('<h1 class="gradient-text">Letterboxd Dashboard</h1>', unsafe_allow_html=True)

# Initialize session states
if 'movie' not in st.session_state:
    st.session_state['movie'] = ''

# Create two columns for the layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎬 Select Movie")
    user_input = st.text_input('Enter the movie you want:', st.session_state['movie'])

    if st.button('🔄 Update Selection'):
        st.session_state['movie'] = user_input
        st.markdown(f"""
            <div class="movie-card">
                <h3>🎯 Selected Film: {st.session_state['movie']}</h3>
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
