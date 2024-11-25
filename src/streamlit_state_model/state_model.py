import streamlit as st
import json 
import inspect 
import ast
from typing import Any,Dict,List,Literal
from .default_factory import DefaultFactory

class StateModel: 
    """
    This class is meant to be used as parent class for other classes that will wrap the session state. 
    
    This setup allows you to define the variables as attributes in the wrapper class, but all actual i/o with the attribute value is forwarded to the streamlit.session_state variable with a name matching the defined attribute.

    A class instance is holding nothing besides annotations on the attributes that are available within the StateModel.
    """

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    @property
    def docstrings(self) -> Dict[str,str]:
        """
        Dictionary of attribute names and their documentation strings.

        Returns:
            Dict[str,str]: A dictionary where keys are attribute names and values are their docstrings.
        """
        return st.session_state.get("_state_model", {}).get(self.class_name, {}).get("_docstrings", {})
    
    @property
    def is_created(self) -> bool:
        "Boolean that flags whether or not the instance of this class already exists in the streamlit.session_state."
        return self.class_name in st.session_state["_state_model"]

    def __init__(
        self,
        mode : Literal["build","lazy", "strict"] = "lazy",
        **kwargs : Dict[str, Any]
    ):
        """
        Initializes an instance of the StateModel class, allowing attributes to be managed through 
        Streamlit's session state mechanism. This method ensures that attributes defined in the class annotations are managed by Streamlit's session state, 
        allowing persistent stateful behavior across page reloads in Streamlit applications.

        Args: 
        mode (str) : Literal["build","lazy", "strict"], default "lazy"
            - "build": Initializes the session state with default values defined in the class annotations. Prevents re-initialization if the session state has already been created. First call will set attributes directly, but subsequent calls will do nothing. This allows you to override defaults on initial build inline with the rest of your app code.
            - "lazy": Since a class instance holds no data, lazy mode just returns an instance that reflects the defined class structure and attribute values will always reflect the current values in the session state. Raises a ValueError if any keyword arguments are provided, as no attributes should be set in this mode.
            - "strict": Requires that the class instance already exist in the session state. If it does not, it will throw an error. Allows setting attributes from the provided kwargs, with no additional restrictions.
        **kwargs (dict[str, Any]) : Keyword arguments representing attributes of the class that you would like to set in this init call.
        """
        #make sure key for _state_model exists in session state
        if "_state_model" not in st.session_state:
            st.session_state["_state_model"] = {}

        #catch no action conditions
        if mode == "build" and self.is_created: #intention here is allow a build mode call to sit inline in page code and do nothing after instance is created 
            return
        if mode == "lazy": 
            return 

        #catch error conditions 
        if mode == "lazy" and kwargs:
            raise ValueError("Keyword arguments cannot be provided in lazy mode.")
        if mode == "strict" and not self.is_created:
            raise ValueError(f"{self.__class__.__name__} has not yet been created.")

        #catch conditons that require action 
        if mode == "strict": 
            self._set_attr_from_kwargs(**kwargs)
        elif mode == "build": #does not exist implied by error condition 
            st.session_state["_state_model"][self.class_name] = {}
            self.set_attr_to_default()
            self._set_attr_from_kwargs(**kwargs)
            self._initialize_doc_strings()
        else:
            raise ValueError(f"Invalid mode: {mode}")

    def __getattribute__(self, name: str) -> Any:
        """
        Retrieve the value of a session state variable.
        """
        #avoid recursion by using super().__getattribute__ for accessing class-level attributes
        annotations = super().__getattribute__("__annotations__")
        if name in annotations:
            if name in st.session_state["_state_model"][self.class_name]:
                return st.session_state["_state_model"][self.class_name][name]
            else:
                raise ValueError(f"Attribute {name} has not been initialized in streamlit.session_state")
        return super().__getattribute__(name)

    def __setattr__(
        self, 
        name: str, 
        value: Any
    ) -> None:
        if name not in self.__annotations__:
            raise AttributeError(f"{self.__class__.__name__} object has no attribute {name}")
        st.session_state["_state_model"][self.class_name][name] = value
    
    def _set_attr_from_kwargs(self,
        **kwargs : Dict[str,Any]
    ) -> None:
        """
        Sets attributes on the class instance based on the provided keyword arguments. This method assigns values to attributes
        by updating the instance with the given kwargs.

        Args:
        **kwargs (dict[str, Any]) : Keyword arguments representing attributes of the class that you would like to set in this init call.

        Raises:
        ValueError: 
            If keyword arguments are provided in "lazy" mode, since this mode does not allow setting of attributes 
            through keyword arguments.
        """
        for key, value in kwargs.items():
                self.__setattr__(key,value)
    
    def dump(
        self,
        exclude: List[str] = None
    ) -> str:
        """
        Dumps all defined session state attributes to a JSON string, with the option to exclude specified attributes.

        Args:
        exclude (List[str], optional) : A list of attribute names to exclude from the output. Defaults to None, 
            which means no attributes will be excluded. If provided, the attributes in this list will not be included 
            in the resulting JSON string.

        Returns:
        str : A JSON string containing the session state attributes and their values, excluding any specified attributes.
        """
        if exclude is None:
            exclude = []
        state_dict = {key: st.session_state["_state_model"][self.class_name].get(key) for key in self.__annotations__ if key not in exclude}
        return json.dumps(state_dict)

    def get_defaults(self) -> Dict[str, Any]:
        """
        Get the default values for all attributes of the class.

        Returns:
        dict[str, Any]: A dictionary containing the default values for all attributes.
        """
        defaults = {}
        for attr_name in self.__class__.__annotations__.keys():
            class_attr = getattr(self.__class__, attr_name, None)
            if isinstance(class_attr, DefaultFactory):  # if factory, get value from factory
                default_value = class_attr.default_factory()
            else:
                default_value = class_attr
            defaults[attr_name] = default_value
        return defaults

    def set_attr_to_default(self) -> None:
        """
        Reset all attributes of the class back to their defaults.
        """
        defaults = self.get_defaults()
        self._set_attr_from_kwargs(**defaults)

    def is_default(self) -> bool:
        """Check if the all values in the instance match the defined defaults of the class."""
        defaults = self.get_defaults()
        for attr_name, default_value in defaults.items():
            if getattr(self, attr_name) != default_value:
                return False
        return True

    def _get_documentation(self, name: str) -> str:
        """
        Internal method used by _initialize_doc_strings to populate the docstring for a specific attribute based on its name by inspecting the source code.

        Args:
            name (str): The name of the attribute.

        Returns:
            str: The docstring of the attribute, or a message if not found.
        """
        source = inspect.getsource(self.__class__)
        tree = ast.parse(source)
        class_node = None
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == self.__class__.__name__:
                class_node = node
                break
        if not class_node:
            return "No docstring found"
        for idx, node in enumerate(class_node.body):
            if isinstance(node, (ast.AnnAssign, ast.Assign)):
                if isinstance(node, ast.AnnAssign):
                    attr_name = node.target.id if isinstance(node.target, ast.Name) else None
                elif isinstance(node, ast.Assign):
                    targets = node.targets
                    if len(targets) == 1 and isinstance(targets[0], ast.Name):
                        attr_name = targets[0].id
                    else:
                        continue
                else:
                    continue
                if attr_name == name:
                    if idx + 1 < len(class_node.body):
                        next_node = class_node.body[idx + 1]
                        if isinstance(next_node, ast.Expr) and isinstance(next_node.value, ast.Constant):
                            docstring = next_node.value.value
                            return docstring.strip()
                    return "No docstring found"
        return "No docstring found"

    def _initialize_doc_strings(self):
        """
        Initialize the doc_strings in st.session_state by extracting docstrings for all annotations.
        """
        if self.class_name not in st.session_state["_state_model"]:
            st.session_state["_state_model"][self.class_name] = {}
        if "_docstrings" not in st.session_state["_state_model"][self.class_name]:
            st.session_state["_state_model"][self.class_name]["_docstrings"] = {}
        for name in self.__annotations__:
            docstring = self._get_documentation(name)
            st.session_state["_state_model"][self.class_name]["_docstrings"][name] = docstring

    @classmethod
    def get_temp_key_name(cls,attr_name: str) -> str: 
        "The temporary key name used to store the value of the attribute in streamlit.session_state within the current page."
        return "_"+attr_name
    
    @classmethod
    def load_value(cls,attr_name: str) -> None:
        "Load the value of the attribute from streamlit.session_state."
        class_name = cls.__name__
        st.session_state[cls.get_temp_key_name(attr_name)] = st.session_state["_state_model"][class_name][attr_name]

    @classmethod
    def store_value(cls,attr_name: str) -> None:
        "Store the value of the attribute in streamlit.session_state."
        class_name = cls.__name__
        st.session_state["_state_model"][class_name][attr_name] = st.session_state[cls.get_temp_key_name(attr_name)]