import streamlit as st 
from demo_app.models.session import Session

#lazy mode lets you use the 'current' state of the state model
session = Session()

st.title("Favorite Food")

available_foods = {"🍕", "🍣", "🌮", "🍔", "🍦", "🍏", "🍌", "🍇", "🍉", "🍓"}
st.multiselect(
    label = "Select your favorite foods",
    key = "food",
    options = available_foods,
    default = session.favorite_foods,
    key = Session.get_temp_key_name("favorite_foods"),
    help = session.docstrings["favorite_foods"],
    on_change = Session.store_value,
    args = ["favorite_foods"]
)

if st.button(label="Next 👉",type="primary"):
        st.switch_page(page="pages/2_🎨_Color.py")     