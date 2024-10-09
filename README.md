# Letterboxd Film Tracker 🎬

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://letterboxd-film-tracker.streamlit.app/)

A web application for analyzing movie reviews and sentiment from Letterboxd. This tool allows users to scrape reviews, analyze sentiment, and visualize trends in movie reception over time.

## Features ✨

- **Review Scraping**: Scrape up to 500 reviews (5000 with admin privileges) from any movie on Letterboxd
- **Sentiment Analysis**: Analyze the emotional tone of reviews using NLTK
- **Data Visualization**: Interactive charts and graphs showing:
  - Rating distributions
  - Sentiment trends over time
  - Overall movie statistics
  - User engagement patterns
- **Real-time Processing**: All analyses are performed in real-time
- **Movie Information**: Display comprehensive movie details including director, release date, and average rating

## Technologies Used 🛠️

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Database**: [MongoDB Atlas](https://www.mongodb.com/atlas/database)
- **Data Processing**:
  - [Python](https://www.python.org/)
  - [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
  - [NLTK](https://www.nltk.org/)
- **Data Visualization**:
  - [Matplotlib](https://matplotlib.org/)
  - [Plotly](https://plotly.com/)

## Installation & Setup 🚀

1. Clone the repository:
```bash
git clone https://github.com/juanjuanjuanfer/yet_to_be_named.git
cd yet_to_be_named
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Create a `.streamlit/secrets.toml` file with your MongoDB connection string:
```toml
MONGODB_URI = "your_mongodb_connection_string"
```

5. Run the application:
```bash
streamlit run Home.py
```

## Project Structure 📁

```
lbxd/
├── Home.py                  # Main Streamlit application
├── pages/                   # Additional pages
│   ├── Scraper.py           # Movie review scraping page
│   └── Dashboard.py         # Analytics dashboard
├── utils.py                 # Utility functions
├── connection_mongo.py      # Database operations  
├── film.py                  # Film scrpaer
├── user.py                  # User scraper
└── requirements.txt         # Project dependencies
```

## Usage 📖

1. **Home Page**: Introduction to the application and its features
2. **Scraper Page**: 
   - Enter a Letterboxd movie URL or title
   - Select number of reviews to scrape
   - View scraping progress in real-time
3. **Dashboard Page**:
   - Select a movie from the database
   - View various analytics and visualizations
   - Filter data by date range
   - Analyze sentiment distribution

## Related Projects 🔗

- [PyBoxd](https://github.com/juanjuanjuanfer/pyboxd) - Python package for Letterboxd scraping

## Contributors 👥

- Alexis Canto Ancona (2009020@upy.edu.mx)
- Samantha Castro Echeverria (2109028@upy.edu.mx)
- Christopher Cumi Llanes (2109048@upy.edu.mx)
- Juan Fernandez Cruz (2109061@upy.edu.mx)
- Juliana Ramayo Cardoso (2109128@upy.edu.mx)

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- [Letterboxd](https://letterboxd.com/) for providing a platform that inspired this project
- Universidad Politécnica de Yucatán for supporting this academic project
- All contributors and users who have helped improve this tool

## Disclaimer ⚠️

This project is not officially affiliated with Letterboxd. It is an academic project created for educational purposes. Please be mindful of Letterboxd's terms of service when using this tool.
