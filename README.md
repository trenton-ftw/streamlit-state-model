# Streamlit State Model

I love Streamlit, but working with `st.session_state` can be tedious. Coming from an OOP background, I cringe at managing each key in `st.session_state` individually, checking if it exists, and losing intellisense for names and types.

So I made `streamlit-state-model` which offers a base class `StateModel` that you can subclass to push your class' attribute I/O directly into `st.session_state`. This means you define what should exist in `st.session_state` once, and then access those values anywhere in your Streamlit app with the expected statefulness of `st.session_state`.

## Features

- **Persistence:** Class instance storage is pushed to `st.session_state` so class attribute values are retained across page refreshes and switches (in multi-page apps).
- **Easy Setup:** `StateModel` can be used with existing or new class definitions.
- **Default Values:** Define the default state of `st.session_state` with normal class' default annotations and gain the ability to reset them all to defaults with a single function call. 
- **Debugging:** When debugging, you can now see the current values in `st.session_state` by inspecting your class' attribute values.
- **Intellisense Support:** Retain normal docstrings and type intellisense that you normally lose when working with `st.session_state`.
- **Inline Integration:** Declare your class instance inline with the rest of your code and eliminate spaghetti `if` checks around current state of `st.session_state`.
- **Docstring Access:** Retrieve attribute docstrings via the `docstrings` dictionary within your app.

## Getting Started

Install the package using pip:

```bash
pip install streamlit-state-model
```  

Take your existing class and subclass `StateModel`:
```python
import streamlit_state_model as ssm 

class Session(ssm.StateModel):
    favorite_color: str = "#252D3D"
    "The user's favorite color as a hex string."
    favorite_number: int = 0
    "The user's favorite number."
```
  
At the entry point of your app, initialize your class in "build" mode.
```python 
# streamlit_app.py
session = Session(mode="build")
st.write(session.favorite_number)  # outputs default value of 0
session.favorite_number = 1  # set to a new value 
```
Anywhere else in your app you can initialize in lazy (default) mode to access current values:
```python
# pages/page_1.py
session = Session() # init in lazy mode
st.write(session.favorite_number) # outputs 1 as set in streamlit_app.py  
""
```  

## Example

Explore our demo Streamlit app in the `/demo_app` directory for an example of integrating `StateModel` into a multipage app on Streamlit Community Cloud. Check out: [state-model-demo-app](https://state-model-demo-app.streamlit.app/).

We're also working on generating API docs for `StateModel` since it already includes many helper functions such as:
- `dump()`: Dump all class attribute values to a JSON string (often paired with `st.json`).
- Widget interaction helpers: Utilize widgets with `StateModel` following Streamlit's recommended patterns. (See the [Streamlit Documentation on Multipage Apps](https://docs.streamlit.io/develop/concepts/multipage-apps/widgets) for details.)
- Reset function: Reset all attribute values to their defaults.

## Development

For details on contributing and the CI/CD process, please refer to the [development documentation](docs/development.md).