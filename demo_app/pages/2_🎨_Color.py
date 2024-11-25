import streamlit as st 
from demo_app.models.session import Session

#lazy mode lets you use the 'current' state of the state model
session = Session()

st.title("Favorite Color")

st.color_picker(
    label = "Select your favorite color",
    value = session.favorite_color,
    key = session.get_temp_key_name("favorite_color"),
    help = session.docstrings["favorite_color"],
    on_change = Session.store_value,
    args = ["favorite_color"]
)

if st.button(label="Next 👉",type="primary"):
    st.switch_page(page="pages/3_🔢_Number.py")