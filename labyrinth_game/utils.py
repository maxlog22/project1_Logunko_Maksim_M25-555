import math

from constants import ROOMS

''' Фунция описания комнаты '''
def describe_current_room(game_state):
    # Получаем текущую комнату из game_state
    current_room = game_state["current_room"]
    room = ROOMS[current_room]

    # Выводим название комнаты
    print(f">> {current_room.upper()} <<")

    # Выводим описание комнаты
    print(room["description"])

    # Выводим список видимых предметов
    if room.get("items"):
        print("Заметные предметы:", ", ".join(room["items"]))

    # Выводим доступные выходы
    exits = room.get("exits", {})
    if exits:
        print("Выходы:", ", ".join(exits.keys()))

    # Выводим сообщение о наличии загадки
    if room.get("puzzle"):
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state):
    ''' Функция решения загадок '''
    current_room = game_state["current_room"]
    room = ROOMS[current_room]
    
    # Проверяем, есть ли загадка в текущей комнате
    if not room.get("puzzle"):
        print("Загадок здесь нет.")
        return
    
    # Получаем загадку и правильный ответ
    puzzle_question, correct_answer = room["puzzle"]
    
    # Выводим вопрос загадки
    print("\n>> ЗАГАДКА <<")
    print(puzzle_question)
    
    # Получаем ответ от пользователя
    from player_actions import get_input
    user_answer = get_input("Ваш ответ: ").strip()
    
    # Создаем список допустимых/альтернативных ответов
    valid_answers = [correct_answer.lower()]
    
    # Добавляем альтернативные варианты для числовых ответов
    if correct_answer == "10":
        valid_answers.extend(["десять", "10", "ten"])

    # Сравниваем ответ пользователя с правильным
    if user_answer.lower() == correct_answer.lower():
        print("Правильно! Загадка решена!")
        
        # Убираем загадку из комнаты
        room["puzzle"] = None
        
        # Награда зависит от комнаты
        rewards = {
            "hall": "torch",
            "trap_room": "sword", 
            "library": "skeleton_key",
            "garden": "bronze box",
            "dungeon": "treasure_key"
        }

        # Добавляем награду игроку
        reward = rewards.get(current_room, f"награда_за_{current_room}")
        game_state['player_inventory'].append(reward)
        print(f"Вы получили: {reward}")
        
    else:
        print("Неверно. Попробуйте снова.")
        if current_room == "trap_room":
            print("Ловушка активирована)")
            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    ''' Реализация логики победы '''
    current_room = game_state["current_room"]
    room = ROOMS[current_room]
    
    # Проверка ключа
    if "treasure_key" in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        
        # Удаляем сундук из предметов комнаты
        if "treasure_chest" in room["items"]:
            room["items"].remove("treasure_chest")
        
        # Сообщаем о победе
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return
    
    # Если ключа нет, предлагаем ввести код
    print("Сундук заперт. Без ключа открыть его будет сложно, но можно попробовать взломать код.") # noqa: E501
    from player_actions import get_input
    answer = get_input("Ввести код? (да/нет): ").strip().lower()
    
    if answer == "да":
        # Получаем правильный ответ из загадки
        if room.get("puzzle"):
            _, correct_answer = room["puzzle"]
            user_code = get_input("Введите код: ").strip()
            
            if user_code.lower() == correct_answer.lower():
                print("Код принят! Сундук открывается!")
                
                # Удаляем сундук из предметов комнаты
                if "treasure_chest" in room["items"]:
                    room["items"].remove("treasure_chest")
                
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код. Сундук остается запертым.")
        else:
            print("Невозможно взломать - система защиты слишком сложна.")
    else:
        print("Вы отступаете от сундука.")

def show_help(commands):
    ''' Функция помощи '''
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        # Форматируем вывод
        print(f"  {cmd:<16} - {desc}")

def pseudo_random(seed, modulo):
    ''' Добавляем случайности в игровой процесс '''
    sin_value = math.sin(seed * 12.9898)
    multiplied = sin_value * 43758.5453
    fractional_part = multiplied - math.floor(multiplied)
    result = math.floor(fractional_part * modulo)
    return result

def trigger_trap(game_state):
    ''' Добавляем ловушки в игровую логику '''
    print("Ловушка активирована! Пол стал дрожать...")
    
    player_inventory = game_state['player_inventory']
    
    # Проверяем, есть ли предметы в инвентаре
    if player_inventory:
        # Выбираем случайный предмет для удаления
        items_count = len(player_inventory)
        random_index = pseudo_random(game_state['steps_taken'], items_count)
        lost_item = player_inventory.pop(random_index)
        print(f"Из-за тряски вы потеряли: {lost_item}!")
    else:
        # Инвентарь пуст - игрок получает урон
        damage_chance = pseudo_random(game_state['steps_taken'], 10)

        if damage_chance < 3:
            print("Сильный толчок сбивает вас с ног! Вы ударяетесь головой о камень...")
            print("ВСЁ ПРОПАЛО! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам удается удержаться на ногах! Вы чудом избежали травмы.")

def random_event(game_state):
    ''' Добавляем случайности во время перемещения игрока '''
    # Проверяем, происходит ли событие (10% вероятность)
    if pseudo_random() % 10 == 0:
        # Выбираем тип события
        event_type = pseudo_random() % 3
        
        if event_type == 0:
            # Сценарий 1: Находка
            print("Вы заметили что-то блестящее на полу... Это монетка!")
            current_room = game_state['current_room']
            if 'items' not in game_state['rooms'][current_room]:
                game_state['rooms'][current_room]['items'] = []
            game_state['rooms'][current_room]['items'].append('coin')
            return True
            
        elif event_type == 1:
            # Сценарий 2: Испуг
            print("Вы слышите странный шорох из темноты...")
            if 'sword' in game_state['inventory']:
                print("Благодаря мечу в вашей руке, существо решает не нападать и отступает.") # noqa: E501
            else:
                print("Вам становится не по себе... лучше бы у вас было оружие.")
            return True
            
        elif event_type == 2:
            # Сценарий 3: Срабатывание ловушки
            current_room = game_state['current_room']
            if current_room == 'trap_room' and 'torch' not in game_state['inventory']:
                print("Вы слышите щелчок под ногой! Это ловушка!")
                trigger_trap(game_state)
                return True
            else:
                return False
    
    return False