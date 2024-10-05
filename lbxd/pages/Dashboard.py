import streamlit as st
import pandas as pd
import film as scraper
import utils





# Establish MongoDB connection
client = utils.login()
db = client.get_database("Letterboxd")

# Set page title
st.set_page_config(page_title="Letterboxd Film Tracker", page_icon=":chart_with_upwards_trend:")

# css for the page with background color #1A232C
# pallete :#1A232C #FF8100 #FFFFFF #3EBDF4 #00E153
page_css = """
<style>
[data-testid="stHeader"]{
    background-color: #0E1217;
}
[id="letterboxd-dashboards"] {
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
[aria-label="Enter the movie you want:"]:hover{
    background-color: #FFFFFF;
    color: #000000;
    border-color: #00E153
}
[data-testid="stBaseButton-secondary"]{
    background-color: #FFFFFF;
    color: #000000;
    border: 2px solid #28a745 !important;  /* Green border */
    transition: all 0.3s ease;  /* Smooth transition for hover effect */
}
[data-testid="stBaseButton-secondary"]:hover {
    border-color: #00E153 !important;  /* Red border on hover */
    transform: scale(1.8);  /* Slightly enlarge button on hover */
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
[data-baseweb="select"]{
    background-color: #FF8100;
    color: #FFFFFF;
    border: 1px solid #000000;
    secondaryBackgroundColor= #FF8100;
    border-radius: 0.5rem;

    }
[data-baseweb="select"] > div{
    background-color: #FF8100;
    color: #FFFFFF;
    border: 1px solid #000000;
    secondaryBackgroundColor= #FFFFFF;
}

[data-baseweb="input"]{
    background-color: #FF8100;
    color: #FFFFFF;
    border: 1px solid #000000;
    secondaryBackgroundColor= #FF8100;
    border-radius: 0.5rem;

    }
[data-baseweb="input"] > div{
    background-color: #FF8100;
    color: #FFFFFF;
    border: 1px solid #000000;
    secondaryBackgroundColor= #FFFFFF;
}



</style>
"""


st.markdown(page_css, unsafe_allow_html=True)


# Main title
st.title('Letterboxd Dashboards')

# Main content
st.header('Movie Stats')

# Text input (default empty) and store the movie in session state
if 'movie' not in st.session_state:
    st.session_state['movie'] = ''

user_input = st.text_input('Enter the movie you want:', st.session_state['movie'])

# Button to change the selected movie and store it in session state
if st.button('Click to change'):
    st.session_state['movie'] = user_input
    st.write(f'Selected film: {st.session_state["movie"]}')
    collection = db[st.session_state['movie']]

# Only proceed if a movie has been selected
if st.session_state['movie']:
    collection = db[st.session_state['movie']]

    film = scraper.Film()
    film.set_film_name(st.session_state['movie'])
    film_poster = film.scrape_film_poster(film.filmMainSoup, film.filmName)
    film_rating = film.scrape_average_rating(film.filmName)

    # get the mean for al values in the dictionary
    film_rating = (sum([key * value for key, value in enumerate(film_rating.values(), start=1)]) / sum(film_rating.values()) * 10).__round__(0)

    st.markdown(
        f'<div style="text-align:center;"><img src="{film_poster}" alt="Movie Image" width="300"></div>',
        unsafe_allow_html=True
    )

    # Gauge plot for Rating 
    fig =  utils.get_gauge_plot(score=film_rating, range_axis=100, title="Rating")
    st.plotly_chart(fig)

    
    
    data = list(collection.find({'rating': {'$exists': True}}).sort([('$natural', -1)]))

    if data:
        # Extract the ratings
        ratings = [x["rating"] for x in data]
        
        # Mapping rating symbols to numbers
        symbol_to_number = {'½': 1, '★': 2, '★½': 3, '★★': 4, '★★½': 5, '★★★': 6, '★★★½': 7, '★★★★': 8, '★★★★½': 9, '★★★★★': 10}

        ratings_mapped = [symbol_to_number.get(r, 0) for r in ratings]  # Replace symbols with numbers
        
        # Create a DataFrame with the mapped ratings
        rating_df = pd.DataFrame({'Ratings': ratings_mapped})
        
        # Count the ratings
        count_ratings = rating_df['Ratings'].value_counts().sort_index()
        
        fig2 = utils.get_vertical_bar_chart(count_ratings)
        # Show plot
        st.pyplot(fig2)


        # Get dates from the database
        dates = collection.distinct('date', {'rating': {'$exists': True}})
        dates = [x for x in dates if x != ""]

        st.header('Ratings Distribution by Date')
        # Manage the selected date using session state
        if 'selected_date' not in st.session_state:
            st.session_state['selected_date'] = None

        if dates:
            st.session_state['selected_date'] = st.selectbox('Select a date', options=dates, index=0)

            # Plot ratings distribution for the selected date
            ratings_2 = list(collection.aggregate([
                # Filter documents based on the given date and check if rating exists
                {'$match': {'date': st.session_state['selected_date'], 'rating': {'$exists': True}}},
                
                # Group by rating and count the occurrences of each rating
                {'$group': {'_id': '$rating', 'count': {'$sum': 1}}}
            ]))
            

            # Convert the result to a dictionary where key is rating and value is the count
            ratings_dict = {item['_id']: item['count'] for item in ratings_2}
            ratings_dict = dict(sorted(ratings_dict.items()))

            if ratings_dict:  # Proceed if there are ratings to show
                ratings_3 = list(ratings_dict.keys())
                counts = list(ratings_dict.values())

                st.subheader(f'Plot for {collection.name} on {st.session_state["selected_date"]}')
                st.write("The movie may have few scraped reviews, so the plot may not be accurate.")

                # Create the horizontal bar plot
                fig_3 = utils.get_horizontal_bar_chart(ratings_3, counts)
                st.pyplot(fig_3)

            else:
                st.write("No ratings data available for the selected date.")




    st.header('Sentiment Analysis')
    # Text input for number of reviews, from 0 to 1000
    n  = st.number_input("Number of recent reviews to analyze", min_value=1, max_value=1000, value=10, step=1)
    n = int(n)

    # Checkbox to display reviews
    if st.checkbox(f'Analize last {n} reviews'):
        data = list(
            collection.find({'rating': {'$exists': True}})
            .sort([('$natural', -1)])
            .limit(n)
        )
        # store the reviews and dates in a list
        result = [x["review_text"] for x in data if "review_text" in x]
        result_date = [x["date"] for x in data if "date" in x]
        # force dataset to the smallest size
        min_size = min(len(result), len(result_date))
        result = result[:min_size]
        result_date = result_date[:min_size]

        # clean the reviews using the sentiment module
        result = [utils.clean_review(str(review)) for review in result]

        # get the sentiment of the reviews
        sentiment_result = [utils.get_sentimet(str(review)) for review in result]
        result = pd.DataFrame({'Review': result, 'Sentiment': sentiment_result})

        st.dataframe(result, width=10000)
        # make a plot with the sentiment of the reviews
        # Assuming result['Sentiment'].value_counts() is available

        sentiment_count = result['Sentiment'].value_counts()
        total = sentiment_count.sum()

        fig_sentiment = utils.get_sentiment_plot(sentiment_count, total)
        st.pyplot(fig_sentiment)
        # add a button to show the sentiment plot
        st.write("Sentiment Over Time still in development. Proceed with caution.")
        if st.button('Show Sentiment Over Time Plot'):
           
            #add result_date to the dataframe
            result['date'] = result_date
            # make a stacked bar plot with the sentiment of the reviews by date
            fig_sov  = utils.get_sov(result)
            st.pyplot(fig)
    
    else:
        st.write("No dates available for the selected movie.")
else:
    st.write("Please enter a movie and click 'Click to change' to see the data.")

# Footer
st.markdown("---")

# Transform footer into two columns
col1, col2 = st.columns(2)
col1.write("Canto Arcona Alexis")
col1.write("Castro Echeverria Samantha")

col2.write("Cumi Llanez Christopher")
col2.write("Fernandez Cruz Juan")
col2.write("Ramayo Cardoso Juliana")
