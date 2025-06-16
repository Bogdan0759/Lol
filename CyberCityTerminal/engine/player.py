class Player:
    def __init__(self, name="Player", health=100):
        self.name = name
        self.health = health
        self.inventory = [] # Using a list for simplicity initially
        self.stats = {"hacking": 1, "combat": 2, "charisma": 0} # Added stats
        self.factions = {"Syndicate": 0, "CyberNuns": 0, "NeoPolice": 0} # Added factions
        self.visited_locations = set() # Added to track visited locations
        self.successful_hacks = set() # Added to track successful hacks (e.g., by difficulty or target ID)

    def __str__(self):
        inventory_summary = ", ".join([item.name for item in self.inventory]) if self.inventory else "Empty"
        stats_summary = ", ".join([f"{stat}: {level}" for stat, level in self.stats.items()])
        factions_summary = ", ".join([f"{faction}: {rep}" for faction, rep in self.factions.items()])
        return f"{self.name} (Health: {self.health})\nStats: {stats_summary}\nFactions: {factions_summary}\nInventory: {inventory_summary}"

    def add_to_inventory(self, item):
        self.inventory.append(item)
        print(f"{item} added to inventory.")

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"{item} removed from inventory.")
        else:
            print(f"{item} not found in inventory.")

    def list_inventory(self):
        if not self.inventory:
            print("Inventory is empty.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"- {item}")

    def visit_location(self, location_id):
        """Marks a location as visited."""
        self.visited_locations.add(location_id)

    def record_successful_hack(self, hack_identifier):
        """Records a successful hack."""
        self.successful_hacks.add(hack_identifier)
