import film as scraper
import connection_mongo as mongo
import time

client= mongo.connect_to_mongo("", "")
db = client.get_database("Letterboxd")
collection = db["reviews_the-substance"]

while True:
    print("Scraping reviews...")
    movie = scraper.Film()
    movie.set_film_name("the-substance")

    reviews = scraper.Film.FilmReview(movie.filmName)
    reviews.get_film_reviews(1)
    data = reviews.filmReviews


    for review in data:
        # insert if 'review_id' not in collection
        if not collection.find_one({"review_id": review['review_id']}):
            collection.insert_one(review)
            print(f"Review with ID {review['review_id']} inserted into the database.")
        else:
            print(f"Review with ID {review['review_id']} already exists in the database.")
    
    print("Waiting for 30 seconds before the next iteration...")
    time.sleep(1)