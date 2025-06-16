import random
from .player import Player
from .inventory import Item # Import Item class

class Enemy:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.damage = damage

    def __str__(self):
        return f"{self.name} (Health: {self.health})"

def start_combat(player: Player, enemy: Enemy, items_data, dialogue_data): # Added items_data and dialogue_data parameters
    print(f"\nA wild {enemy.name} appears!")
    # Add combat start dialogue
    if "combat_start" in dialogue_data:
        # Assuming dialogue_data["combat_start"] is a list of strings
        print(random.choice(dialogue_data["combat_start"]))
    else:
         print("Starting combat...")

    while player.health > 0 and enemy.health > 0:
        print(f"\n{player.name} Health: {player.health}")
        print(f"{enemy.name} Health: {enemy.health}")

        # Player turn
        player_action = input("Choose your action (attack, use [item_name], quit): ").lower().strip()

        if player_action == "attack":
            player_damage = random.randint(10, 20) # Basic random damage
            enemy.health -= player_damage
            print(f"{player.name} attacks {enemy.name} for {player_damage} damage.")
        elif player_action.startswith("use "):
            item_name_to_use = player_action[4:].strip().replace(" ", "_")
            used_item = None
            for item in player.inventory:
                if item.name.lower().replace(" ", "_") == item_name_to_use:
                    used_item = item
                    break

            if used_item:
                item_info = items_data.get(used_item.name.lower().replace(" ", "_"))
                if item_info and "effect" in item_info:
                    effect = item_info["effect"]
                    if used_item.type == "consumable":
                        if "heal" in effect:
                            heal_amount = effect["heal"]
                            player.health += heal_amount
                            print(f"Used {used_item.name}. Healed for {heal_amount} health.")
                            player.remove_from_inventory(used_item) # Remove consumable after use
                        # Add other consumable effects here (e.g., damage boost)
                    else:
                        print("You can't use that item in combat.")
                else:
                     print(f"No usable effect found for {used_item.name}.")
            else:
                print(f"You don't have a {item_name_to_use.replace('_', ' ')} in your inventory.")

        elif player_action == "quit":
            print("Attempting to flee...")
            # Simple flee chance
            if random.random() < 0.5: # 50% chance to flee
                print("Successfully fled from combat.")
                return True # Fleeing counts as not losing
            else:
                print("Failed to flee!")
                continue # Enemy still attacks

        else:
            print("Invalid action.")
            continue # Skip enemy turn if action is invalid

        if enemy.health <= 0:
            print(f"{enemy.name} defeated!")
            # Add combat win dialogue
            if "combat_win" in dialogue_data:
                 print(random.choice(dialogue_data["combat_win"]))
            return True # Player wins

        # Enemy turn
        enemy_damage = random.randint(5, enemy.damage)
        player.health -= enemy_damage
        print(f"{enemy.name} attacks {player.name} for {enemy_damage} damage.")

        if player.health <= 0:
            print(f"{player.name} has been defeated...")
            # Add combat lose dialogue
            if "combat_lose" in dialogue_data:
                 print(random.choice(dialogue_data["combat_lose"]))
            return False # Player loses

    return False # Should not reach here in a normal combat flow
