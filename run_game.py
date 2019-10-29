from units import *
from random import shuffle
from units_consts import STRATEGIES

print('The game is starting!',
      'You can attack: ')
for n, strategy_name in enumerate(STRATEGIES, 1):
    print(f'\t{n}. {strategy_name} squad')
strategy_num = int(input('Choose your strategy number: '))-1

player_strategy = STRATEGIES[strategy_num]
print(f'You have chosen: attack {player_strategy} squad')
enemy_strategy = choice(STRATEGIES)
print(f'Enemy has chosen: attack {enemy_strategy} squad')

player_army = Army(strategy=player_strategy)
enemy_army = Army(strategy=enemy_strategy)
warring_armies = [player_army, enemy_army]
shuffle(warring_armies)

while player_army.is_active and enemy_army.is_active:
    warring_armies[0].attack(warring_armies[1])
    warring_armies[1].attack(warring_armies[0])

if player_army.is_active:
    print('Your Army has Won!')
else:
    print('Enemy Army has Won!')

input('Press Enter to close..')
