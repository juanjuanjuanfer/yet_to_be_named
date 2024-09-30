from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import utils
from flask_session import Session
import asyncio
import threading

MONGOUSERNAME = ""
MONGOPASSWORD = ""
MONGODB = "x_app"

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

scrape_status = {}


def background_scrape(user_id, username, email, password, mongoUsername, mongoPassword, database, collection, query, amount, type_, increment):
    scrape_status[user_id] = 'in progress'
    
    # Call the async scrape_data function
    asyncio.run(
        utils.scrape_data(username=username, email=email, password=password, mongoUsername=mongoUsername, mongoPassword=mongoPassword, 
                          database=database, collection=collection, query=query, amount=amount, type_=type_, increment=increment)
    )
    
    # Update status when finished
    scrape_status[user_id] = 'finished'

@app.route('/scrape_status')
def scrape_status_check():
    user_id = session.get('user_id')
    
    # Return the current status of the scrape task for this user
    status = scrape_status.get(user_id)
    
    return jsonify({'status': status})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        # Your scraping logic here
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        query = request.form['query']
        type_ = request.form['type']
        amount = int(request.form['amount'])
        increment = int(request.form['increment'])
        collection = request.form['collection']
        user_id = session.get('user_id', username)  # Using username for simplicity
        scrape_thread = threading.Thread(target=background_scrape, args=(user_id, username, email, password, MONGOUSERNAME, MONGOPASSWORD, MONGODB, collection, query, amount, type_, increment))
        scrape_thread.start()

        # Redirect to the waiting page
        return redirect(url_for('status'))

    # For GET request, show the form
    return render_template('scrape.html')
    
@app.route('/status')
def status():
    user_id = session.get('user_id')
    
    # Render a template that polls for status
    return render_template('status.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    data = "None"  # Initialize data as None
    if request.method == 'POST':
        # Get the collection name from the form
        mongoCollection = request.form['collection']
        # Fetch data from MongoDB
        data = utils.get_data_from_mongo(MONGOUSERNAME, MONGOPASSWORD, MONGODB, mongoCollection=mongoCollection, amount=20)
    return render_template('dashboard.html', data=data)

    
if __name__ == '__main__':
    app.run(debug=True)