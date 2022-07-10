import home
import model
import lstm
import streamlit as st
from PIL import Image

# A dictionary that maps the name of the page to the page itself.
PAGES = {
    "Home": home,
    "Prophet Model": model, 
    "LSTM Model": lstm
}
st.set_page_config(layout="wide")

with st.sidebar.expander("Objetive"):
    st.write("""
    The aim of this project is to use different tools to find the best approach for predicting global temperature change.
    """)
with st.sidebar.expander("Page description"):
    st.write("""
    - **Home**: You can find a descriptive analysis of the data used for the model. 

        You will also find more detailed information by country and year of the temperature increases.

    - **Prophet Model**: The Prophet model, as well as its main results and conclusions.


    - **LSTM Model**: The LSTM model
    """)
# Creating a title for the sidebar.

# Creating a radio button in the sidebar that allows the user to select which page they want to go to.
selection = st.sidebar.radio("Go to", list(PAGES.keys()))


# Assigning the value of the key `selection` to the variable `page`.
page = PAGES[selection]

# Calling the `app()` function from the `page` variable.
page.app()
