import random
import json # Import the json module
import os # Import the os module

def display_message(message, lang_manager=None):
    """Displays a general message to the user."""
    # If lang_manager is provided and message is a key, get translated string
    if lang_manager and isinstance(message, str) and message in lang_manager.translations:
        print(lang_manager.get_string(message))
    else:
        print(message)

def display_random_message(message_list, lang_manager=None):
    """Displays a random message from a list."""
    if message_list:
        message = random.choice(message_list)
        # If lang_manager is provided and message is a key, get translated string
        if lang_manager and isinstance(message, str) and message in lang_manager.translations:
            print(lang_manager.get_string(message))
        else:
            print(message)

# Get the absolute path of the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data") # data is one level up from ui

def load_messages(filepath="dialog.json"):
    """Loads messages/dialogue from a JSON file."""
    # Construct the full path to the data file
    full_filepath = os.path.join(DATA_DIR, filepath)
    try:
        with open(full_filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {full_filepath} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {full_filepath}.")
        return {}

# You can add more specific message handling functions here later
# based on different types of messages or events.
