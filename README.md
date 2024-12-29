# Streamlit State Model

Managing session state in Streamlit can be tedious, especially when repeatedly checking and updating st.session_state. Streamlit State Model offers a clean, class-based approach to this problem. By subclassing our StateModel, you can define what you want to be stored in Streamlit's `session_state` with standard Python in the form of classes and attributes while our tool automatically syncs these with Streamlit's session state—eliminating repetitive code and reducing errors. This completely eliminates the need for you to interact with st.session_state directly. 

## Features

- **Easy Setup:** Use existing or new class definitions to store in `session_state`.
- **Default Values:** Automatically default class-defined values into `session_state` based on the defined defaults in your class.
- **Inline Integration:** Eliminate spaghetti `if` statements for `session_state` interaction and declare your class instance inline with the rest of your code.
- **Persistence:** Maintain class attribute values across page refreshes and switches in multi-page apps.
- **Intellisense Support:** Retain normal docstrings and type intellisense that you normally lose when working with session_state.
- **Docstring Access:** Access attribute docstrings via the `docstrings` dictionary within your app.

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
session = Session() #init in lazy mode
st.write(session.favorite_number) #outputs 1 as set in streamlit_app.py  
""
```  

## Example

Explore our demo Streamlit app in the `/demo_app` directory for an example of integrating `StateModel` into a multi-page app on Streamlit Community Cloud here: [state-model-demo-app](https://state-model-demo-app.streamlit.app/).

We're also working on generating API docs for `StateModel` because it already inclues many helper functions (with more to come) such as:
- `dump()`: View all attribute values.
- Widget interaction helpers: Utilize widgets with `StateModel` following Streamlit's recommended patterns (For more details, refer to the [Streamlit Documentation on Working with Widgets in Multipage Apps](https://docs.streamlit.io/develop/concepts/multipage-apps/widgets)).
- Reset function: Reset all attribute values to their defaults.

## Contributing

If you have an idea for a new feature or have found a bug, please open an issue or submit a pull request. I don't have a formal code of conduct or contribution guidelines yet, but I appreciate respectful and constructive contributions.

## Development

For more details on contributing and the CI/CD process, please refer to the [development documentation](docs/development.md).