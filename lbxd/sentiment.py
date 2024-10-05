import connection_mongo
import re
#import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

def get_reviews(collection: str, username:str, password:str):
    client = connection_mongo.connect_to_mongo(username, password)
    db = client["Letterboxd"]
    collection = db[collection]
    #get reviews from the collection and store them in a list
    reviews = list(collection.find())
    cleaned_reviews = [clean_review(review["review_text"]) for review in reviews if "review_text" in review]
    
    sentiments = [get_sentimet(review) for review in cleaned_reviews]
    # make df with reviews["review_text"] [sentiment] ["rating"]
    df = pd.DataFrame({"review": cleaned_reviews, "sentiment": sentiments})
  
    return df

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

username = "juan"
password = "lokura22"
collection = "the-substance"
result =get_reviews(collection, username, password)
