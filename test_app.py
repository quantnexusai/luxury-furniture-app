import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Configure page
st.set_page_config(
    page_title="Luxury Furniture Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=Montserrat:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 400;
        color: #2c2c2c;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.title("Luxury Furniture Studio")
st.markdown("### Curated Elegance for Distinguished Spaces")

# Sidebar
with st.sidebar:
    st.markdown("## Navigation")
    page = st.radio(
        "Go to",
        ["Collection", "Simple 3D Viewer", "Custom Design", "About", "Contact"]
    )

# Main Content
if page == "Collection":
    st.header("Exclusive Collection")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox("Category", ["All", "Seating", "Tables", "Storage", "Lighting", "Decor"])
    with col2:
        material = st.selectbox("Material", ["All", "Wood", "Marble", "Leather", "Metal", "Glass"])
    with col3:
        price_range = st.select_slider("Price Range", options=["All", "$1k-5k", "$5k-10k", "$10k-20k", "$20k+"])
    
    # Display sample furniture items
    items_per_row = 3
    for i in range(2):
        cols = st.columns(items_per_row)
        for j in range(items_per_row):
            with cols[j]:
                st.image("https://via.placeholder.com/300x200.png?text=Furniture+Item", use_column_width=True)
                st.markdown(f"### Sample Furniture {i*3+j+1}")
                st.markdown("Elegant description of this luxury piece.")
                st.markdown("**$5,999**")
                st.button(f"View Details {i*3+j+1}")

elif page == "Simple 3D Viewer":
    st.header("3D Furniture Visualization")
    
    # Select furniture type
    furniture_type = st.selectbox(
        "Select Furniture Type",
        ["Sofa", "Table", "Chair", "Bookshelf"]
    )
    
    # Create a simple 3D visualization using Plotly
    st.subheader(f"{furniture_type} Visualization")
    
    # Create different shapes based on selection
    if furniture_type == "Sofa":
        # Create a simple sofa shape
        x = np.linspace(0, 10, 100)
        y = np.linspace(0, 5, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X/2) * np.cos(Y/2) + 2
        
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
    
    elif furniture_type == "Table":
        # Create a simple table shape
        x = np.linspace(-5, 5, 50)
        y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X) + 2  # Flat surface
        
        # Table legs
        x_legs = [-4, -4, 4, 4]
        y_legs = [-4, 4, -4, 4]
        z_legs = [0, 0, 0, 0]
        
        fig = go.Figure()
        fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Browns', showscale=False))
        fig.add_trace(go.Scatter3d(x=x_legs, y=y_legs, z=z_legs, mode='lines',
                               line=dict(color='brown', width=10)))
    
    else:
        # Generic shape for other furniture
        theta = np.linspace(0, 2*np.pi, 100)
        phi = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(theta), np.sin(phi))
        y = np.outer(np.sin(theta), np.sin(phi))
        z = np.outer(np.ones_like(theta), np.cos(phi))
        
        fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='Blues')])
    
    fig.update_layout(
        title=f"3D {furniture_type} Model",
        width=800,
        height=600,
        scene=dict(
            xaxis_title='Width',
            yaxis_title='Depth',
            zaxis_title='Height',
            aspectratio=dict(x=1, y=1, z=0.7),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1))
        )
    )
    
    st.plotly_chart(fig)
    
    # Material selection
    st.subheader("Customize Materials")
    material = st.selectbox(
        "Primary Material",
        ["Oak", "Walnut", "Maple", "Leather", "Velvet", "Marble"]
    )
    
    color = st.color_picker("Select color shade", "#3D2314")
