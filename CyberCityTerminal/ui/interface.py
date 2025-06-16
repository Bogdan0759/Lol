\
def print_message(message, lang_manager=None):
    """Prints a message to the console."""
    if lang_manager:
        # Assume message is a key and try to get the translated string.
        # If message is not a key, get_string will return message itself.
        print(lang_manager.get_string(message))
    else:
        # If no lang_manager, just print the message directly.
        print(message)

def print_location(location_name, description, lang_manager=None):
    """Prints the current location name and description."""
    # Use lang_manager for 'Location:' if available
    location_label = lang_manager.get_string("location_label") if lang_manager else "Location:"
    # Use lang_manager for location_name if available and location_name is a key
    translated_location_name = lang_manager.get_string(location_name) if lang_manager and location_name in lang_manager.translations else location_name
    print(f"\n{location_label} {translated_location_name}")
    # Use lang_manager for description if available and description is a key
    if lang_manager and description in lang_manager.translations:
        print(lang_manager.get_string(description))
    else:
        print(description)
