# Streamlit State Model
Tired of writing repetitive `if key not in st.session_state` checks in your Streamlit apps?  
  
Introducing `StateModel` - a streamlined solution that lets you manage `session_state` effortlessly through standard Python class definitions. With `StateModel`, you can store and retrieve class attributes directly in `session_state` without any extra hassle, making your code cleaner and more maintainable.

## Features

- **Easy Setup:** Use existing or new class definitions to store in `session_state`.
- **Inline Integration:** Eliminate spaghetti `if` statements for `session_state` interaction.
- **Default Values:** Automatically default class-defined values into `session_state`.
- **Persistence:** Maintain class attribute values across page refreshes and switches in multi-page apps.
- **Intellisense Support:** Retain docstrings and type intellisense with `StateModel`.
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

Explore our demo Streamlit app in the `/demo_app` directory for an example of integrating `StateModel` into a multi-page app (coming soon to the Streamlit Community).

We're also working on generating API docs for `StateModel` because it already inclues many helper functions (with more to come) such as:
- `dump()`: View all attribute values.
- Widget interaction helpers: Utilize widgets with `StateModel` following Streamlit's recommended patterns (For more details, refer to the [Streamlit Documentation on Working with Widgets in Multipage Apps](https://docs.streamlit.io/develop/concepts/multipage-apps/widgets)).
- Reset function: Reset all attribute values to their defaults.

## Contributing

If you have an idea for a new feature or have found a bug, please open an issue or submit a pull request. I don't have a formal code of conduct or contribution guidelines yet, but I appreciate respectful and constructive contributions.

## Development
The project is built with Flit and a Conda development environment (dev_environment.yml) is provided in the project root. 

Tests are built using pytest and [Streamlit's app testing framework](https://docs.streamlit.io/develop/api-reference/app-testing) ran against the demo app.