import streamlit as st
st.set_page_config(page_title="Letterboxd Film Tracker", page_icon=":chart_with_upwards_trend:", layout="wide")

# css for the page with background color #1A232C
# pallete :#1A232C #FF8100 #FFFFFF #3EBDF4 #00E153
page_css = """

<style>
[data-testid="stHeader"]{
    background-color: #0E1217;
    color: #FFFFFF;
}

[data-testid="stMainBlockContainer"]{

    background-color: #202830;\
    color: #FFFFFF;
    }
[id="letterboxd-scraper"] {
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
    color: transparent;
    display: inline-block;
}
[data-testid="stMain"]{

    background-color: #202830;\
    }

[data-testid="stSidebarContent"]{
    background-color: #0E1217;\
    color: #FFFFFF;
    }
</style>
"""

st.markdown(page_css, unsafe_allow_html=True)

# Set padding for the page
padding_top = 2
# Set page title and layout

# center and a little to the left


# include image with markdown size half https://a.ltrbxd.com/logos/letterboxd-logo-v-neg-rgb-1000px.png
st.markdown('<img src="https://a.ltrbxd.com/logos/letterboxd-logo-v-neg-rgb.svg" alt="Letterboxd Logo" width="300">', unsafe_allow_html=True)
st.markdown('<style>body{text-align: center;}</style>',unsafe_allow_html=True)

st.markdown('<h4     style="font-size: 3em;background: linear-gradient(        to right,        #FF8100 0%,        #FF8100 30%,        #00E153 35%,        #00E153 65%,        #3EBDF4 70%,        #3EBDF4 100%    );    -webkit-background-clip: text;    -webkit-text-fill-color: transparent;    background-clip: text;    color: transparent;    display: inline-block;">&nbsp;Letterboxd Film Tracker</h1>', unsafe_allow_html=True)

