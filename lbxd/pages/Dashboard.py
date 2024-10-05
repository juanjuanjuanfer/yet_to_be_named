import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import connection_mongo
import film as scraper
import sentiment
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px


# Establish MongoDB connection
client = connection_mongo.connect_to_mongo("juan", "lokura22")
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
    film_rating = sum([key * value for key, value in enumerate(film_rating.values(), start=1)]) / sum(film_rating.values()) * 10
    film_rating = film_rating.__round__(0)

    image_url = film_poster  # Replace with your image URL
    st.markdown(
        f'<div style="text-align:center;"><img src="{image_url}" alt="Movie Image" width="300"></div>',
        unsafe_allow_html=True
    )
    fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = film_rating,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Rating"},
    gauge = {'axis': {'range': [None, 100]},
             'steps': [{'range': [0, 100], 'color': "#202830"}],
             'bar' : {'color': "#00E054"},
             'bgcolor': "#202830"
             },
    
    ))
    fig.update_layout(paper_bgcolor="#202830", font={'color': "white"})
    st.plotly_chart(fig)

    


    
    data = list(collection.find({'rating': {'$exists': True}}))


    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['text.color'] = 'white'  # Set default text color to white

    # Sample dataset from MongoDB
    # data = list(collection.find({'rating': {'$exists': True}}))

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
        
        # Set up the plot
        fig, ax = plt.subplots()
        
        # Create a vertical bar chart
        ax.bar(count_ratings.index, count_ratings.values, color='#00E054', width=0.75)
        # Set grid lines, but only for the y-axis (horizontal lines)
        ax.grid(True, axis='y', color='gray', linestyle='--', linewidth=0.7)
        ax.grid(True, axis='x', color='gray', linestyle='--', linewidth=0.7, alpha=0)


        # Customize labels and title with white text color
        ax.set_xlabel('Rating', fontsize=12, color='white')
        ax.set_ylabel('Count', fontsize=12, color='white')
        ax.set_title(f'Ratings', fontsize=15, color='white')
        
        # Change background color to #202830
        fig.patch.set_facecolor('#202830')  # Figure background
        ax.set_facecolor('#202830')         # Axes background
        
        # Set the ticks to white color
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        # Remove the black borders (spines)
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        # Show plot
        st.pyplot(fig)
        # make title "Sentiment Analysis"

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
                fig, ax = plt.subplots()

                # Create horizontal bar chart
                ax.barh(ratings, counts, color='#00E054')  # Set bar color to the desired green
                # eliminate grid
                ax.grid(True, axis='y', color='gray', linestyle='--', linewidth=0.7, alpha=0)
                ax.grid(True, axis='x', color='gray', linestyle='--', linewidth=0.7)

                # Add labels and title with white text color
                ax.set_xlabel('Count', color='white')
                ax.set_ylabel('Rating', color='white')
                ax.set_title('Ratings Distribution', color='white')

                # Change the background color to #202830
                fig.patch.set_facecolor('#202830')  # Set figure background
                ax.set_facecolor('#202830')         # Set axis background
                # Set grid lines, but only for the x-axis (vertical lines)

                # Set the ticks to white color
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')

                # Remove the black borders (spines)
                for spine in ax.spines.values():
                    spine.set_visible(False)

                # Display the plot in Streamlit
                st.pyplot(fig)
            else:
                st.write("No ratings data available for the selected date.")




    st.header('Sentiment Analysis')
    # Text input for number of reviews
    n = st.text_input("Number of recent reviews to analize", "10")
    n = int(n)

    # Checkbox to display reviews
    if st.checkbox(f'Analize last {n} reviews'):
        data = list(
            collection.find({'rating': {'$exists': True}})
            .sort([('$natural', -1)])
            .limit(n)
        )
        result  = [x["review_text"] for x in data]

        # clean the reviews using the sentiment module
        result = [sentiment.clean_review(str(review)) for review in result]

        # get the sentiment of the reviews
        sentiment_result = [sentiment.get_sentimet(str(review)) for review in result]
        result = pd.DataFrame({'Review': result, 'Sentiment': sentiment_result})

        st.dataframe(result)
        # make a plot with the sentiment of the reviews
        # Assuming result['Sentiment'].value_counts() is available

        sentiment_count = result['Sentiment'].value_counts()
        total = sentiment_count.sum()

        # Custom color palette for sentiment categories
        custom_colors = {'Positive': '#00E054', 'Negative': '#FF8000', 'Neutral': '#40BCF4'}

        # Create a figure and axis object with dark background
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#202830')  # Set figure background to dark
        ax.set_facecolor('#202830')         # Set axes background to dark

        # Use matplotlib's bar chart instead of seaborn
        ax.bar(sentiment_count.index, sentiment_count.values, color=[custom_colors[x] for x in sentiment_count.index])

        # Customize the labels and title with white text
        ax.set_xlabel('Sentiment', fontsize=12, labelpad=10, color='white')
        ax.set_ylabel('Count', fontsize=12, labelpad=10, color='white')
        ax.set_title('Sentiment Distribution', fontsize=15, pad=15, color='white')

        # Add percentages to the bars
        for i, (sentiment, val) in enumerate(sentiment_count.items()):
            percentage = f'{(val / total) * 100:.1f}%'  # Calculate percentage
            ax.text(i, val + 1, percentage, ha='center', va='bottom', fontsize=12, color='white')  # Set color to white

        # Rotate x-axis labels (optional)
        ax.set_xticklabels(sentiment_count.index, rotation=0, ha='center', fontsize=11, color='white')

        # Set tick parameters to white
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Remove the black borders (spines)
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Set horizontal grid lines only (remove vertical grid lines)
        ax.grid(True, axis='y', color='gray', linestyle='--', linewidth=0.7)

        # Display the plot in Streamlit
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
