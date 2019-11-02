"""
This module contains logic of game and it run the game
"""
from random import shuffle, choice
from units import Army
from units_consts import STRATEGIES, COUNTRY_NAMES


print('The game is starting!')

player_count = int(input('Enter player count(from 2 to 10): '))
shuffle(COUNTRY_NAMES)
warring_armies = [Army(country=COUNTRY_NAMES[i], strategy=choice(STRATEGIES)) for i in range(player_count)]

for army in warring_armies:
    print(f'Army of {army.country} joined the game... Commander of army chose the strategy -> ({army.strategy})')


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








# from random import shuffle, choice
# from units import Army
# from units_consts import STRATEGIES
#
#
# print('The game is starting!',
#       'You can attack: ')
# for n, strategy_name in enumerate(STRATEGIES, 1):
#     print(f'\t{n}. {strategy_name} squad')
# # STRATEGY_NUM = int(input('Choose your strategy number: ')) - 1
#
# # PLAYER_STRATEGY = STRATEGIES[STRATEGY_NUM]
# PLAYER_STRATEGY = 'strongest'
# print(f'You have chosen: attack {PLAYER_STRATEGY} squad')
# # ENEMY_STRATEGY = choice(STRATEGIES)
# ENEMY_STRATEGY = 'strongest'
# print(f'Enemy has chosen: attack {ENEMY_STRATEGY} squad')
#
# PLAYER_ARMY = Army(strategy=PLAYER_STRATEGY)
# ENEMY_ARMY = Army(strategy=ENEMY_STRATEGY)
# WARRING_ARMIES = [PLAYER_ARMY, ENEMY_ARMY]
# shuffle(WARRING_ARMIES)
#
# move_counter = 0
#
# while PLAYER_ARMY.is_active and ENEMY_ARMY.is_active:
#     move_counter += 1
#     print(f'Move: {move_counter}')
#     WARRING_ARMIES[0].attack(WARRING_ARMIES[1])
#     WARRING_ARMIES[1].attack(WARRING_ARMIES[0])
#
# if PLAYER_ARMY.is_active:
#     print('Your Army has Won!')
# else:
#     print('Enemy Army has Won!')
#
# print('Total moves:', move_counter)
# # input('Press Enter to close..')