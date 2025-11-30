#!/usr/bin/env python3
from constants import COMMANDS
from player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from utils import describe_current_room, show_help, solve_puzzle

'''Определение текущего состояния игрока'''
game_state = {
        'player_inventory': [],  # Инвентарь игрока
        'current_room': 'entrance',  # Текущая комната
        'game_over': False,  # Значения окончания игры
        'steps_taken': 0  # Количество шагов
            }


def process_command(game_state, command):
    ''' Обрабатывает команду пользователя '''
    parts = command.strip().lower().split()
    if not parts:
        return
    
    main_command = parts[0]
    argument = parts[1] if len(parts) > 1 else None
    
    directions = {"north", "south", "east", "west", "up", "down"} 
    match main_command:
        case "look":
            describe_current_room(game_state)
            
        case "inventory":
            show_inventory(game_state)
                          
        case "take":
            if argument:
                take_item(game_state, argument)
            else:
                print("Укажите название предмета. Например: 'take torch'")
        
        case "solve":
            if game_state["current_room"] == "treasure_room":
                from utils import attempt_open_treasure
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
            
        case "use": 
            if argument:
                use_item(game_state, argument)
            else:
                print("Укажите название предмета. Например: 'use torch'")
        
        case "quit":
            print("Спасибо за игру! До свидания!")
            game_state['game_over'] = True
       
        case "help":
            show_help(COMMANDS)

        case c if c in directions:
            # Если ввод только одно слово-направление
            move_player(game_state, c)
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")

       
def main():
    ''' Основной игровой цикл ''' 
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)
    while not game_state['game_over']:
        command = get_input("\nВведите команду: ")
        process_command(game_state, command)

if __name__ == "__main__":
    main()