import json
import os # Import the os module

class Faction:
    def __init__(self, id, name, description, attitude=None):
        self.id = id
        self.name = name
        self.description = description
        self.attitude = attitude if attitude is not None else {} # Attitude towards other factions

    def __str__(self):
        return f"{self.name}: {self.description}"

class FactionManager:
    def __init__(self):
        self._factions = {}

    # Get the absolute path of the script's directory
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data") # data is one level up from engine

    def load_factions(self, filepath="factions.json"):
        """Loads faction data from a JSON file."""
        # Construct the full path to the data file
        full_filepath = os.path.join(self.DATA_DIR, filepath)
        try:
            with open(full_filepath, 'r') as f:
                factions_data = json.load(f)
                for faction_id, data in factions_data.items():
                    self._factions[faction_id] = Faction(faction_id, data["name"], data["description"], data.get("attitude", {}))
            print("Faction data loaded successfully.")
        except FileNotFoundError:
            print(f"Error: {full_filepath} not found.")
            self._factions = {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {full_filepath}.")
            self._factions = {}

    def get_faction_by_id(self, faction_id):
        """Returns a Faction object by its ID."""
        return self._factions.get(faction_id)

    def get_all_factions(self):
        """Returns a list of all Faction objects."""
        return list(self._factions.values())
