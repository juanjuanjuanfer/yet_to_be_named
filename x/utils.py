from connection_mongo import connect_to_mongo
import asyncio
from twikit import Client
import time



def insert_tweets(data:dict, database:str, collection:str, mongoUsername:str, mongoPassword:str) -> None:

    client = connect_to_mongo(mongoUsername, mongoPassword)

    db = client[database]

    collection = db[collection]

    if collection.find_one({"tweetId": data["tweetId"]}):

        print(f"Tweet {data['tweetId']} already in the collection")

    else:

        collection.insert_one(data)

        print(f"Tweet {data['tweetId']} inserted")


async def scrape_data(username:str, email:str, password:str, mongoUsername:str, mongoPassword:str, database:str, collection:str, query:str, amount:int=60, type_:str="Latest", increment:int=20, wait_time:int=0.5) -> None:
    client = Client('en-US')
    
    await client.login(
        auth_info_1=username,
        auth_info_2=email,
        password=password
    )

    tweets = await client.search_tweet(query=query, product=type_, count=increment)


    scraped = increment

    while scraped < amount:

        print(f"Scraped {scraped} tweets")
        
        
        for tweet in tweets:
            tweet_data = {
                "tweetUser": tweet.user.id,
                "tweetUserFollowers": tweet.user.followers_count,
                "tweetUserWithheldCountries": tweet.user.withheld_in_countries,
                "tweetId": tweet.id,
                "tweetHashtags": tweet.hashtags,
                "tweetTimestamp": tweet.created_at,
                "tweetFavoriteCount": tweet.favorite_count,
                "tweetRetweetCount": tweet.retweet_count,
                "tweetReplyCount": tweet.reply_count,
                "tweetQuoteCount": tweet.quote_count,
                "tweetViewCount": tweet.view_count,
                "tweetText": tweet.text
            }
            insert_tweets(data = tweet_data, database = database, collection=collection, mongoUsername=mongoUsername, mongoPassword=mongoPassword)  

   
        tweets = await tweets.next()
        scraped += increment
        time.sleep(wait_time)

    return

def get_data_from_mongo(mongoUsername:str, mongoPassword:str, mongoDB:str, mongoCollection:str, amount:int=20) -> list:
    client = connect_to_mongo(mongoUsername, mongoPassword)

    db = client[mongoDB]

    collection = db[mongoCollection]

    data = list(collection.find().sort([('$natural', -1)]).limit(amount))
    result = []
    for x in data:
        # get only "tweetId" "tweetTimestamp" and "tweetText"
        result.append({"tweetId": x["tweetId"], "tweetTimestamp": x["tweetTimestamp"], "tweetText": x["tweetText"]})


    return result