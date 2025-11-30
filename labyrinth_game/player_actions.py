from constants import ROOMS


def show_inventory(game_state):
    ''' Выводим инвентарь игрока '''
    player_inventory = game_state["player_inventory"]

    # Проверяем, пуст ли инвентарь
    if not player_inventory:
        print("Ваш инвентарь пуст.")
    else:
        print("Инвентарь:")
        for item in player_inventory:
            print(f"  - {item}")


def get_input(prompt="> "):
    ''' Ввод пользователя '''
    try:
        user_input = input(prompt).strip()
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    ''' Функция перемещения '''
    cur_room = game_state["current_room"]
    
    # Проверяем, существует ли выход в этом направлении
    if direction in ROOMS[cur_room]['exits']:
        next_room = ROOMS[cur_room]['exits'][direction]
        
        if next_room != '':
            # Проверяем, является ли следующая комната treasure_room
            if next_room == 'treasure_room':
                # Проверяем наличие ключа в инвентаре
                if 'rusty_key' in game_state['player_inventory']:
                    print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.") # noqa: E501
                    # Обновляем текущую комнату
                    game_state["current_room"] = next_room
                    # Увеличиваем шаг на единицу
                    game_state['steps_taken'] += 1
                    # Выводим описание новой комнаты
                    from utils import describe_current_room
                    describe_current_room(game_state)
                    from utils import random_event
                    random_event(game_state)
                else:
                    print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                    return False
            else:
                # Для всех других комнат - обычное перемещение
                game_state["current_room"] = next_room
                game_state['steps_taken'] += 1
                from utils import describe_current_room
                describe_current_room(game_state)
                from utils import random_event
                random_event(game_state)
        else:
            print("Нельзя пойти в этом направлении.")
            return False
    else:
        print("Нельзя пойти в этом направлении.")
        return False
    
    return True

def take_item(game_state, item_name):
    ''' Функция взятия предмета '''
    cur_room = game_state['current_room']

    # Проверяем, не пытается ли игрок взять сундук
    if item_name.lower() == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return
    
     # Проверяем, есть ли предмет в комнате
    if item_name in ROOMS[cur_room]["items"]:
        # Проверяем, есть ли уже такой предмет в инвентаре
        if item_name in game_state['player_inventory']:
            print(f"У вас уже есть {item_name} в инвентаре!")
        else:
            game_state['player_inventory'].append(item_name)
            ROOMS[cur_room]['items'].remove(item_name)
            print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    ''' Использование предмета из инвентаря '''
    # Проверяем, есть ли предмет у игрока
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return
    
    # Обрабатываем использование конкретных предметов
    match item_name:
        case "torch":
            print("Вы зажигаете факел. Вокруг стало светлее и теплее.")
            
        case "sword":
            print("Вы достаете меч. Чувствуете себя более уверенно и готовы к бою.")
            
        case "bronze_box":
            print("Вы открываете бронзовую шкатулку. Внутри лежит старый ржавый ключ!")
            # Добавляем rusty_key в инвентарь, если его еще нет
            if "rusty_key" not in game_state['player_inventory']:
                game_state['player_inventory'].append("rusty_key")
                print("Вы получили: rusty_key")
            else:
                print("Но у вас уже есть ржавый ключ!")
        case _:
            # Для всех остальных предметов
            print(f"Вы не знаете, как использовать {item_name}.")