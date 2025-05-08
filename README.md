# Luxury Furniture Studio

A high-end furniture application featuring interactive 3D visualization for a luxury brand. The application showcases premium furniture pieces with an emphasis on elegant design, user experience, and interactive elements.

## Features

- **Collection Gallery**: Browse through curated luxury furniture pieces
- **3D Visualization**: View and customize furniture with interactive 3D models
- **Custom Design Service**: Request bespoke furniture creation
- **Material Customization**: Explore different materials and finishes
- **Design Consultation**: Schedule sessions with senior designers

## Tech Stack

- **Backend & UI**: Python, Streamlit
- **3D Visualization**: Plotly 3D
- **Styling**: Custom CSS, Streamlit components

## Getting Started

### Prerequisites

- Python 3.8+
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/quantnexusai/luxury-furniture-app.git
   cd luxury-furniture-app
   ```

2. Set up the Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Development

### Streamlit Development

To run the Streamlit app in development mode:
```bash
streamlit run app.py
```
This will start the Streamlit server at http://localhost:8501.

### Adding New Furniture

To add new furniture items to the collection:

1. Add images to the `assets/furniture/` directory
2. Update the `furniture_data` list in the `display_collection()` function in `app.py`
3. For 3D models, add new visualization logic in the `display_configurator()` function

## Future Enhancements

- Integration with React and Three.js for more advanced 3D configurator
- Design mood board feature for creating visual collections
- User accounts and saved configurations
- AR visualization on mobile devices

## License

MIT License