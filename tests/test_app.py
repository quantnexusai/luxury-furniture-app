import pytest
import streamlit as st
from app import load_furniture_data

# Mock Streamlit
class StreamlitMock:
    def __init__(self):
        self.state = {}
        self.text_data = []
        self.markdown_data = []
        self.title_data = []
    
    def text(self, text):
        self.text_data.append(text)
    
    def markdown(self, text):
        self.markdown_data.append(text)
    
    def title(self, text):
        self.title_data.append(text)
    
    def header(self, text):
        self.title_data.append(text)

# Replace streamlit with mock
st = StreamlitMock()

def test_load_furniture_data():
    """Test that furniture data is loaded correctly"""
    data = load_furniture_data()
    
    # Assert we have furniture data
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Assert each item has required fields
    for item in data:
        assert 'id' in item
        assert 'name' in item
        assert 'category' in item
        assert 'price' in item
        assert 'materials' in item
        assert 'image' in item