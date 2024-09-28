import re

def clean_tweet(text):
    # Delete URLs
    text = re.sub(r'https\S+|www\.\S+','', text)
    # Delete mentions (@user)
    text = re.sub(r'@\w+','', text)
    # Delete hashtags
    text = re.sub(r'#\w+','', text)
    # Delete special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Delete extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text