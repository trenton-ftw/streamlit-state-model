import streamlit as st 
from demo_app.models.session import Session

#lazy mode lets you use the 'current' state of the state model
session = Session()

st.title("Favorite Number")

st.number_input(
    label = "Select your favorite number",
    key = Session.get_temp_key_name("favorite_number"),
    value = session.favorite_number,
    help = session.docstrings["favorite_number"],
    on_change = Session.store_value,
    args = ["favorite_number"]
)

if st.button(label="Back to home 👉",type="primary"):
    st.switch_page(page="Favorites.py")