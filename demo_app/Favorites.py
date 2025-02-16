import streamlit as st 
from models.session import Session

#initial build of state class instance 
session = Session(mode="build")

#header info 
col1,col2 = st.columns([4,1])
with col1: 
    st.header(body="streamlit-state-model Demo App")
with col2: 
    st.link_button(label="📄 GitHub",url="https://github.com/trenton-ftw/streamlit-state-model")
st.markdown(body="This app demonstrates the statefulness of a `StateModel`, a base class provided by `streamlit-state-model` that you can subclass to push your class' attribute I/O directly into `st.session_state`")

if session.is_default():
    st.markdown("**See the demo in action by selecting your favorites below!**")
    if st.button(label="Start here 👉",key="start_here",type="primary"):
        st.switch_page(page="pages/1_🍽️_Food.py")     
else: 
    if st.button(label="Reset My Favorites",key="reset_session"):
        session.set_attr_to_default()
        st.rerun()
    st.markdown("As you can see, your selections that are stored within the class that subclassed `StateModel` are retained across page refreshes because they were stored in `st.session_state` automatically.")
    st.json(session.dump())

st.write("Example class subclassing StateModel")
st.code("""class Session(ssm.StateModel):
    favorite_color: str = "#252D3D"
    "The user's favorite color as a hex string."
    favorite_number: int = 0
    "The user's favorite number."
    favorite_foods: List[str] = ssm.DefaultFactory(lambda: ["🍕", "🍣", "🌮"])
    "A list of the user's favorite foods as emoji strings. Users can select as many as they like (from the available options)."
""",language="python")
 