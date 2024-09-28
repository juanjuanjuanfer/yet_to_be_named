from json_reader import read_json
from tweet_cleaner import clean_tweet
from mysql_handler import connect_mysql, create_table, insert_tweets
from config import CONFIG

def main():
    tweets = read_json(CONFIG['json_file'])
    
    # Clean tweets
    for tweet in tweets:
        tweet['tweetText'] = clean_tweet(tweet['tweetText'])

    connection = connect_mysql(CONFIG['host'], CONFIG['user'], CONFIG['password'], CONFIG['database'])

    if connection:
        create_table(connection)
        insert_tweets(connection, tweets)
        connection.close()
        print('Connection closed')

if __name__ == '__main__':
    main()