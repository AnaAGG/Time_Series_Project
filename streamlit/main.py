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

st.sidebar.image("images/portada.png", use_column_width=True)

# Creating a title for the sidebar.
st.sidebar.title('Navigation')

# Creating a radio button in the sidebar that allows the user to select which page they want to go to.
selection = st.sidebar.radio("Go to", list(PAGES.keys()))


# Assigning the value of the key `selection` to the variable `page`.
page = PAGES[selection]

# Calling the `app()` function from the `page` variable.
page.app()
