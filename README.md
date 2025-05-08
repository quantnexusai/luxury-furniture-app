# Luxury Furniture App

A high-end furniture application featuring a 3D configurator for a luxury brand. The application showcases premium furniture pieces with an emphasis on elegant design, user experience, and interactive elements.

## Features

- **Collection Gallery**: Browse through curated luxury furniture pieces
- **3D Configurator**: Customize furniture with real-time 3D visualization
- **Custom Design Service**: Request bespoke furniture creation
- **Design Mood Board**: Create visual collections of materials, colors, and styles
- **Design Consultation**: Schedule sessions with senior designers

## Tech Stack

- **Frontend**: Next.js, React, Three.js, shadcn/ui
- **Backend**: Python, Streamlit
- **3D Rendering**: Three.js, React Three Fiber
- **Styling**: Tailwind CSS
- **Deployment**: GitHub Actions, Streamlit Cloud

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js and npm
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

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

4. Build the React components:
   ```bash
   npm run build
   ```

5. Run the Streamlit app:
   ```bash
   cd ..
   streamlit run app.py
   ```

## Development

### Frontend Development

To work on the frontend components:
```bash
cd frontend
npm run dev
```
This will start the Next.js development server at http://localhost:3000.

### Streamlit Development

To run the Streamlit app in development mode:
```bash
streamlit run app.py
```
This will start the Streamlit server at http://localhost:8501.

## Deployment

The app is automatically deployed to Streamlit Cloud when changes are pushed to the main branch. See the GitHub Actions workflow in `.github/workflows/deploy.yml` for details.

## License

MIT License