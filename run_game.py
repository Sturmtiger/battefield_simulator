"""
This module contains logic of game and it run the game
"""

from random import shuffle, choice
from units import Army
from units_consts import STRATEGIES


print('The game is starting!',
      'You can attack: ')
for n, strategy_name in enumerate(STRATEGIES, 1):
    print(f'\t{n}. {strategy_name} squad')
STRATEGY_NUM = int(input('Choose your strategy number: ')) - 1

PLAYER_STRATEGY = STRATEGIES[STRATEGY_NUM]
print(f'You have chosen: attack {PLAYER_STRATEGY} squad')
ENEMY_STRATEGY = choice(STRATEGIES)
print(f'Enemy has chosen: attack {ENEMY_STRATEGY} squad')

PLAYER_ARMY = Army(strategy=PLAYER_STRATEGY)
ENEMY_ARMY = Army(strategy=ENEMY_STRATEGY)
WARRING_ARMIES = [PLAYER_ARMY, ENEMY_ARMY]
shuffle(WARRING_ARMIES)

move_counter = 0

while PLAYER_ARMY.is_active and ENEMY_ARMY.is_active:
    move_counter += 1
    WARRING_ARMIES[0].attack(WARRING_ARMIES[1])
    WARRING_ARMIES[1].attack(WARRING_ARMIES[0])

if PLAYER_ARMY.is_active:
    print('Your Army has Won!')
else:
    print('Enemy Army has Won!')

print('Total moves:', move_counter)
# input('Press Enter to close..')
