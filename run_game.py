"""
This module contains logic of game and it run the game
"""
from random import shuffle, choice
from units import Army
from units_consts import COUNTRY_NAMES
from specfuncs import get_random_strategy_name


if __name__ == '__main__':
    print('The game is starting!')

    player_count = int(input('Enter player count(from 2 to 10): '))
    # player_count = 3
    shuffle(COUNTRY_NAMES)
    warring_armies = [Army(country=COUNTRY_NAMES[i],
                           strategy_name=get_random_strategy_name())
                      for i in range(player_count)]

    for army in warring_armies:
        print(f'Army of {army.country} joined the game... Commander of army chose the strategy -> '
              f'({army.strategy_name})')

    move_counter = 0

    while len(warring_armies) != 1:
        move_counter += 1
        print('Move:', move_counter)
        for army in [army for army in warring_armies if army.is_active]:
            if not army.is_active:
                continue
            enemy_armies = [army for army in warring_armies if army.is_active]
            enemy_armies.remove(army)
            chosen_enemy_army = choice(enemy_armies)
            army.attack(chosen_enemy_army)

            if not chosen_enemy_army.is_active:
                warring_armies.remove(chosen_enemy_army)

    print('Total moves:', move_counter)
    print('Winner:', warring_armies[0])
