import json
import os # Import the os module

class Quest:
    def __init__(self, id, name, description, objectives, reward, choices=None):
        self.id = id
        self.name = name
        self.description = description
        self.objectives = objectives # e.g., {"kill": {"enemy_type": "robot", "count": 5}, "collect": {"item_name": "data_chip", "count": 1}, "visit": {"location_id": 1}, "hack_success": {"difficulty": 5}}
        self.reward = reward # e.g., {"item": "credits", "amount": 100}
        self.choices = choices if choices is not None else {} # Added choices attribute
        self.is_completed = False
        self.resolved_choices = set() # Added to track resolved choice points

    def __str__(self):
        status = "(Completed)" if self.is_completed else "(Active)"
        return f"{self.name} {status}"

    def check_completion(self, player): # Accept player object
        """Checks if the quest objectives are met based on player state."""
        if self.is_completed:
            return True # Already completed

        all_objectives_met = True

        # Check 'collect' objectives
        if "collect" in self.objectives:
            for item_name, count in self.objectives["collect"].items():
                # Check if player has enough of the required item in inventory
                item_count_in_inventory = sum(1 for item in player.inventory if item.name.lower() == item_name.lower())
                if item_count_in_inventory < count:
                    all_objectives_met = False
                    break # No need to check other collect objectives if one is not met

        # Check 'visit' objectives
        if all_objectives_met and "visit" in self.objectives:
            for location_id in self.objectives["visit"]:
                if location_id not in player.visited_locations:
                    all_objectives_met = False
                    break # No need to check other visit objectives if one is not met

        # Check 'hack_success' objectives
        if all_objectives_met and "hack_success" in self.objectives:
            for hack_identifier, required_count in self.objectives["hack_success"].items():
                 # Assuming hack_identifier could be difficulty or a specific target ID
                 # For now, let's assume hack_identifier is the difficulty level as a string
                 successful_hack_count = sum(1 for hack in player.successful_hacks if str(hack) == hack_identifier)
                 if successful_hack_count < required_count:
                     all_objectives_met = False
                     break

        # TODO: Add checks for other objective types (kill, etc.)

        if all_objectives_met:
            self.is_completed = True
            return True
        else:
            return False

class QuestManager:
    def __init__(self):
        self._quests = {}
        self._active_quests = []
        self._completed_quests = []

    # Get the absolute path of the script's directory
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data") # data is one level up from engine

    def load_quests(self, filepath="quests.json"):
        """Loads quest data from a JSON file."""
        # Construct the full path to the data file
        full_filepath = os.path.join(self.DATA_DIR, filepath)
        try:
            with open(full_filepath, 'r') as f:
                quests_data = json.load(f)
                for quest_id, data in quests_data.items():
                    # Pass choices data to Quest constructor
                    self._quests[quest_id] = Quest(quest_id, data["name"], data["description"], data.get("objectives", {}), data.get("reward", {}), data.get("choices", {}))
            print("Quests loaded successfully.")
        except FileNotFoundError:
            print(f"Error: {full_filepath} not found.")
            self._quests = {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {full_filepath}.")
            self._quests = {}

    def start_quest(self, quest_id):
        """Adds a quest to the active quests list."""
        if quest_id in self._quests and self._quests[quest_id] not in self._active_quests and self._quests[quest_id] not in self._completed_quests:
            self._active_quests.append(self._quests[quest_id])
            print(f"Quest started: {self._quests[quest_id].name}")
            return True
        elif quest_id not in self._quests:
            print(f"Quest with ID {quest_id} not found.")
            return False
        else:
            print(f"Quest {self._quests[quest_id].name} is already active or completed.")
            return False

    def complete_quest(self, quest_id):
        """Marks a quest as completed and moves it from active to completed."""
        for quest in self._active_quests:
            if quest.id == quest_id:
                quest.is_completed = True
                self._active_quests.remove(quest)
                self._completed_quests.append(quest)
                print(f"Quest completed: {quest.name}")
                # TODO: Implement reward distribution
                return True
        print(f"Quest with ID {quest_id} not found in active quests.")
        return False

    def check_active_quests_completion(self, player):
        """Checks if any active quests are completed and moves them."""
        completed_now = []
        for quest in list(self._active_quests): # Iterate over a copy in case list is modified
            if quest.check_completion(player):
                completed_now.append(quest.id)

        for quest_id in completed_now:
            self.complete_quest(quest_id) # Use the complete_quest method to handle moving and potential rewards

        return completed_now

    def get_active_quests(self):
        """Returns a list of active quests."""
        return self._active_quests

    def get_completed_quests(self):
        """Returns a list of completed quests."""
        return self._completed_quests

    def get_quest_by_id(self, quest_id):
        """Returns a quest object by its ID."""
        return self._quests.get(quest_id)

    def get_quest_by_name(self, quest_name):
        """Returns a quest object by its name (case-insensitive)."""
        for quest in self._quests.values():
            if quest.name.lower() == quest_name.lower():
                return quest
        return None

    def apply_choice_consequences(self, player, quest_id, choice_id, option_index):
        """Applies the consequences of a chosen quest option."""
        quest = self.get_quest_by_id(quest_id)
        if not quest or choice_id not in quest.choices:
            print("Error: Invalid quest or choice.")
            return False

        choice_point = quest.choices[choice_id]
        options = choice_point.get("options", [])

        if not (0 <= option_index < len(options)):
            print("Error: Invalid choice option index.")
            return False

        chosen_option = options[option_index]
        consequences = chosen_option.get("consequences", {})
        skill_check = chosen_option.get("skill_check")

        # Perform skill check if required
        if skill_check:
            skill_name = skill_check.get("skill")
            required_level = skill_check.get("level", 0)
            player_skill_level = player.stats.get(skill_name, 0)

            if player_skill_level < required_level:
                print(f"Skill check failed: Requires {skill_name} level {required_level}, you have {player_skill_level}.")
                # TODO: Handle consequences of failed skill check (e.g., different outcome, combat)
                # For now, let's just not apply the success consequences
                return False # Indicate skill check failed
            else:
                print(f"Skill check successful: {skill_name} level {player_skill_level} meets requirement of {required_level}.")

        # Apply reputation changes
        if "reputation" in consequences:
            for faction, change in consequences["reputation"].items():
                if faction in player.factions:
                    player.factions[faction] += change
                    print(f"Your reputation with {faction} changed by {change}.")
                else:
                    print(f"Warning: Unknown faction '{faction}' in consequences.")

        # TODO: Handle other consequences (e.g., gaining items, starting combat, moving to next quest step)
        if "next_step" in consequences:
            next_step_id = consequences["next_step"]
            print(f"Proceeding to next quest step: {next_step_id}")
            # This would require more complex quest state management
            # For now, we'll just print the next step ID

        quest.resolved_choices.add(choice_id) # Mark this choice point as resolved
        return True # Indicate consequences were applied (or skill check passed)
