from constants import ROOMS

def describe_current_room(game_state):
    # Получаем текущую комнату из game_state
    current_room_id = game_state["current_room"]
    room = ROOMS[current_room_id]

    # Название комнаты в верхнем регистре
    print(f"== {current_room_id.upper()} ==")

    # Описание комнаты
    print(room["description"])

    # Список видимых предметов
    if room.get("items"):
        print("Заметные предметы:", ", ".join(room["items"]))

    # Доступные выходы
    exits = room.get("exits", {})
    if exits:
        print("Выходы:", ", ".join(exits.keys()))

    # Сообщение о наличии загадки
    if room.get("puzzle"):
        print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
    """Функция решения загадок в текущей комнате"""
    current_room_id = game_state["current_room"]
    room = ROOMS[current_room_id]
    
    # Проверяем, есть ли загадка в текущей комнате
    if not room.get("puzzle"):
        print("Загадок здесь нет.")
        return
    
    # Получаем загадку и правильный ответ
    puzzle_question, correct_answer = room["puzzle"]
    
    # Выводим вопрос загадки
    print("\n=== ЗАГАДКА ===")
    print(puzzle_question)
    
    # Получаем ответ от пользователя
    from player_actions import get_input
    user_answer = get_input("Ваш ответ: ").strip()
    
    # Сравниваем ответ пользователя с правильным
    if user_answer.lower() == correct_answer.lower():
        print("Правильно! Загадка решена!")
        
        # Убираем загадку из комнаты
        room["puzzle"] = None
        
        # Добавляем награду игроку (можно настроить для каждой комнаты)
        reward = f"награда_за_{current_room_id}"
        game_state['player_inventory'].append(reward)
        print(f"Вы получили: {reward}")
        
    else:
        print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):
    """Попытка открыть сундук с сокровищами"""
    current_room_id = game_state["current_room"]
    room = ROOMS[current_room_id]
    
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
    print("Сундук заперт. Без ключа открыть его будет сложно, но можно попробовать взломать код.")
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


def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
