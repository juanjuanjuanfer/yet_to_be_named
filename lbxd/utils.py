import connection_mongo
import plotly.graph_objects 
import matplotlib.pyplot as plt
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import download

def login():
    try:
        #use .streamlit/secrets.toml to store credentials
        with open(".streamlit/secrets.toml", "r") as f:
            contents = f.read()
            username = re.search(r'username = "(.*)"', contents).group(1)
            password = re.search(r'password = "(.*)"', contents).group(1)
    except:
        return "Error: Could not read credentials file or file does not exist."
    
    return connection_mongo.connect_to_mongo(username, password)

def get_gauge_plot(score:int, range_axis:int, title:str="Title") -> plotly.graph_objects.Figure:
    """
    Returns a gauge plot with the given score.

    score: int or float
        The score to be displayed in the gauge plot.
    range_axis: int or float
        The maximum value for the gauge plot.
    title: str, optional
        The title of the gauge plot. Default is "Title".
    """
    fig = plotly.graph_objects.Figure(plotly.graph_objects.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        gauge = {'axis': {'range': [None, range_axis]},
                'steps': [{'range': [0, range_axis], 'color': "#202830"}],
                'bar' : {'color': "#00E054"},
                'bgcolor': "#202830"
                },
        
        ))
    fig.update_layout(paper_bgcolor="#202830", font={'color': "white"})
    return fig

def get_vertical_bar_chart(count_ratings) -> plt.figure:

    fig, ax = plt.subplots()
        
    ax.bar(count_ratings.index, count_ratings.values, color='#00E054', width=0.75)

    ax.grid(True, axis='y', color='gray', linestyle='--', linewidth=0.7)
    ax.grid(True, axis='x', color='gray', linestyle='--', linewidth=0.7, alpha=0)


    ax.set_xlabel('Rating', fontsize=12, color='white')
    ax.set_ylabel('Count', fontsize=12, color='white')
    ax.set_title(f'Ratings', fontsize=15, color='white')
    

    fig.patch.set_facecolor('#202830')  # Figure background
    ax.set_facecolor('#202830')         # Axes background
    

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    

    for spine in ax.spines.values():
        spine.set_visible(False)
        
    return fig

def get_horizontal_bar_chart(ratings_3, counts) -> plt.figure:

    fig, ax = plt.subplots()
    ax.barh(ratings_3, counts, color='#00E054')  # Set bar color to the desired green


    ax.grid(True, axis='y', color='gray', linestyle='--', linewidth=0.7, alpha=0)
    ax.grid(True, axis='x', color='gray', linestyle='--', linewidth=0.7)


    ax.set_xlabel('Count', color='white')
    ax.set_ylabel('Rating', color='white')
    ax.set_title('Ratings Distribution', color='white')


    fig.patch.set_facecolor('#202830')  # Set figure background
    ax.set_facecolor('#202830')         # Set axis background


    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')


    for spine in ax.spines.values():
        spine.set_visible(False)

    return fig

def clean_review(review:str):
    review = re.sub(r'http\S+|@\w+|#\w+', '', review)
    review = review.lower()
    review = re.sub(r'\s+', ' ', review).strip()
    return review

def get_sentimet(review:str):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(review)
    if sentiment["compound"] >= 0.05:
        return "Positive"
    elif sentiment["compound"] <= -0.05:
        return "Negative"
    else:
        return "Neutral"
    return 

def get_sentiment_plot(sentiment_count, total) -> plt.figure:

    custom_colors = {'Positive': '#00E054', 'Negative': '#FF8000', 'Neutral': '#40BCF4'}


    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('#202830')  # Set figure background to dark
    ax.set_facecolor('#202830')         # Set axes background to dark
    ax.grid(True, axis='y', color='white', linestyle='--', linewidth=0.7)

    ax.bar(sentiment_count.index, sentiment_count.values, color=[custom_colors[x] for x in sentiment_count.index])


    ax.set_xlabel('Sentiment', fontsize=12, labelpad=10, color='white')
    ax.set_ylabel('Count', fontsize=12, labelpad=10, color='white')
    ax.set_title('Sentiment Distribution', fontsize=15, pad=15, color='white')


    for i, (sentiment, val) in enumerate(sentiment_count.items()):
        percentage = f'{(val / total) * 100:.1f}%'  # Calculate percentage
        ax.text(i, val + 1, percentage, ha='center', va='bottom', fontsize=12, color='white')  # Set color to white


    ax.set_xticklabels(sentiment_count.index, rotation=0, ha='center', fontsize=11, color='white')


    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')


    for spine in ax.spines.values():
        spine.set_visible(False)




    return fig

def get_sov(result):
    fig, ax = plt.subplots()
    result.groupby(['date', 'Sentiment']).size().unstack().plot(kind='bar', stacked=True, ax=ax)
    return fig

download('vader_lexicon')

