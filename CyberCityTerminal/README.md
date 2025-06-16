# Cyber City Terminal RPG

A text-based terminal RPG set in a cyberpunk future.

## Concept

Navigate the neon-drenched streets of Cyber City, interact with various factions, take on dangerous quests, and hone your skills in hacking and combat.

## Концепция

Перемещайтесь по залитым неоновым светом улицам Кибергорода, взаимодействуйте с различными фракциями, выполняйте опасные квесты и оттачивайте свои навыки взлома и боя.

## How to Play

1.  Make sure you have Python installed.
2.  Navigate to the game directory in your terminal.
3.  Install dependencies (if any, based on `requirements.txt`).
4.  Run the game using `python main.py`.
5.  Follow the on-screen prompts and type commands to interact with the game world.

## Как играть

1. Убедитесь, что у вас установлен Python.
2. Перейдите в директорию игры в вашем терминале.
3. Установите зависимости (если есть, на основе `requirements.txt`).
4. Запустите игру с помощью `python main.py`.
5. Следуйте инструкциям на экране и вводите команды для взаимодействия с игровым миром.

## Commands

*   **Movement:** `north`, `south`, `east`, `west` - Move between locations.
*   **status:** View your player's health, stats, and faction reputation.
*   **inventory:** List items in your inventory.
*   **use [item_name]:** Use an item from your inventory (e.g., `use medkit`).
*   **quests:** List your active quests.
*   **completed_quests:** List quests you have completed.
*   **all_quests:** List all available quests.
*   **quest_details [quest_id]:** View details of a specific quest, including objectives and choices.
*   **accept_quest [quest_id]:** Accept an available quest.
*   **make_choice [quest_id] [choice_id] [option_number]:** Make a choice for a quest (e.g., `make_choice retrieve_data_chip approach_office 1`).
*   **hack [difficulty]:** Attempt a hacking mini-game with a given difficulty.
*   **save:** Save your current game progress.
*   **load:** Load a saved game.
*   **quit:** Exit the game.

## Команды

*   **Movement:** `north`, `south`, `east`, `west` - Перемещение между локациями.
*   **status:** Просмотр здоровья, характеристик игрока и репутации фракций.
*   **inventory:** Список предметов в вашем инвентаре.
*   **use [название_предмета]:** Использовать предмет из инвентаря (например, `use medkit`).
*   **quests:** Список ваших активных квестов.
*   **completed_quests:** Список выполненных вами квестов.
*   **all_quests:** Список всех доступных квестов.
*   **quest_details [id_квеста]:** Просмотр деталей конкретного квеста, включая цели и выборы.
*   **accept_quest [id_квеста]:** Принять доступный квест.
*   **make_choice [id_квеста] [id_выбора] [номер_варианта]:** Сделать выбор для квеста (например, `make_choice retrieve_data_chip approach_office 1`).
*   **hack [сложность]:** Попытка взлома с заданной сложностью.
*   **save:** Сохранить текущий прогресс игры.
*   **load:** Загрузить сохраненную игру.
*   **quit:** Выйти из игры.

## Features Implemented (So Far)

*   Basic game loop and command processing.
*   World exploration with different locations.
*   Player stats, inventory, and faction reputation tracking.
*   Item usage (healing).
*   Basic combat encounters.
*   Quest system with objectives (collect, visit, hack_success).
*   Quests with branching choices and consequences (reputation changes, skill checks).
*   Saving and loading game progress.
*   Basic dialogue and messages.

## Future Plans

*   Expand questlines and add more complex narratives.
*   Implement quest rewards (items, credits, skill points).
*   Develop more interactive hacking mini-games.
*   Add NPCs and dialogue options based on reputation and skills.
*   Introduce a currency system.
*   Enhance combat with more options and enemy types.
*   Add ASCII art for atmosphere and events.
