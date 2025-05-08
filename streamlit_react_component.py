import os
import streamlit.components.v1 as components
import json

# Define the custom component for React integration
def react_component(component_path, props=None, height=None, key=None):
    """
    Render a React component in Streamlit.
    
    Parameters:
    -----------
    component_path : str
        Path to the component JS bundle
    props : dict
        Props to pass to the component
    height : int
        Height of the component
    key : str
        Unique key for the component
    
    Returns:
    --------
    The component's return value
    """
    if props is None:
        props = {}
    
    # Get absolute path to the component
    if not os.path.isabs(component_path):
        component_path = os.path.join(os.path.dirname(__file__), component_path)
    
    # Create the component
    return components.declare_component(
        f"react_{key}" if key else "react_component",
        path=component_path,
        props=props,
        default=None,
        height=height
    )

# Function to load the furniture configurator
def load_furniture_configurator(model_id, height=700, key=None):
    """
    Load the furniture configurator component.
    
    Parameters:
    -----------
    model_id : str
        ID of the model to load
    height : int
        Height of the component
    key : str
        Unique key for the component
    
    Returns:
    --------
    The component's return value (configuration)
    """
    component_path = "frontend/build"
    props = {"modelId": model_id}
    
    # Check if the component has been built
    if not os.path.exists(component_path):
        # Return placeholder with instructions
        return {"error": "React component not built. Run 'npm run build' in the frontend directory."}
    
    return react_component(component_path, props, height, key)