import mysql.connector
from mysql.connector import Error
import datetime
import dateutil.parser

def connect_mysql(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        if connection.is_connected():
            print('Successful Connection to MySQL')
            return connection
    except Error as e:
        print(f'Error while connecting to MySQL: {e}')
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tweets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        tweet_id BIGINT,
        tweet_created_at DATETIME,
        favorite_count INT,
        retweet_count INT,
        reply_count INT,
        quote_count INT,
        view_count INT,
        tweet_text TEXT
    )
    """)
    print("Table 'tweets' created or already exists")

def insert_tweets(connection, tweets):
    cursor = connection.cursor()
    for tweet in tweets:
        try:
            tweet_created_at = dateutil.parser.parse(tweet['tweetTimestamp'])
        except ValueError:
            print(f"Error parsing timestamp for tweet {tweet['tweetId']}")
            continue

        query = """
        INSERT INTO tweets
        (tweet_id, tweet_created_at, favorite_count, retweet_count, reply_count, quote_count, view_count, tweet_text)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            tweet['tweetId'],
            tweet_created_at,
            tweet['tweetFavoriteCount'],
            tweet['tweetRetweetCount'],
            tweet['tweetReplyCount'],
            tweet['tweetQuoteCount'],
            tweet['tweetViewCount'],
            tweet['tweetText']
        )
        try:
            cursor.execute(query, values)
        except Error as e:
            print(f"Error while inserting tweet {tweet['tweetId']}: {e}")
    
    connection.commit()
    print(f"{cursor.rowcount} tweets inserted in the database")