import streamlit as st
import streamlit.components.v1 as components
import os
import json

def load_shadcn_component(component_name, props=None, height=None, key=None):
    """
    Load a shadcn/ui component.
    
    Parameters:
    -----------
    component_name : str
        Name of the component to load
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
    
    # Use the streamlit-shadcn-ui package for rendering shadcn components
    try:
        from streamlit_shadcn_ui import shadcn
        return shadcn(component_name, props=props, key=key)
    except ImportError:
        # Fallback to standard Streamlit components if package not available
        st.warning(f"streamlit-shadcn-ui not installed. Using standard Streamlit components.")
        
        # Map shadcn component names to Streamlit equivalents
        if component_name == "button":
            return st.button(props.get("text", "Button"), key=key)
        elif component_name == "input":
            return st.text_input(
                props.get("label", ""),
                value=props.get("value", ""),
                key=key
            )
        elif component_name == "select":
            return st.selectbox(
                props.get("label", ""),
                options=props.get("options", []),
                index=props.get("defaultValue", 0),
                key=key
            )
        elif component_name == "checkbox":
            return st.checkbox(
                props.get("label", ""),
                value=props.get("checked", False),
                key=key
            )
        elif component_name == "slider":
            return st.slider(
                props.get("label", ""),
                min_value=props.get("min", 0),
                max_value=props.get("max", 100),
                value=props.get("value", 50),
                step=props.get("step", 1),
                key=key
            )
        else:
            st.error(f"Component {component_name} not supported in fallback mode")
            return None

# Example usage in Streamlit
def shadcn_button(label, variant="default", size="default", key=None):
    """
    Render a shadcn/ui button.
    
    Parameters:
    -----------
    label : str
        Button text
    variant : str
        Button variant (default, outline, destructive, etc.)
    size : str
        Button size (default, sm, lg)
    key : str
        Unique key for the component
    
    Returns:
    --------
    Boolean indicating if the button was clicked
    """
    props = {
        "text": label,
        "variant": variant,
        "size": size
    }
    return load_shadcn_component("button", props, key=key)

def shadcn_input(label, placeholder="", key=None):
    """Render a shadcn/ui input field."""
    props = {
        "label": label,
        "placeholder": placeholder
    }
    return load_shadcn_component("input", props, key=key)