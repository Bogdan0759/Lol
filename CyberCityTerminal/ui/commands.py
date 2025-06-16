from ui.interface import print_message
from engine.inventory import Item
from ui.messages import display_random_message

def process_command(command, player, items_data, quest_manager, attempt_hack_func, dialogue_data, current_location_id, save_game_func, load_game_func, faction_manager, lang_manager): # Added lang_manager parameter
    """Processes user commands."""
    command_parts = command.lower().split(maxsplit=2)
    action = command_parts[0]
    arg1 = command_parts[1] if len(command_parts) > 1 else None
    arg2 = command_parts[2] if len(command_parts) > 2 else None

    if action == "quit":
        return False, lang_manager.get_string("exiting_game") # Use lang_manager
    elif action == "status":
        print_message(player, lang_manager) # Pass lang_manager
        return True, None # No additional message needed
    elif action == "inventory":
        player.list_inventory(lang_manager) # Pass lang_manager
        return True, None # No additional message needed
    elif action == "use" and arg1:
        item_name_to_use = arg1.replace(" ", "_") # Simple handling for multi-word items
        used_item = None
        for item in player.inventory:
            if item.name.lower().replace(" ", "_") == item_name_to_use:
                used_item = item
                break

        if used_item:
            item_info = items_data.get(used_item.name.lower().replace(" ", "_")) # Get item data from loaded items
            if item_info and "effect" in item_info:
                effect = item_info["effect"]
                if used_item.type == "consumable":
                    if "heal" in effect:
                        heal_amount = effect["heal"]
                        player.health += heal_amount
                        print_message(lang_manager.get_string("used_item_heal", used_item.name, heal_amount), lang_manager) # Use lang_manager and format
                        player.remove_from_inventory(used_item) # Remove consumable after use
                    # Add other consumable effects here (e.g., damage boost)
                    return True, None
                else:
                    print_message(lang_manager.get_string("cannot_use_item_this_way", used_item.name), lang_manager) # Use lang_manager and format
                    return True, None
            else:
                 print_message(lang_manager.get_string("no_usable_effect", used_item.name), lang_manager) # Use lang_manager and format
                 return True, None
        else:
            print_message(lang_manager.get_string("item_not_in_inventory", arg1), lang_manager) # Use lang_manager and format
            return True, None
    elif action == "quests": # New command to list active quests
        active_quests = quest_manager.get_active_quests()
        if active_quests:
            print_message(lang_manager.get_string("active_quests_label"), lang_manager) # Use lang_manager
            for quest in active_quests:
                print_message(f"- {quest.name}: {quest.description}", lang_manager) # Pass lang_manager
        else:
            print_message(lang_manager.get_string("no_active_quests"), lang_manager) # Use lang_manager
        return True, None
    elif action == "completed_quests": # New command to list completed quests
        completed_quests = quest_manager.get_completed_quests()
        if completed_quests:
            print_message(lang_manager.get_string("completed_quests_label"), lang_manager) # Use lang_manager
            for quest in completed_quests:
                print_message(f"- {quest.name}", lang_manager) # Pass lang_manager
        else:
            print_message(lang_manager.get_string("no_completed_quests"), lang_manager) # Use lang_manager
        return True, None
    elif action == "all_quests": # New command to list all quests
        all_quests = quest_manager._quests.values()
        if all_quests:
            print_message(lang_manager.get_string("all_quests_label"), lang_manager) # Use lang_manager
            for quest in all_quests:
                status = lang_manager.get_string("status_completed") if quest.is_completed else (lang_manager.get_string("status_active") if quest in quest_manager.get_active_quests() else lang_manager.get_string("status_available")) # Use lang_manager
                print_message(f"- {quest.name} [{quest.id}] {status}: {quest.description}", lang_manager) # Pass lang_manager
        else:
            print_message(lang_manager.get_string("no_quests_available"), lang_manager) # Use lang_manager
        return True, None
    elif action == "hack" and arg1:
        try:
            difficulty = int(arg1)
            if difficulty > 0:
                # Perform the hack attempt
                success = attempt_hack_func(difficulty)
                if success:
                    player.record_successful_hack(str(difficulty)) # Record successful hack, using difficulty as identifier
            else:
                print_message(lang_manager.get_string("hack_difficulty_positive"), lang_manager) # Use lang_manager
        except ValueError:
            print_message(lang_manager.get_string("invalid_difficulty"), lang_manager) # Use lang_manager
        return True, None
    elif action == "accept_quest" and arg1: # New command to accept a quest
        quest_id = arg1
        quest_to_start = quest_manager.get_quest_by_id(quest_id)
        if quest_to_start:
            if quest_manager.start_quest(quest_id):
                # Display quest giver intro dialogue
                if "quest_giver_intro" in dialogue_data:
                    display_random_message(dialogue_data["quest_giver_intro"], lang_manager) # Pass lang_manager
                return True, lang_manager.get_string("quest_accepted", quest_to_start.name) # Use lang_manager and format
            else:
                 return True, lang_manager.get_string("quest_already_active_completed", quest_id) # Use lang_manager and format
        else:
            return True, lang_manager.get_string("quest_not_found", quest_id) # Use lang_manager and format
    elif action == "quest_details" and arg1: # New command to view quest details
        quest_id = arg1
        quest = quest_manager.get_quest_by_id(quest_id)
        if quest:
            print_message(lang_manager.get_string("quest_details_label", quest.name), lang_manager) # Use lang_manager and format
            print_message(lang_manager.get_string("description_label", quest.description), lang_manager) # Use lang_manager and format
            print_message(lang_manager.get_string("objectives_label"), lang_manager) # Use lang_manager
            if quest.objectives:
                for obj_type, obj_details in quest.objectives.items():
                    print_message(f"- {obj_type.capitalize()}:", lang_manager) # Pass lang_manager
                    for detail_key, detail_value in obj_details.items():
                         print_message(f"  {detail_key.replace('_', ' ').capitalize()}: {detail_value}", lang_manager) # Pass lang_manager
            else:
                print_message(lang_manager.get_string("no_objectives_listed"), lang_manager) # Use lang_manager
            status = lang_manager.get_string("status_completed") if quest.is_completed else (lang_manager.get_string("status_active") if quest in quest_manager.get_active_quests() else lang_manager.get_string("status_available")) # Use lang_manager
            print_message(lang_manager.get_string("status_label", status), lang_manager) # Use lang_manager and format

            # Display available choices if any and not yet resolved
            if quest.choices:
                print_message(lang_manager.get_string("choices_label"), lang_manager) # Use lang_manager
                for choice_id, choice_info in quest.choices.items():
                    if choice_id not in quest.resolved_choices:
                        print_message(f"- [{choice_id}] {choice_info.get('description', '')}", lang_manager) # Pass lang_manager
                        for i, option in enumerate(choice_info.get("options", [])):
                            print_message(f"  {i + 1}. {option.get('text', '')}", lang_manager) # Pass lang_manager
        else:
            print_message(lang_manager.get_string("quest_not_found", quest_id), lang_manager) # Use lang_manager and format
        return True, None
    elif action == "start_quest_test" and arg1: # Command to manually start a quest for testing
        quest_id = arg1
        if quest_manager.start_quest(quest_id):
             return True, lang_manager.get_string("manually_started_quest", quest_id) # Use lang_manager and format
        else:
             return True, lang_manager.get_string("could_not_manually_start_quest", quest_id) # Use lang_manager and format
    elif action == "save": # New command to save the game
        save_game_func(player, quest_manager, current_location_id)
        return True, None
    elif action == "load": # New command to load the game
        # Note: Loading will restart the main loop with loaded data
        print_message(lang_manager.get_string("loading_game"), lang_manager) # Use lang_manager
        return False, "load"
    elif action == "make_choice" and arg1 and arg2: # New command to make a quest choice
        quest_id = arg1
        choice_id = arg2
        option_number = None
        try:
            # Expecting option number as the third part of the command
            command_parts = command.lower().split(maxsplit=3)
            if len(command_parts) > 3:
                 option_number = int(command_parts[3])
            else:
                 print_message(lang_manager.get_string("specify_option_number"), lang_manager) # Use lang_manager
                 return True, None
        except ValueError:
            print_message(lang_manager.get_string("invalid_option_number"), lang_manager) # Use lang_manager
            return True, None

        quest = quest_manager.get_quest_by_id(quest_id)
        if quest:
            if choice_id in quest.choices:
                options = quest.choices[choice_id].get("options", [])
                if 1 <= option_number <= len(options):
                    # Call the apply_choice_consequences method
                    success = quest_manager.apply_choice_consequences(player, quest_id, choice_id, option_number - 1) # Adjust for 0-based index
                    if success:
                        return True, lang_manager.get_string("chose_option", option_number, choice_id, quest.name) # Use lang_manager and format
                    else:
                         return True, lang_manager.get_string("could_not_apply_consequences", option_number) # Use lang_manager and format
                else:
                    print_message(lang_manager.get_string("invalid_option_number_for_choice", choice_id), lang_manager) # Use lang_manager and format
            else:
                print_message(lang_manager.get_string("choice_id_not_found", choice_id, quest.name), lang_manager) # Use lang_manager and format
        else:
            print_message(lang_manager.get_string("quest_not_found", quest_id), lang_manager) # Use lang_manager and format
        return True, None
    elif action == "russia": # New command to switch language to Russian
        if lang_manager.load_language("russian"):
            # Use lang_manager.get_string for the success message
            return True, lang_manager.get_string("language_set_to_russian")
        else:
            # Use lang_manager.get_string for the failure message
            return True, lang_manager.get_string("language_switch_failed")
    # Add other commands here later
    else:
        return True, lang_manager.get_string("unknown_command", command) # Use lang_manager and format
