#!/usr/bin/env python3
from constants import ROOMS
from utils import describe_current_room, solve_puzzle, show_help
from player_actions import move_player, show_inventory, take_item, get_input, use_item

game_state = {
        'player_inventory': [],  # Инвентарь игрока
        'current_room': 'entrance',  # Текущая комната
        'game_over': False,  # Значения окончания игры
        'steps_taken': 0  # Количество шагов
            }

def process_command(game_state, command):
    """Обрабатывает команду пользователя"""
    # Разделяем команду на части
    parts = command.strip().lower().split()
    if not parts:
        return
    
    main_command = parts[0]
    argument = parts[1] if len(parts) > 1 else None
    
    # Обрабатываем команды с помощью match/case
    match main_command:
        case "look":
            describe_current_room(game_state)
            
        case "inventory":
            show_inventory(game_state)
            
        case "go":
            if argument:
                move_player(game_state, argument)
            else:
                print("Укажите направление. Например: 'go north'")
                
        case "take":
            if argument:
                take_item(game_state, argument)
            else:
                print("Укажите название предмета. Например: 'take torch'")
        
        case "solve":
            solve_puzzle(game_state)
            
        case "use":  # ДОБАВЛЕН КЕЙС ДЛЯ КОМАНДЫ use
            if argument:
                use_item(game_state, argument)
            else:
                print("Укажите название предмета. Например: 'use torch'")
        
        case "quit" | "exit":
            print("Спасибо за игру! До свидания!")
            game_state['game_over'] = True
       
        case "help":
            show_help()

        
def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)
    # Основной игровой цикл
    while not game_state['game_over']:
        
        # Считываем команду от пользователя
        command = get_input("\nВведите команду: ")
        
        # Обрабатываем команду
        process_command(game_state, command)


if __name__ == "__main__":
    main()
