import random
import os
from ui.interface import print_message, print_location
from ui.commands import process_command
from engine.world import load_locations, get_location_info, move_to_location
from ui.messages import load_messages, display_random_message
from engine.player import Player
from engine.inventory import Item, load_items
from engine.combat import start_combat, Enemy
from engine.quests import QuestManager
from engine.hacking import attempt_hack
from engine.save_load import save_game, load_game
from engine.factions import FactionManager
from engine.language import LanguageManager 
import json

# Get the absolute path of the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

def load_enemies(filepath="enemies.json"):
    """Loads enemy data from a JSON file."""
    # Construct the full path to the data file
    full_filepath = os.path.join(DATA_DIR, filepath)
    try:
        with open(full_filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {full_filepath} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {full_filepath}.")
        return {}

def main():
    # Initialize LanguageManager and load default language
    lang_manager = LanguageManager()
    lang_manager.load_language("english")

    print_message(lang_manager.get_string("welcome_message"), lang_manager) # Pass lang_manager
    print_message(lang_manager.get_string("quit_instructions"), lang_manager) # Pass lang_manager

    load_locations() # This function is in engine/world.py, will need to fix there too
    dialogue_data = load_messages() # This function is in ui/messages.py, will need to fix there too
    enemies_data = load_enemies()
    items_data = load_items() # This function is in engine/inventory.py, will need to fix there too

    player = None
    quest_manager = None
    current_location_id = None
    faction_manager = FactionManager()
    faction_manager.load_factions() # This likely calls a function in engine/factions.py, will need to fix there too

    # Attempt to load a saved game
    loaded_data = load_game()
    if loaded_data and loaded_data[0] and loaded_data[1] and loaded_data[2]:
        player, quest_manager, current_location_id = loaded_data
        print_message(lang_manager.get_string("game_loaded_successfully"), lang_manager) # Pass lang_manager
    else:
        # Start a new game if no save or loading failed
        print_message(lang_manager.get_string("starting_new_game"), lang_manager) # Pass lang_manager
        player = Player("Vex")
        # Add a starting item to inventory using loaded data
        if "medkit" in items_data:
            medkit_info = items_data["medkit"]
            player.add_to_inventory(Item(medkit_info["name"], medkit_info["description"], medkit_info["type"], medkit_info.get("effect")))

        quest_manager = QuestManager()
        quest_manager.load_quests()
        current_location_id = "downtown"

    running = True
    while running:
        location_info = get_location_info(current_location_id)
        if location_info:
            print_location(location_info["name"], location_info["description"], lang_manager) # Pass lang_manager
            greeting_key = f"greeting_{current_location_id}"
            if greeting_key in dialogue_data:
                display_random_message(dialogue_data[greeting_key], lang_manager) # Pass lang_manager

            print_message(lang_manager.get_string("exits_label") + ", ".join(location_info.get("exits", {}).keys()), lang_manager) # Pass lang_manager

        # Check for completed quests after each command/action
        completed_quests_ids = quest_manager.check_active_quests_completion(player)
        for quest_id in completed_quests_ids:
            completed_quest = quest_manager.get_quest_by_id(quest_id)
            if completed_quest:
                print_message(lang_manager.get_string("quest_completed", completed_quest.name), lang_manager) # Pass lang_manager and format
                # Display quest completion dialogue
                if "quest_complete" in dialogue_data:
                    display_random_message(dialogue_data["quest_complete"], lang_manager) # Pass lang_manager
                # TODO: Implement reward distribution here

        # Simple combat encounter chance in industrial district
        if current_location_id == "industrial_district" and random.random() < 0.3: # 30% chance
            enemy_type = random.choice(list(enemies_data.keys()))
            enemy_info = enemies_data.get(enemy_type)
            if enemy_info:
                enemy = Enemy(enemy_info["name"], enemy_info["health"], enemy_info["damage"])
                combat_outcome = start_combat(player, enemy, items_data, dialogue_data, lang_manager) # Pass lang_manager to combat
                if not combat_outcome: # If player loses combat
                    print_message(lang_manager.get_string("game_over"), lang_manager) # Pass lang_manager
                    running = False # End the game
                    continue # Skip the rest of the loop

        command = input("> ").strip()

        # Check for movement commands first
        if command.lower() in ["north", "south", "east", "west"]:
            next_location_id = move_to_location(current_location_id, command)
            if next_location_id:
                current_location_id = next_location_id
                player.visit_location(current_location_id) # Record visited location
            else:
                print_message(lang_manager.get_string("cannot_go_that_way"), lang_manager) # Pass lang_manager
        else:
            # Pass necessary objects and functions to process_command, including lang_manager
            running, message = process_command(command, player, items_data, quest_manager, attempt_hack, dialogue_data, current_location_id, save_game, load_game, faction_manager, lang_manager) # Pass faction_manager and lang_manager
            if message:
                print_message(message, lang_manager) # Pass lang_manager

if __name__ == "__main__":
    main()
