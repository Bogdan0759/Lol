import json
import os
from .player import Player
from .quests import QuestManager, Quest
from .inventory import Item # Import Item class

SAVE_DIR = "saves/"

def save_game(player, quest_manager, current_location_id, filename="savegame.json"):
    """Saves the current game state to a JSON file."""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    save_path = os.path.join(SAVE_DIR, filename)

    game_state = {
        "player": {
            "name": player.name,
            "health": player.health,
            "inventory": [item.name for item in player.inventory] # Save item names
        },
        "quests": {
            "active": [quest.id for quest in quest_manager.get_active_quests()], # Save quest IDs
            "completed": [quest.id for quest in quest_manager.get_completed_quests()] # Save quest IDs
        },
        "current_location_id": current_location_id
        # Add other game state variables here as needed (e.g., world state, defeated enemies)
    }

    try:
        with open(save_path, 'w') as f:
            json.dump(game_state, f, indent=4)
        print(f"Game saved to {save_path}")
    except IOError as e:
        print(f"Error saving game: {e}")

def load_game(filename="savegame.json"):
    """Loads the game state from a JSON file."""
    save_path = os.path.join(SAVE_DIR, filename)

    if not os.path.exists(save_path):
        print(f"No save game found at {save_path}")
        return None, None, None # Return None for player, quest_manager, location

    try:
        with open(save_path, 'r') as f:
            game_state = json.load(f)

        # Load player state
        player_state = game_state.get("player", {})
        player = Player(name=player_state.get("name", "Player"), health=player_state.get("health", 100))
        # TODO: Recreate item objects for inventory based on saved names
        # For now, just adding names as strings
        player.inventory = [Item(item_name) for item_name in player_state.get("inventory", [])] # Assuming Item class is accessible

        # Load quest state
        quest_state = game_state.get("quests", {})
        quest_manager = QuestManager()
        quest_manager.load_quests() # Reload all possible quests first
        # Activate saved active quests
        for quest_id in quest_state.get("active", []):
            quest = quest_manager.get_quest_by_id(quest_id)
            if quest:
                quest_manager._active_quests.append(quest) # Directly add to active list for simplicity
        # Mark saved completed quests
        for quest_id in quest_state.get("completed", []):
             quest = quest_manager.get_quest_by_id(quest_id)
             if quest:
                 quest.is_completed = True
                 quest_manager._completed_quests.append(quest) # Directly add to completed list for simplicity

        current_location_id = game_state.get("current_location_id", "downtown")

        print(f"Game loaded from {save_path}")
        return player, quest_manager, current_location_id

    except IOError as e:
        print(f"Error loading game: {e}")
        return None, None, None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {save_path}.")
        return None, None, None
