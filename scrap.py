# THE CODE GENERATES A JSON FILE BUT THE STRUCTURE IS WRONG, MUST BE MANUALLY FIXED
# ALSO THE CODE MAY NOT WORK, IF YOU GET THE ERROR COMMENT TO ME (JUAN) AND I WILL TELL YOU HOW TO FIX IT
# THE ERROR ABOVE IS THIS: BadRequest: status: 400, message: "{"errors":[{"code":366,"message":"flow name LoginFlow is currently not accessible"}]}"
# DO NOT UPLOAD THE CREDENTIALS TO GITHUB
# THE CODE IS NOT OPTIMIZED, I DONT KNOW HOW WOULD THE WHILE TRUE WORK WHEN IT GETS TOO MANY TWEETS
# THE CODE IS NOT OPTIMIZED, I DONT KNOW HOW WOULD THE WHILE TRUE WORK WHEN IT GETS TOO MANY TWEETS
# THE CODE IS NOT OPTIMIZED, I DONT KNOW HOW WOULD THE WHILE TRUE WORK WHEN IT GETS TOO MANY TWEETS

import asyncio
# python -m pip install twikit
# python -m pip uninstall --y twikit
# python -m pip install https://github.com/d60/twikit/archive/login_fix.zip
from twikit import Client
import time

# constants
USERNAME = ''
EMAIL = ''
PASSWORD = ''
# CHANGE QUERY TO WHATEVER YOU WANT
QUERY = "amlo"
# CHANGE INCREMENT_COUNT TO WHATEVER YOU WANT, MAX 20!!!
INCREMENT_COUNT = 20
# CHANGE SLEEPTIME TO WHATEVER YOU WANT, THAT IS THE UPDATE TIME OF THE SCRAP
WAITTIME = 0.3

# IDK IF THERE ARE OTHER CLIENTS THIS WORKS
client = Client('en-US')





# structure to keep the code running to prevent many logins, just kill with ctrl+c
async def main():
    # idk what await means but necessary
    await client.login(
        auth_info_1=USERNAME ,
        auth_info_2=EMAIL,
        password=PASSWORD
    )
    
    # unnecessary prints 
    print('Logged in')
    print('Searching for tweets...')

    # search for FIRST tweets, NECESSARY TO BE OUTSIDE LOOP also await necessary, set count to whatever you want
    # default is 20, also max is 20
    tweets =  await client.search_tweet(query=QUERY, product='Latest', count=INCREMENT_COUNT)
    
    # THIS PRINT IS FOR TESTING PURPOSES
    #[print(tweet.id) for tweet in tweets]
    
    scraped = 20
    # LOOP TO KEEP SEARCHING FOR TWEETS, CHANGE THE SLEEP TIME TO WHATEVER YOU WANT
    while True:
        print(f"Scraped {scraped} tweets")
        time.sleep(WAITTIME)
        with open(f'{QUERY}_tweets.json', 'a',encoding="UTF-8") as f:
            for tweet in tweets:
                f.write(str({
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
            "tweetText": tweet.text,
            "tweetLocation" : tweet.place
        })+"\n")
        tweets = await tweets.next()
        scraped += 20

        # THIS PRINT IS FOR TESTING PURPOSES
        #[print(tweet.id) for tweet in tweets]
        

asyncio.run(main())