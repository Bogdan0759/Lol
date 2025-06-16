import json
import os

class LanguageManager:
    def __init__(self):
        self.translations = {}
        self.current_language = "english" # Default language

        # Get the absolute path of the script's directory
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data") # data is one level up from engine

    def load_language(self, lang_code):
        filepath = os.path.join(self.DATA_DIR, f"{lang_code}.json")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
            self.current_language = lang_code
            # Use get_string for the confirmation message after setting the language
            print(self.get_string("language_set_to_russian") if lang_code == "russian" else f"Language set to {lang_code}.")
            return True
        except FileNotFoundError:
            print(f"Error: Language file not found at {filepath}.")
            self.translations = {} # Clear translations if file not found
            return False
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {filepath}.")
            self.translations = {} # Clear translations if error
            return False

    def get_string(self, key, *args):
        """Gets a translated string for the given key.
           Supports basic formatting with *args.
        """
        # Fallback to key if translation not found
        message = self.translations.get(key, key)
        try:
            return message.format(*args)
        except IndexError as e:
            print(f"Error formatting string for key '{key}': {e}")
            return message # Return raw message if formatting fails

# Initialize with default language (English)
# This will be done in main.py now