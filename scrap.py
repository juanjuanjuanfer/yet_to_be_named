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
USERNAME = '...'
EMAIL = '...'
PASSWORD = '...'
# CHANGE QUERY TO WHATEVER YOU WANT
QUERY = "taylor swift"
# CHANGE INCREMENT_COUNT TO WHATEVER YOU WANT, MAX 20!!!
INCREMENT_COUNT = 20
# CHANGE SLEEPTIME TO WHATEVER YOU WANT, THAT IS THE UPDATE TIME OF THE SCRAP
WAITTIME = 5

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
                f.write(str('{\n'+
                        f'"tweetId": "{tweet.id}",\n'+
                        f'"tweetTimestamp": "{tweet.created_at}",\n'+
                        f'"tweetFavoriteCount": "{tweet.favorite_count}",\n'+
                        f'"tweetRetweetCount": "{tweet.retweet_count}",\n'+
                        f'"tweetReplyCount": "{tweet.reply_count}",\n'+
                        f'"tweetQuoteCount": "{tweet.quote_count}",\n'+
                        f'"tweetViewCount": "{tweet.view_count}",\n'+
                        f'"tweetText": "{tweet.text}",\n'+
                        '},\n'))
        tweets = await tweets.next()
        scraped += 20

        # THIS PRINT IS FOR TESTING PURPOSES
        #[print(tweet.id) for tweet in tweets]
        

asyncio.run(main())