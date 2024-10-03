import film as scraper
import connection_mongo as mongo
import time

client= mongo.connect_to_mongo("-", "-")
db = client.get_database("Letterboxd")
moviename = "beetlejuice-beetlejuice"
collection = db[moviename]

# number of pages to scrape
n = 1

while True:
    print("Scraping reviews...")
    movie = scraper.Film()
    movie.set_film_name(moviename)

    reviews = scraper.Film.FilmReview(movie.filmName)
    reviews.get_film_reviews(n)
    data = reviews.filmReviews


    for review in data:
        # insert if 'review_id' not in collection
        if not collection.find_one({"review_id": review['review_id']}):
            collection.insert_one(review)
            print(f"Review with ID {review['review_id']} inserted into the database.")
        else:
            print(f"Review with ID {review['review_id']} already exists in the database.")
    
    print(f"Waiting for {n} seconds before the next iteration...")
    time.sleep(1)