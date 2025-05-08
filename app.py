import streamlit as st
from streamlit_three_d_viewer import streamlit_three_d_viewer
import pandas as pd
import json
import os

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
    
    /* Button Styling */
    .stButton > button {
        background-color: var(--primary);
        color: var(--light);
        border: none;
        border-radius: 2px;
        padding: 12px 24px;
        font-family: 'Montserrat', sans-serif;
        font-weight: 500;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: var(--accent);
        color: var(--dark);
    }
    
    /* Card Styling */
    [data-testid="stVerticalBlock"] {
        padding: 20px;
        border-radius: 4px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--light);
        border-right: 1px solid rgba(201, 168, 115, 0.2);
    }
    
    /* Main area */
    .main .block-container {
        padding: 40px;
    }
    
    /* Header */
    .main .block-container > div:first-child h1 {
        font-size: 3.5rem;
        margin-bottom: 2rem;
        color: var(--primary);
        letter-spacing: 1px;
    }
    
    /* Custom Components - Furniture Cards */
    .furniture-card {
        border: 1px solid rgba(201, 168, 115, 0.3);
        border-radius: 4px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    .furniture-card:hover {
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
        transform: translateY(-5px);
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.title("Luxury Furniture Studio")
st.markdown("### Curated Elegance for Distinguished Spaces")

# Sidebar Navigation
with st.sidebar:
    st.image("assets/logo.png", width=150)
    st.markdown("## Navigation")
    page = st.radio(
        "Go to",
        ["Collection", "3D Configurator", "Custom Design", "About", "Contact"]
    )

# Main Content
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

# Import shadcn UI components
from streamlit_shadcn_ui import shadcn_button, shadcn_input

# Then use them in your app
# For example, in the display_collection function:

def display_collection():
    st.header("Exclusive Collection")
    
    # Filter options with shadcn components
    col1, col2, col3 = st.columns(3)
    with col1:
        category = shadcn_input("Category", placeholder="All categories", key="category_filter")
    with col2:
        material = shadcn_input("Material", placeholder="All materials", key="material_filter")
    with col3:
        price_range = st.select_slider("Price Range", options=["All", "$1k-5k", "$5k-10k", "$10k-20k", "$20k+"])
    
    # Apply button with shadcn style
    if shadcn_button("Apply Filters", variant="default", key="apply_filters"):
        st.session_state.filters_applied = True
    
    # Rest of the function remains the same...
    
    # Display furniture items in a grid
    items_per_row = 3
    furniture_data = load_furniture_data()
    
    # Filter based on selections
    if category != "All":
        furniture_data = [item for item in furniture_data if item["category"] == category]
    if material != "All":
        furniture_data = [item for item in furniture_data if material.lower() in item["materials"].lower()]
    if price_range != "All":
        # Logic to filter by price range
        pass
    
    # Display in grid
    for i in range(0, len(furniture_data), items_per_row):
        cols = st.columns(items_per_row)
        for j in range(items_per_row):
            if i + j < len(furniture_data):
                with cols[j]:
                    item = furniture_data[i + j]
                    with st.container():
                        st.markdown(f"""
                        <div class="furniture-card">
                            <img src="{item['image']}" width="100%">
                            <h3>{item['name']}</h3>
                            <p>{item['description'][:100]}...</p>
                            <p style="color: #c9a873; font-weight: 600;">${item['price']:,}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.button(f"View Details {item['id']}", key=f"view_{item['id']}")
                        with col2:
                            st.button(f"Configure {item['id']}", key=f"config_{item['id']}")

def display_configurator():
    from streamlit_react_component import load_furniture_configurator
    
    st.header("3D Furniture Configurator")
    
    # Select furniture piece to configure
    furniture_piece = st.selectbox(
        "Select Furniture to Configure",
        ["Milano Sofa", "Vienna Coffee Table", "Oslo Dining Chair", "Manhattan Bookshelf"]
    )
    
    # Map selection to model ID
    model_id_map = {
        "Milano Sofa": "sofa",
        "Vienna Coffee Table": "coffeeTable",
        "Oslo Dining Chair": "diningChair",
        "Manhattan Bookshelf": "bookshelf"
    }
    model_id = model_id_map.get(furniture_piece, "sofa")
    
    # Load the React component
    config_result = load_furniture_configurator(model_id, height=700, key="furniture_config")
    
    # Handle the result
    if isinstance(config_result, dict) and "error" in config_result:
        # Show placeholder if component not built
        col1, col2 = st.columns([2, 1])
        with col1:
            st.image("assets/placeholder_3d.png", caption="3D Model Placeholder")
            st.info("React component not built yet. Follow the setup instructions.")
        
        with col2:
            st.subheader("Customize Your Piece")
            # Display simplified configurator UI
            material = st.selectbox("Primary Material", ["Oak", "Walnut", "Maple", "Ebony", "Mahogany"])
            color = st.color_picker("Select color", "#3D2314")
            # Additional simplified controls...
    else:
        # Display the saved configuration if available
        if config_result:
            st.subheader("Saved Configuration")
            st.json(config_result)
            
            if st.button("Add to Project", key="add_to_project"):
                st.success("Configuration added to your project!")

def display_custom_design():
    st.header("Custom Design Service")
    
    # Tabs for different design services
    tabs = st.tabs(["Bespoke Furniture", "Mood Board", "Design Consultation"])
    
    with tabs[0]:
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
    
    with tabs[1]:
        st.markdown("""
        ## Design Mood Board
        
        Create a visual collection of materials, colors, and styles to define the aesthetic direction of your project.
        """)
        
        # Load React mood board component if available, otherwise show placeholder
        try:
            from streamlit_react_component import load_react_component
            mood_board_component = load_react_component("mood-board", height=800, key="mood_board")
            
            if isinstance(mood_board_component, dict) and "selections" in mood_board_component:
                st.subheader("Your Saved Selections")
                st.json(mood_board_component["selections"])
                
                if st.button("Create Design Brief Based on Selections"):
                    st.success("Design brief created and sent to your email!")
        except:
            # Placeholder mood board with standard Streamlit components
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Materials")
                materials = st.multiselect(
                    "Select materials",
                    ["Walnut Wood", "Calacatta Marble", "Brushed Brass", "Full-Grain Leather", 
                     "Smoked Oak", "Velvet", "Linen", "Bronze", "Glass"]
                )
                
                st.subheader("Colors")
                colors = st.color_picker("Primary Color", "#1A2A40")
                accent_color = st.color_picker("Accent Color", "#D4AF37")
            
            with col2:
                st.subheader("Style Preferences")
                styles = st.multiselect(
                    "Select styles",
                    ["Modern Minimalist", "Art Deco", "Contemporary Craftsman", 
                     "Scandinavian Luxury", "Industrial Elegance", "Japanese Influence"]
                )
                
                st.subheader("Inspirations")
                inspirations = st.text_area("Describe your inspirations", 
                                           placeholder="e.g., Modern Parisian apartment, Japanese minimalism...")
            
            if st.button("Create Mood Board"):
                st.success("Mood board created! A design team member will contact you to discuss your selections.")
    
    with tabs[2]:
        st.markdown("""
        ## Design Consultation
        
        Schedule a one-on-one session with our senior designers to discuss your vision, requirements, and design direction.
        """)
        
        # Consultation scheduling form
        with st.form("consultation_form"):
            st.subheader("Schedule a Consultation")
            
            name = st.text_input("Full Name", key="consult_name")
            email = st.text_input("Email Address", key="consult_email")
            phone = st.text_input("Phone Number", key="consult_phone")
            
            consultation_type = st.radio(
                "Consultation Type",
                ["Virtual", "In-Showroom", "On-Site Visit"]
            )
            
            if consultation_type == "On-Site Visit":
                address = st.text_area("Property Address")
            
            preferred_date = st.date_input("Preferred Date")
            preferred_time = st.selectbox(
                "Preferred Time",
                ["Morning (9AM-12PM)", "Afternoon (12PM-4PM)", "Evening (4PM-7PM)"]
            )
            
            design_focus = st.multiselect(
                "Design Focus",
                ["Furniture Selection", "Space Planning", "Material & Finish Selection", 
                 "Lighting Design", "Color Scheme", "Art & Accessories"]
            )
            
            submitted = st.form_submit_button("Request Consultation")
            
            if submitted:
                st.success("Thank you for your consultation request. Our team will confirm your appointment within 24 hours.")

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
    
    ## Our Artisans
    
    Our team includes woodworkers, metalworkers, upholsterers, and designers who have dedicated their lives to their craft. Many have been with us for decades, bringing unparalleled expertise to each creation.
    """)
    
    # Display team
    st.subheader("Our Leadership")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("assets/placeholder_person1.jpg", width=200)
        st.markdown("**Alessandro Ricci**")
        st.markdown("*Founder & Creative Director*")
    
    with col2:
        st.image("assets/placeholder_person2.jpg", width=200)
        st.markdown("**Sophia Chen**")
        st.markdown("*Head of Design*")
    
    with col3:
        st.image("assets/placeholder_person3.jpg", width=200)
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
    st.image("assets/map_placeholder.jpg", caption="Interactive map will be implemented here")

def load_furniture_data():
    # In a real app, this would load from a database or API
    # This is sample data for demonstration
    return [
        {
            "id": 1,
            "name": "Milano Sofa",
            "category": "Seating",
            "description": "Handcrafted Italian leather sofa with walnut frame and brass accents.",
            "price": 8950,
            "materials": "Leather, Walnut, Brass",
            "image": "assets/furniture/sofa.jpg"
        },
        {
            "id": 2,
            "name": "Vienna Coffee Table",
            "category": "Tables",
            "description": "Marble top coffee table with sculpted bronze base.",
            "price": 5650,
            "materials": "Marble, Bronze",
            "image": "assets/furniture/coffee_table.jpg"
        },
        {
            "id": 3,
            "name": "Oslo Dining Chair",
            "category": "Seating",
            "description": "Scandinavian-inspired dining chair with woven leather seat and oak frame.",
            "price": 2450,
            "materials": "Oak, Leather",
            "image": "assets/furniture/chair.jpg"
        },
        {
            "id": 4,
            "name": "Manhattan Bookshelf",
            "category": "Storage",
            "description": "Modular bookshelf system with adjustable shelves and integrated lighting.",
            "price": 11200,
            "materials": "Walnut, Glass, Brass",
            "image": "assets/furniture/bookshelf.jpg"
        },
        {
            "id": 5,
            "name": "Kyoto Side Table",
            "category": "Tables",
            "description": "Japanese-inspired side table with intricate woodwork and hidden compartment.",
            "price": 3950,
            "materials": "Cherry Wood, Maple",
            "image": "assets/furniture/side_table.jpg"
        },
        {
            "id": 6,
            "name": "Paris Pendant Light",
            "category": "Lighting",
            "description": "Hand-blown glass pendant with brushed brass fittings.",
            "price": 4250,
            "materials": "Glass, Brass",
            "image": "assets/furniture/pendant.jpg"
        }
    ]

# Run the app
if __name__ == "__main__":
    # This will be executed when the script is run directly
    pass