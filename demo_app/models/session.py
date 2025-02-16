from typing import List
import streamlit_state_model as ssm 

class Session(ssm.StateModel):
    favorite_color: str = "#252D3D"
    "The user's favorite color as a hex string."
    favorite_number: int = 0
    "The user's favorite number."
    favorite_foods: List[str] = ssm.DefaultFactory(lambda: ["🍕", "🍣", "🌮"])
    """
    A list of the user's favorite foods as emoji strings. Users can select as many as they like (from the available options).
    """
