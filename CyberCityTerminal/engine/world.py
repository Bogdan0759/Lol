import json
import os # Import the os module

locations = {}

# Get the absolute path of the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data") # data is one level up from engine

def load_locations(filepath="locations.json"):
    """Loads location data from a JSON file."""
    global locations
    # Construct the full path to the data file
    full_filepath = os.path.join(DATA_DIR, filepath)
    try:
        with open(full_filepath, 'r') as f:
            locations = json.load(f)
        print("Locations loaded successfully.")
    except FileNotFoundError:
        print(f"Error: {full_filepath} not found.")
        locations = {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {full_filepath}.")
        locations = {}

def get_location_info(location_id):
    """Gets information for a specific location."""
    return locations.get(location_id)

def move_to_location(current_location_id, direction):
    """Handles movement between locations."""
    current_location = get_location_info(current_location_id)
    if current_location and "exits" in current_location:
        next_location_id = current_location["exits"].get(direction.lower())
        if next_location_id and next_location_id in locations:
            return next_location_id
    return None
