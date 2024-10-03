import streamlit as st
st.set_page_config(page_title="Letterboxd Film Tracker", page_icon=":chart_with_upwards_trend:", layout="wide")

# css for the page with background color #1A232C
# pallete :#1A232C #FF8100 #FFFFFF #3EBDF4 #00E153
page_css = """

<style>
[data-testid="stHeader"]{
    background-color: #1A232C;
    color: #FFFFFF;
}

[data-testid="stMainBlockContainer"]{

    background-color: #1A232C;\
    color: #FFFFFF;
    }

[data-testid="stMain"]{

    background-color: #1A232C;\
</style>
"""

st.markdown(page_css, unsafe_allow_html=True)

# Set padding for the page
padding_top = 2
# Set page title and layout

st.title('Letterboxd Film Tracker')