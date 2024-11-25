# Streamlit State Model

I love Streamlit apps, but I might lose it if I have to write `if key not in st.session_state` one more time. So I made this package which provides a `StateModel` for you to subclass in your python class definition. This forwards your class instance's attribute storage/retrieval to session_state with no extra work. This allows you to interact with `session_state` without having to directly touch it within your code. 

## Feautures 

- **Easy to Setup.** Use your existing class definitions or define whatever you need to store in `session_state` as a class definition. 
- **Can sit inline with the rest of your app code.** Get rid of the spaghetti `if` statements in your app code to interact with `session_state`. 
- **Default values defined in your class are defaulted into `session_state`**  
- **Makes your class instance consistently available across all pages in multi-page app.** With `StateModel`, your class' attribute storage is now backed directly by `session_state`, so all attribute values of your class will persist across page refreshes or page switches that you might find in a multi-page app.
- **Keep intellisense working while working with `session_state`.** Your defined docstrings and type intellisense will continue to work as normal with a `StateModel` even though you are storing it in `session_state` (which you typically lose when working with `session_state`). 
- **Use attribute docstrings within your app.** Your `StateModel`'s attribute docstrings are parsed and made available to you in the `docstrings` dict keyed by its attribute name.

## Getting Started

Install the package using pip:

```bash
pip install streamlit-state-model
```  
Just take your existing class definition and subclass `StateModel`. 
```python
import streamlit_state_model as ssm 

class Session(ssm.StateModel):
    favorite_color: str = "#252D3D"
    "The user's favorite color as a hex string."
    favorite_number: int = 0
    "The user's favorite number."
```
  
At the entry point to your app, init an instance of your class definition in "build" mode.
```python 
#streamlit_app.py
session = Session(mode="build")
st.write(session.favorite_number) #outputs default value of 0
session.favorite_number = 1 #set to a new value 
""
```
Anywhere else in your app you can init an instance of your `StateModel` using lazy (default) mode. `StateModel` is a singleton like storage of your class instance, so when you init an instance of your class after building it, it does nothing except provide the class interface to your python code for accessing your class' attribute values. 
```python
#pages/page_1.py
session = Session() #init in lazy modey
st.write(session.favorite_number) #outputs 1 as set in streamlit_app.py  
""
```


## Example 
Check out our demo Streamlit app within this repo at `/demo_app` for an example (coming to Streamlit Community soon) of integrating `StateModel` into a simple multi-page app. 

Also working on generating API docs for `StateModel` as it also provides many other commonly needed helper functions for your class. Provides a `dump()` function to make it easy to view all attribute values, functions to help utilize widets to interact with your `StateModel` (following the 'Option 2: Save your widget values into a dummy key in Session State' pattern defined by Streamlit [Streamlit Documentation | Working with widgets in multipage apps](https://docs.streamlit.io/develop/concepts/multipage-apps/widgets)), a function to reset all attribute values to their defaults, and many others!