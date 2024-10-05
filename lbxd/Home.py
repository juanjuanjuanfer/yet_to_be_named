import streamlit as st
import pandas as pd

st.set_page_config(page_title="Letterboxd Film Tracker", page_icon=":chart_with_upwards_trend:", layout="wide")

# Custom CSS with your existing color palette
page_css = """
<style>
[data-testid="stHeader"] {
    background-color: #0E1217;
    color: #FFFFFF;
}

[data-testid="stMainBlockContainer"] {
    background-color: #202830;
    color: #FFFFFF;
}

[data-testid="stMain"] {
    background-color: #202830;
}

[data-testid="stSidebarContent"] {
    background-color: #0E1217;
    color: #FFFFFF;
}

.gradient-text {
    background: linear-gradient(
        to right,
        #FF8100 0%,
        #FF8100 30%,
        #00E153 35%,
        #00E153 65%,
        #3EBDF4 70%,
        #3EBDF4 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stat-card {
    background-color: #1A232C;
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
}

.action-button {
    background-color: #FF8100;
    border: none;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    margin: 5px;
}
</style>
"""

st.markdown(page_css, unsafe_allow_html=True)

# Logo and Title
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("https://a.ltrbxd.com/logos/letterboxd-logo-v-neg-rgb.svg", width=300)
    st.markdown('<h1 class="gradient-text">Letterboxd Film Tracker</h1>', unsafe_allow_html=True)

# Welcome message
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h3>Welcome to your personal movie journey! Track, discover, and share your cinematic experiences.</h3>
    </div>
""", unsafe_allow_html=True)

# Movie Stats Section
st.markdown("## 📊 Your Movie Stats")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Movies Watched", value="127", delta="3 this week")
with col2:
    st.metric(label="Movies This Month", value="12", delta="2 more than last month")
with col3:
    st.metric(label="Average Rating", value="4.2 ⭐", delta="↑ 0.2")
with col4:
    st.metric(label="Most Watched Genre", value="Drama", delta="Action close second")

# Quick Actions Section
st.markdown("## 🎯 Quick Actions")
col1, col2 = st.columns(2)
with col1:
    st.button("🎬 Log a Movie", use_container_width=True)
    st.button("📝 Write a Review", use_container_width=True)
with col2:
    st.button("➕ Add to Watchlist", use_container_width=True)
    st.button("🎲 Get Recommendations", use_container_width=True)

# Movie Mood Selector
st.markdown("## 🎭 Your Movie Mood Today")
moods = st.columns(5)
with moods[0]:
    st.button("😊 Feel-good", use_container_width=True)
with moods[1]:
    st.button("🎭 Drama", use_container_width=True)
with moods[2]:
    st.button("🚀 Action", use_container_width=True)
with moods[3]:
    st.button("🤣 Comedy", use_container_width=True)
with moods[4]:
    st.button("👻 Horror", use_container_width=True)

# Recent Activity and Stats
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Recent Activity")
    # Example data for charts
    import numpy as np
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Movies Watched', 'Reviews Written', 'Ratings Given']
    )
    st.line_chart(chart_data)

with col2:
    st.markdown("### 🏆 Watching Challenge")
    st.progress(65)
    st.caption("65/100 movies watched this year")

# Random Movie Feature
st.markdown("### 🎲 Movie of the Day")
movie_col1, movie_col2 = st.columns([1, 3])
with movie_col1:
    st.image("https://via.placeholder.com/150x225", caption="Movie Poster")
with movie_col2:
    st.markdown("#### The Godfather (1972)")
    st.markdown("⭐ 4.5/5 average rating")
    st.markdown("🎬 Crime, Drama | 175 min")
    st.button("Add to Watchlist", key="movie_of_day")

# Footer Stats
st.markdown("---")
footer_cols = st.columns(3)
with footer_cols[0]:
    st.markdown("### 📅 This Month")
    st.metric(label="Watch Time", value="48 hours")
with footer_cols[1]:
    st.markdown("### 🎯 Goal Progress")
    st.metric(label="Year Goal", value="65%", delta="On Track")
with footer_cols[2]:
    st.markdown("### 🌟 Achievement")
    st.metric(label="Review Streak", value="7 days")