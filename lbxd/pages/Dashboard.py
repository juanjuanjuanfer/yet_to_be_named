import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import connection_mongo
import film as scraper

# Establish MongoDB connection
client = connection_mongo.connect_to_mongo("-", "-")
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

    
    image_url = film_poster  # Replace with your image URL
    st.markdown(
        f'<div style="text-align:center;"><img src="{image_url}" alt="Movie Image" width="300"></div>',
        unsafe_allow_html=True
    )
    # Text input for number of reviews
    n = st.text_input("Number of recent reviews to show", "10")
    n = int(n)

    # Checkbox to display reviews
    if st.checkbox(f'Show last {n} reviews'):
        data = list(
            collection.find({'rating': {'$exists': True}})
            .sort([('$natural', -1)])
            .limit(n)
        )
        result  = []
        for x in data:
            result.append([x["username"], x["rating"], x["review_text"], x["date"]])
        st.dataframe(result)

    # Get dates from the database
    dates = collection.distinct('date', {'rating': {'$exists': True}})
    dates = [x for x in dates if x != ""]

    # Manage the selected date using session state
    if 'selected_date' not in st.session_state:
        st.session_state['selected_date'] = None

    if dates:
        st.session_state['selected_date'] = st.selectbox('Select a date', options=dates, index=0)

        # Plot ratings distribution for the selected date
        ratings = list(collection.aggregate([
            # Filter documents based on the given date and check if rating exists
            {'$match': {'date': st.session_state['selected_date'], 'rating': {'$exists': True}}},
            
            # Group by rating and count the occurrences of each rating
            {'$group': {'_id': '$rating', 'count': {'$sum': 1}}}
        ]))

        # Convert the result to a dictionary where key is rating and value is the count
        ratings_dict = {item['_id']: item['count'] for item in ratings}
        ratings_dict = dict(sorted(ratings_dict.items()))

        if ratings_dict:  # Proceed if there are ratings to show
            ratings = list(ratings_dict.keys())
            counts = list(ratings_dict.values())

            # Create the horizontal bar plot
            st.subheader(f'Plot for {collection.name} on {st.session_state["selected_date"]}')
            st.write("The movie may have few scraped reviews, so the plot may not be accurate.")
            fig, ax = plt.subplots()  # Create a figure and axis
            ax.barh(ratings, counts)  # Create horizontal bar chart

            # Add labels and title
            ax.set_xlabel('Count')
            ax.set_ylabel('Rating')
            ax.set_title('Ratings Distribution')

            # Display the plot in Streamlit
            st.pyplot(fig)
        else:
            st.write("No ratings data available for the selected date.")
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
