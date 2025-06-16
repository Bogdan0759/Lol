import random

def attempt_hack(difficulty):
    """Simulates a hacking attempt with a given difficulty."""
    # Basic hacking success chance based on difficulty
    # Higher difficulty means lower chance of success
    success_chance = 100 - (difficulty * 10)

    if random.randint(1, 100) <= success_chance:
        print("Hacking successful!")
        return True
    else:
        print("Hacking failed.")
        return False

# You can add more complex hacking mechanics here later,
# like minigames, different types of hacks, etc.
