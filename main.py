import asyncio
from twikit import Client
import json

# Constants (fill with your credentials and parameters)
USERNAME = '...'
EMAIL = '...@gmail.com'
PASSWORD = '...'
QUERY = "amlo"
INCREMENT_COUNT = 20
WAITTIME = 5

# Initialize the Twikit client
client = Client('en-US')

# Producer function to scrape tweets and put them into a queue
async def scrape_tweets(queue):
    await client.login(auth_info_1=USERNAME, auth_info_2=EMAIL, password=PASSWORD)
    print('Logged in')
    print('Searching for tweets...')

    # Initial search
    tweets = await client.search_tweet(query=QUERY, product='Top', count=INCREMENT_COUNT)
    scraped = 20

    while True:
        print(f"Scraped {scraped} tweets")
        # Put each tweet into the queue
        for tweet in tweets:
            await queue.put(tweet)
        # Fetch the next set of tweets
        tweets = await tweets.next()
        scraped += 20
        await asyncio.sleep(WAITTIME)  # Non-blocking sleep

# Consumer function to process tweets from the queue
async def process_tweets(queue):
    while True:
        tweet = await queue.get()  # Wait for a tweet to be available in the queue
        # Process tweet (store or handle in real-time)
        tweet_data = {
            "tweetId": tweet.id,
            "tweetTimestamp": tweet.created_at,
            "tweetFavoriteCount": tweet.favorite_count,
            "tweetRetweetCount": tweet.retweet_count,
            "tweetReplyCount": tweet.reply_count,
            "tweetQuoteCount": tweet.quote_count,
            "tweetViewCount": tweet.view_count,
            "tweetText": tweet.text
        }
        # Append tweet data to JSON file (ensuring proper structure)
        with open(f'{QUERY}_tweets.json', 'a', encoding="UTF-8") as f:
            json.dump(tweet_data, f, ensure_ascii=False)
            f.write(',\n')  # Append a comma for JSON array format
        
        queue.task_done()  # Mark the task as done

# Main function to run the asyncio tasks
async def main():
    queue = asyncio.Queue()  # Initialize the queue
    # Create and run tasks for scraping and processing
    scraping_task = asyncio.create_task(scrape_tweets(queue))
    processing_task = asyncio.create_task(process_tweets(queue))
    await asyncio.gather(scraping_task, processing_task)  # Run both tasks concurrently

# Run the main function with asyncio
asyncio.run(main())
