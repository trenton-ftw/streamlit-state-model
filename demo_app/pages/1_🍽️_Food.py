import streamlit as st 
from models.session import Session

#lazy mode lets you use the 'current' state of the state model
session = Session()

st.title("Favorite Food")

available_foods = {"🍕", "🍣", "🌮", "🍔", "🍦", "🍏", "🍌", "🍇", "🍉", "🍓"}
st.multiselect(
    label = "Select your favorite foods",
    options = available_foods,
    default = session.favorite_foods,
    key = session.get_widget_key_name("favorite_foods"),
    help = session.docstrings["favorite_foods"],
    on_change = session.sync_from_widget_key,
    args = ["favorite_foods"]
)

if st.button(label="Next 👉",type="primary"):
        st.switch_page(page="pages/2_🎨_Color.py")