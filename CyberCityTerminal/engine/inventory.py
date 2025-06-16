import json
import os # Import the os module

class Item:
    def __init__(self, name, description="", item_type="generic", effect=None):
        self.name = name
        self.description = description
        self.type = item_type # e.g., consumable, quest_item
        self.effect = effect # e.g., {"heal": 30}

    def __str__(self):
        return self.name

class Inventory:
    def __init__(self):
        self._items = []

    def add_item(self, item):
        if isinstance(item, Item):
            self._items.append(item)
            print(f"{item.name} added to inventory.")
        else:
            print("Can only add Item objects to inventory.")

    def remove_item(self, item_name):
        for item in self._items:
            if item.name.lower() == item_name.lower():
                self._items.remove(item)
                print(f"{item.name} removed from inventory.")
                return
        print(f"{item_name} not found in inventory.")

    def list_items(self):
        if not self._items:
            print("Inventory is empty.")
        else:
            print("Inventory:")
            for item in self._items:
                print(f"- {item.name}: {item.description}")

    def has_item(self, item_name):
        return any(item.name.lower() == item_name.lower() for item in self._items)

# Get the absolute path of the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data") # data is one level up from engine

def load_items(filepath="items.json"):
    """Loads item data from a JSON file."""
    # Construct the full path to the data file
    full_filepath = os.path.join(DATA_DIR, filepath)
    try:
        with open(full_filepath, 'r') as f:
            items_data = json.load(f)
            # Convert loaded data into Item objects if needed, or just return the dict
            # For now, let's just return the dictionary and create Item objects when needed.
            return items_data
    except FileNotFoundError:
        print(f"Error: {full_filepath} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {full_filepath}.")
        return {}
