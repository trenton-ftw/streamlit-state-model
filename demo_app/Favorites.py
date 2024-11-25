import streamlit as st 
from demo_app.models.session import Session

#initial build of state class instance 
session = Session(mode="build")

#header info 
st.header(body="streamlit-state-model Demo App")
st.caption(body="This app demonstrates the statefulness of a StateModel as a middleware to st.session_state in a multipage app.")

if session.is_default():
    st.write("It looks like you haven't selected your favorites yet?? 🤔")
    if st.button(label="Start here 👉",key="start_here",type="primary"):
        st.switch_page(page="pages/1_🍽️_Food.py")     
else: 
    if st.button(label="Reset My Favorites",key="reset_session"):
        session.set_attr_to_default()
        st.rerun()

#display favorites
st.subheader("Your Favorites")
st.json(session.dump())