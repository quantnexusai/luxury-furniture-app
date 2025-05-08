import json
import os

# Path to the data file
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "furniture_data.json")

def load_data():
    """Load data from the JSON file"""
    if not os.path.exists(DATA_FILE):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        
        # Create empty data structure
        data = {"furniture": []}
        
        # Save to file
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        
        return data
    
    # Load from file
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    """Save data to the JSON file"""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_furniture_items(filters=None):
    """
    Get furniture items with optional filtering
    
    Parameters:
    -----------
    filters : dict
        Filters to apply to the data
    
    Returns:
    --------
    List of furniture items
    """
    data = load_data()
    items = data.get("furniture", [])
    
    if not filters:
        return items
    
    # Apply filters
    filtered_items = items
    
    if "category" in filters and filters["category"] != "All":
        filtered_items = [item for item in filtered_items if item["category"] == filters["category"]]
    
    if "material" in filters and filters["material"] != "All":
        filtered_items = [
            item for item in filtered_items 
            if any(filters["material"].lower() in material.lower() for material in item["materials"])
        ]
    
    if "price_min" in filters and "price_max" in filters:
        filtered_items = [
            item for item in filtered_items 
            if filters["price_min"] <= item["price"] <= filters["price_max"]
        ]
    
    return filtered_items

def get_furniture_by_id(item_id):
    """Get a furniture item by ID"""
    data = load_data()
    items = data.get("furniture", [])
    
    for item in items:
        if item["id"] == item_id:
            return item
    
    return None

def save_configuration(config):
    """Save a furniture configuration"""
    data = load_data()
    
    if "configurations" not in data:
        data["configurations"] = []
    
    # Add the configuration
    data["configurations"].append(config)
    
    # Save to file
    save_data(data)
    
    return len(data["configurations"])