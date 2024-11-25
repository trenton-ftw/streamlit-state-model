import pytest
from streamlit.testing.v1 import AppTest

#NOTE: the demo at itself is used to perform these tests. altering the demo at would require test updates 

#NOTE: The StateModel instance itself is not made available within the at framework per se, just the values inside the 
#_state_model st.session_state key. So all tests need to reference StateModel's attribute keys in session_state instead of 
#trying to interact with the class instance directly, the class instance wrapper of StateModel is only available in 
#at runtime 

@pytest.fixture(scope="function",autouse=True)
def demo_streamlit_app():
    "Run our demo at and provide the running at to the test."
    at = AppTest.from_file("demo_app/Favorites.py")
    at.run()  
    yield at

def test_Session_init_BuildMode_AttributesSetToDefault(demo_streamlit_app):
    at = demo_streamlit_app
    assert at.session_state["_state_model"]["Session"]["favorite_color"] == "#252D3D"
    assert at.session_state["_state_model"]["Session"]["favorite_number"] == 0
    assert at.session_state["_state_model"]["Session"]["favorite_foods"] == ["🍕", "🍣", "🌮"]

def test_Session_init_BuildMode_DocstringsSet(demo_streamlit_app):
    at = demo_streamlit_app
    assert at.session_state["_state_model"]["Session"]["_docstrings"]["favorite_color"] == "The user's favorite color as a hex string."
    assert at.session_state["_state_model"]["Session"]["_docstrings"]["favorite_number"] == "The user's favorite number."
    assert at.session_state["_state_model"]["Session"]["_docstrings"]["favorite_foods"] == """A list of the user's favorite foods as emoji strings.\n    \n    Users can select as many as they like (from the available options)."""

def test_Session_isdefault_Defaults_DefaultsDetected(demo_streamlit_app): 
    at = demo_streamlit_app
    #the start_here button should be displayed because the session has default values 
    assert at.button(key="start_here")
    with pytest.raises(KeyError):
        at.button(key="reset_session")

def test_Session_isdefault_ChangeFavoriteNumber_DefaultsNotDetected(demo_streamlit_app): 
    at = demo_streamlit_app
    at.session_state["_state_model"]["Session"]["favorite_number"] = 5
    at.run() 
    #the start_here button should not be displayed because the session has a modified value
    with pytest.raises(KeyError):
        assert at.button(key="start_here")
    assert at.button(key="reset_session")