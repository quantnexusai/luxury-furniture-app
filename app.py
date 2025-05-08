import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="Luxury Furniture Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for luxury look and feel
st.markdown("""
<style>
    /* Global Typography */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600;700&family=Montserrat:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 400;
        color: #2c2c2c;
    }
    
    /* Luxury Color Palette */
    :root {
        --primary: #1e293b;
        --accent: #c9a873;
        --light: #f8f5f0;
        --dark: #18181b;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.title("Luxury Furniture Studio")
st.markdown("### Curated Elegance for Distinguished Spaces")

# Sidebar Navigation
with st.sidebar:
    st.markdown("## Navigation")
    page = st.radio(
        "Go to",
        ["Collection", "3D Configurator", "Custom Design", "About", "Contact"]
    )

# Functions for different pages
def display_collection():
    st.header("Exclusive Collection")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox("Category", ["All", "Seating", "Tables", "Storage", "Lighting", "Decor"])
    with col2:
        material = st.selectbox("Material", ["All", "Wood", "Marble", "Leather", "Metal", "Glass"])
    with col3:
        price_range = st.select_slider("Price Range", options=["All", "$1k-5k", "$5k-10k", "$10k-20k", "$20k+"])
    
    # Sample furniture data
    furniture_data = [
        {
            "id": 1,
            "name": "Milano Sofa",
            "description": "Handcrafted Italian leather sofa with walnut frame.",
            "price": 8950,
            "image": "assets/furniture/sofa.jpg"
        },
        {
            "id": 2,
            "name": "Vienna Coffee Table",
            "description": "Marble top coffee table with sculpted bronze base.",
            "price": 5650,
            "image": "assets/furniture/coffee_table.jpg"
        },
        {
            "id": 3,
            "name": "Oslo Dining Chair",
            "description": "Scandinavian-inspired dining chair with woven leather seat.",
            "price": 2450,
            "image": "assets/furniture/chair.jpg"
        },
        {
            "id": 4,
            "name": "Manhattan Bookshelf",
            "description": "Modular bookshelf system with adjustable shelves.",
            "price": 11200,
            "image": "assets/furniture/bookshelf.jpg"
        },
        {
            "id": 5,
            "name": "Kyoto Side Table",
            "description": "Japanese-inspired side table with intricate woodwork.",
            "price": 3950,
            "image": "assets/furniture/side_table.jpg"
        },
        {
            "id": 6,
            "name": "Paris Pendant Light",
            "description": "Hand-blown glass pendant with brushed brass fittings.",
            "price": 4250,
            "image": "assets/furniture/pendant.jpg"
        }
    ]
    
    # Define items_per_row if it's not already defined
    items_per_row = 3
    
    # Display in grid
    for i in range(0, len(furniture_data), items_per_row):
        cols = st.columns(items_per_row)
        for j in range(items_per_row):
            if i + j < len(furniture_data):
                with cols[j]:
                    item = furniture_data[i + j]
                    # Option 1: Just use the image with no width parameter
                    st.image(item["image"])
                    
                    # Or Option 2: See if width is supported 
                    # try:
                    #     st.image(item["image"], width=None)  # This should fill the column
                    # except TypeError:
                    #     st.image(item["image"])  # Fallback to no parameter
                    
                    st.markdown(f"### {item['name']}")
                    st.markdown(item["description"])
                    st.markdown(f"**${item['price']:,}**")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.button(f"View Details", key=f"view_{item['id']}")
                    with col2:
                        st.button(f"Configure", key=f"config_{item['id']}")
                        
def display_configurator():
    st.header("3D Furniture Configurator")
    
    # Select furniture piece to configure
    furniture_piece = st.selectbox(
        "Select Furniture to Configure",
        ["Milano Sofa", "Vienna Coffee Table", "Oslo Dining Chair", "Manhattan Bookshelf"]
    )
    
    st.subheader(f"{furniture_piece} Visualization")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create different shapes based on furniture selection
        if "Sofa" in furniture_piece:
            # Create a more sofa-like shape
            # Base dimensions
            length, width, height = 8, 3, 1
            
            # Create the base of the sofa
            x_base = np.linspace(0, length, 20)
            y_base = np.linspace(0, width, 20)
            X_base, Y_base = np.meshgrid(x_base, y_base)
            Z_base = np.zeros_like(X_base) + 0.2  # Low height for base
            
            # Create the seat cushion
            x_seat = np.linspace(0, length, 20)
            y_seat = np.linspace(0, width, 20)
            X_seat, Y_seat = np.meshgrid(x_seat, y_seat)
            Z_seat = np.zeros_like(X_seat) + 0.5
            # Add some cushion-like deformation
            for i in range(3):
                center_x = length * (i + 1) / 4
                Z_seat += 0.2 * np.exp(-0.5 * ((X_seat - center_x) ** 2 + (Y_seat - width/2) ** 2))
            
            # Create the backrest
            x_back = np.linspace(0, length, 20)
            z_back = np.linspace(0.5, height + 0.5, 20)
            X_back, Z_back = np.meshgrid(x_back, z_back)
            Y_back = np.zeros_like(X_back) + 0.2  # Backrest at the back of the sofa
            
            # Create a figure with multiple surfaces
            fig = go.Figure()
            fig.add_trace(go.Surface(z=Z_base, x=X_base, y=Y_base, colorscale='YlOrBr', showscale=False, opacity=0.9))
            fig.add_trace(go.Surface(z=Z_seat, x=X_seat, y=Y_seat, colorscale='YlOrBr', showscale=False, opacity=0.9))
            fig.add_trace(go.Surface(z=Z_back, x=X_back, y=Y_back, colorscale='YlOrBr', showscale=False, opacity=0.9))
        
        elif "Table" in furniture_piece:
            # Create a more realistic table
            # Table top
            x = np.linspace(-2, 2, 20)
            y = np.linspace(-1, 1, 20)
            X, Y = np.meshgrid(x, y)
            Z = np.zeros_like(X) + 0.75  # Table top height
            
            # Table legs positions
            x_legs = [-1.8, -1.8, 1.8, 1.8]
            y_legs = [-0.8, 0.8, -0.8, 0.8]
            z_bottom = [0, 0, 0, 0]
            z_top = [0.75, 0.75, 0.75, 0.75]
            
            fig = go.Figure()
            # Table top
            fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='earth', showscale=False, opacity=0.95))
            
            # Table legs using cylinders approximation with scatter3d
            for i in range(4):
                # Create points for a cylinder-like shape for each leg
                theta = np.linspace(0, 2*np.pi, 20)
                radius = 0.1  # Leg thickness
                
                for height in np.linspace(0, 0.75, 10):
                    x_circle = x_legs[i] + radius * np.cos(theta)
                    y_circle = y_legs[i] + radius * np.sin(theta)
                    z_circle = np.ones_like(theta) * height
                    
                    fig.add_trace(go.Scatter3d(
                        x=x_circle,
                        y=y_circle,
                        z=z_circle,
                        mode='markers',
                        marker=dict(size=5, color='brown', opacity=0.8),
                        showlegend=False
                    ))
        
        elif "Chair" in furniture_piece:
            # Create a dining chair
            # Seat dimensions
            seat_width, seat_depth = 1.2, 1.2
            seat_height = 0.45
            
            # Create seat
            x_seat = np.linspace(-seat_width/2, seat_width/2, 20)
            y_seat = np.linspace(-seat_depth/2, seat_depth/2, 20)
            X_seat, Y_seat = np.meshgrid(x_seat, y_seat)
            Z_seat = np.zeros_like(X_seat) + seat_height
            # Add some cushion-like deformation
            Z_seat -= 0.05 * np.exp(-0.5 * ((X_seat) ** 2 + (Y_seat) ** 2) / 0.3)
            
            # Create backrest
            x_back = np.linspace(-seat_width/2, seat_width/2, 20)
            z_back = np.linspace(seat_height, seat_height + 1, 20)
            X_back, Z_back = np.meshgrid(x_back, z_back)
            Y_back = np.zeros_like(X_back) - seat_depth/2  # Backrest at the back
            
            # Chair legs positions
            x_legs = [-seat_width/2 + 0.1, -seat_width/2 + 0.1, 
                      seat_width/2 - 0.1, seat_width/2 - 0.1]
            y_legs = [-seat_depth/2 + 0.1, seat_depth/2 - 0.1, 
                      -seat_depth/2 + 0.1, seat_depth/2 - 0.1]
            
            fig = go.Figure()
            # Seat
            fig.add_trace(go.Surface(z=Z_seat, x=X_seat, y=Y_seat, colorscale='YlOrBr', showscale=False, opacity=0.9))
            # Backrest
            fig.add_trace(go.Surface(y=Y_back, x=X_back, z=Z_back, colorscale='YlOrBr', showscale=False, opacity=0.9))
            
            # Chair legs
            for i in range(4):
                fig.add_trace(go.Scatter3d(
                    x=[x_legs[i], x_legs[i]],
                    y=[y_legs[i], y_legs[i]],
                    z=[0, seat_height],
                    mode='lines',
                    line=dict(color='brown', width=10),
                    showlegend=False
                ))
        
        elif "Bookshelf" in furniture_piece:
            # Create a bookshelf
            # Bookshelf dimensions
            width, depth, height = 2.5, 0.6, 3
            
            # Create outer frame panels
            # Back panel
            x_back = np.linspace(-width/2, width/2, 20)
            y_back = np.linspace(-depth/2, -depth/2, 20)
            X_back, Y_back = np.meshgrid(x_back, y_back)
            Z_back = np.linspace(0, height, 20)
            Z_back, _ = np.meshgrid(Z_back, np.zeros(20))
            
            # Left side panel
            x_left = np.linspace(-width/2, -width/2, 20)
            y_left = np.linspace(-depth/2, depth/2, 20)
            X_left, Y_left = np.meshgrid(x_left, y_left)
            Z_left = np.linspace(0, height, 20)
            Z_left, _ = np.meshgrid(Z_left, np.zeros(20))
            
            # Right side panel
            x_right = np.linspace(width/2, width/2, 20)
            y_right = np.linspace(-depth/2, depth/2, 20)
            X_right, Y_right = np.meshgrid(x_right, y_right)
            Z_right = np.linspace(0, height, 20)
            Z_right, _ = np.meshgrid(Z_right, np.zeros(20))
            
            # Shelves: Bottom, middle 1, middle 2, top
            shelf_heights = [0, height/4, height/2, 3*height/4, height]
            shelf_panels = []
            
            for h in shelf_heights:
                x_shelf = np.linspace(-width/2, width/2, 20)
                y_shelf = np.linspace(-depth/2, depth/2, 20)
                X_shelf, Y_shelf = np.meshgrid(x_shelf, y_shelf)
                Z_shelf = np.zeros_like(X_shelf) + h
                shelf_panels.append((X_shelf, Y_shelf, Z_shelf))
            
            fig = go.Figure()
            
            # Add all panels
            # Side panels
            fig.add_trace(go.Surface(z=Z_left, x=X_left, y=Y_left, colorscale='YlOrBr', showscale=False, opacity=0.9))
            fig.add_trace(go.Surface(z=Z_right, x=X_right, y=Y_right, colorscale='YlOrBr', showscale=False, opacity=0.9))
            fig.add_trace(go.Surface(x=X_back, y=Y_back, z=Z_back, colorscale='YlOrBr', showscale=False, opacity=0.9))
            
            # Shelves
            for i, (X_shelf, Y_shelf, Z_shelf) in enumerate(shelf_panels):
                fig.add_trace(go.Surface(z=Z_shelf, x=X_shelf, y=Y_shelf, colorscale='YlOrBr', showscale=False, opacity=0.9))
        
        else:
            # Generic shape as fallback
            theta = np.linspace(0, 2*np.pi, 100)
            phi = np.linspace(0, np.pi, 100)
            x = np.outer(np.cos(theta), np.sin(phi))
            y = np.outer(np.sin(theta), np.sin(phi))
            z = np.outer(np.ones_like(theta), np.cos(phi))
            
            fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='Viridis')])
        
        # Common layout settings for all furniture types
        fig.update_layout(
            width=600,
            height=500,
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(
                xaxis_title='Width',
                yaxis_title='Depth',
                zaxis_title='Height',
                aspectmode='data',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1),
                    up=dict(x=0, y=0, z=1)
                )
            )
        )
        
        # Add rotation controls
        fig.update_layout(
            updatemenus=[
                dict(
                    type='buttons',
                    showactive=False,
                    buttons=[
                        dict(
                            label='Rotate',
                            method='animate',
                            args=[None, dict(frame=dict(duration=30, redraw=True), 
                                             fromcurrent=True,
                                             mode='afterall')],
                        )
                    ],
                    x=0.1,
                    y=0.1,
                )
            ]
        )
        
        st.plotly_chart(fig)
    
    # Configuration panel (existing code)
    with col2:
        st.subheader("Customize Your Piece")
        
        # Material selection
        st.markdown("#### Materials")
        material = st.selectbox(
            "Primary Material",
            ["Oak", "Walnut", "Maple", "Ebony", "Mahogany"]
        )
        
        # Color options
        st.markdown("#### Finish")
        color = st.color_picker("Select color", "#3D2314")
        
        # Dimensions
        st.markdown("#### Dimensions")
        
        # Set appropriate dimension ranges based on furniture type
        if "Sofa" in furniture_piece:
            width = st.slider("Width (cm)", 180, 320, 240)
            depth = st.slider("Depth (cm)", 80, 120, 100)
            height = st.slider("Height (cm)", 70, 100, 85)
        elif "Table" in furniture_piece:
            width = st.slider("Width (cm)", 80, 180, 120)
            depth = st.slider("Depth (cm)", 60, 100, 80)
            height = st.slider("Height (cm)", 40, 60, 45)
        elif "Chair" in furniture_piece:
            width = st.slider("Width (cm)", 45, 65, 55)
            depth = st.slider("Depth (cm)", 45, 65, 55)
            height = st.slider("Height (cm)", 75, 95, 85)
        elif "Bookshelf" in furniture_piece:
            width = st.slider("Width (cm)", 120, 240, 180)
            depth = st.slider("Depth (cm)", 30, 60, 45)
            height = st.slider("Height (cm)", 180, 300, 240)
        else:
            width = st.slider("Width (cm)", 60, 300, 120)
            depth = st.slider("Depth (cm)", 60, 200, 90)
            height = st.slider("Height (cm)", 40, 200, 80)
        
        # Different feature options based on furniture type
        st.markdown("#### Features")
        if "Sofa" in furniture_piece:
            features = st.multiselect(
                "Additional Features",
                ["Premium Down Cushions", "Brass Feet", "Contrast Piping", "USB Charging Port", "Lumbar Support Pillows"]
            )
        elif "Table" in furniture_piece:
            features = st.multiselect(
                "Additional Features",
                ["Hidden Storage Drawer", "Glass Inlay", "Brass Detail Work", "Book-Matched Veining", "Felt-Lined Base"]
            )
        elif "Chair" in furniture_piece:
            features = st.multiselect(
                "Additional Features",
                ["Premium Seat Cushion", "Brass Foot Caps", "Leather Back Panel", "Custom Arm Rests", "Caning Detail"]
            )
        elif "Bookshelf" in furniture_piece:
            features = st.multiselect(
                "Additional Features",
                ["Integrated Lighting", "Glass Cabinet Doors", "Cable Management", "Adjustable Shelving", "Metal Accent Details"]
            )
        else:
            features = st.multiselect(
                "Additional Features",
                ["Premium Materials", "Custom Hardware", "Integrated Technology", "Bespoke Finishes"]
            )
        
        # Price calculation based on furniture type
        base_prices = {
            "Milano Sofa": 8950,
            "Vienna Coffee Table": 5650,
            "Oslo Dining Chair": 2450,
            "Manhattan Bookshelf": 11200
        }
        
        # Get base price for selected furniture or use default
        base_price = base_prices.get(furniture_piece, 5000)
        
        # Material price adjustments
        material_price = {"Oak": 0, "Walnut": 500, "Maple": 300, "Ebony": 1200, "Mahogany": 800}
        
        # Feature prices
        feature_prices = {
            # Sofa features
            "Premium Down Cushions": 499,
            "Brass Feet": 299,
            "Contrast Piping": 199,
            "USB Charging Port": 349,
            "Lumbar Support Pillows": 249,
            # Table features
            "Hidden Storage Drawer": 399,
            "Glass Inlay": 499,
            "Brass Detail Work": 299,
            "Book-Matched Veining": 599,
            "Felt-Lined Base": 149,
            # Chair features
            "Premium Seat Cushion": 199,
            "Brass Foot Caps": 149,
            "Leather Back Panel": 299,
            "Custom Arm Rests": 249,
            "Caning Detail": 349,
            # Bookshelf features
            "Integrated Lighting": 899,
            "Glass Cabinet Doors": 599,
            "Cable Management": 249,
            "Adjustable Shelving": 349,
            "Metal Accent Details": 399,
            # Generic features
            "Premium Materials": 599,
            "Custom Hardware": 399,
            "Integrated Technology": 699,
            "Bespoke Finishes": 499
        }
        
        # Calculate total price
        total_price = base_price + material_price.get(material, 0)
        for feature in features:
            total_price += feature_prices.get(feature, 0)
        
        # Add premium for custom dimensions
        standard_dimensions = {
            "Milano Sofa": (240, 100, 85),
            "Vienna Coffee Table": (120, 80, 45),
            "Oslo Dining Chair": (55, 55, 85),
            "Manhattan Bookshelf": (180, 45, 240)
        }
        
        # Check if dimensions are custom
        standard = standard_dimensions.get(furniture_piece, (120, 80, 60))
        if width != standard[0] or depth != standard[1] or height != standard[2]:
            total_price = int(total_price * 1.1)  # 10% premium for custom dimensions
        
        st.markdown(f"#### Estimated Price: **${total_price:,}**")
        
        # Call-to-action buttons
        if st.button("Save Configuration", key="save_config"):
            st.success("Your custom configuration has been saved!")
        
        if st.button("Add to Project", key="add_project"):
            st.success("Added to your project!")

def display_custom_design():
    st.header("Custom Design Service")
    
    st.markdown("""
    ## Bespoke Furniture Creation
    
    Our artisans will craft exclusive pieces tailored to your exact specifications and style preferences.
    
    ### Process:
    1. **Consultation** - Meet with our design team
    2. **Concept Development** - Review sketches and materials
    3. **Production** - Handcrafted by master artisans
    4. **Delivery & Installation** - White glove service
    """)
    
    # Form for custom request
    with st.form("custom_design_form"):
        st.subheader("Start Your Custom Design Journey")
        
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        
        project_type = st.selectbox(
            "Project Type",
            ["Single Furniture Piece", "Room Design", "Full Home Collection", "Commercial Space"]
        )
        
        description = st.text_area("Project Description", height=150,
                                  placeholder="Describe your vision, space, and specific requirements...")
        
        budget = st.select_slider(
            "Budget Range",
            options=["$5,000 - $10,000", "$10,000 - $25,000", "$25,000 - $50,000", "$50,000 - $100,000", "$100,000+"]
        )
        
        timeline = st.selectbox(
            "Desired Timeline",
            ["1-2 months", "3-4 months", "5-6 months", "6+ months"]
        )
        
        file_upload = st.file_uploader("Upload Inspiration Images or Floor Plans", 
                                     type=["jpg", "png", "pdf"], accept_multiple_files=True)
        
        submitted = st.form_submit_button("Submit Design Request")
        
        if submitted:
            st.success("Thank you for your design request. Our team will contact you within 24 hours to schedule your consultation.")

def display_about():
    st.header("About Our Atelier")
    
    st.markdown("""
    ## Heritage of Craftsmanship
    
    For over three decades, our atelier has been creating bespoke furniture pieces that blend traditional craftsmanship with contemporary design. Each piece is meticulously handcrafted by our master artisans, using only the finest materials sourced from sustainable suppliers worldwide.
    
    ## Our Philosophy
    
    We believe that luxury furniture should not only be visually stunning but also functional and enduring. Our designs emphasize:
    
    - **Timeless Aesthetics** - Pieces that transcend trends
    - **Exceptional Materials** - The finest woods, metals, and textiles
    - **Masterful Craftsmanship** - Techniques passed down through generations
    - **Sustainability** - Responsible sourcing and production practices
    """)
    
    # Display team
    st.subheader("Our Leadership")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("assets/team/1.png", width=200)
        st.markdown("**Alessandro Ricci**")
        st.markdown("*Founder & Creative Director*")
    
    with col2:
        st.image("assets/team/2.png", width=200)
        st.markdown("**Sophia Chen**")
        st.markdown("*Head of Design*")
    
    with col3:
        st.image("assets/team/3.png", width=200)
        st.markdown("**Marcus Lindholm**")
        st.markdown("*Master Craftsman*")

def display_contact():
    st.header("Contact Us")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### Visit Our Showroom
        
        **New York**  
        120 Greene Street  
        SoHo, New York, NY 10012  
        +1 (212) 555-1234
        
        **London**  
        18 Brompton Road  
        Knightsbridge, London SW1X 7QN  
        +44 20 7946 0851
        
        **Milan**  
        Via Montenapoleone, 8  
        20121 Milano MI, Italy  
        +39 02 7634 7180
        """)
        
        st.markdown("""
        ### Hours
        
        Monday - Friday: 10:00 AM - 7:00 PM  
        Saturday: 11:00 AM - 6:00 PM  
        Sunday: By appointment only
        """)
    
    with col2:
        with st.form("contact_form"):
            st.subheader("Send a Message")
            
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            subject = st.text_input("Subject")
            message = st.text_area("Message", height=150)
            
            submitted = st.form_submit_button("Send Message")
            
            if submitted:
                st.success("Thank you for your message. We will respond within 24 hours.")
    
    # Map (placeholder)
    st.markdown("### Our Locations")
    st.image("assets/map_placeholder.jpg", caption="Our global showrooms")

# Display the selected page
if page == "Collection":
    display_collection()
elif page == "3D Configurator":
    display_configurator()
elif page == "Custom Design":
    display_custom_design()
elif page == "About":
    display_about()
else:
    display_contact()