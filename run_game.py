"""
This module contains logic of game and it run the game
"""

from pseudo_random import p_rand
from json import dump
from random import randint
from units import Army
from units_consts import *
from specfuncs import get_random_strategy_name


class Game:
    def run_game(self):
        seed = randint(0, 100)
        p_rand.seed(seed)

        print('The game is starting!',
              f'Seed number: {seed}', sep='\n')

        # player_count = int(input('Enter player count(from 2 to 10): '))
        player_count = 3
        p_rand.shuffle(COUNTRY_NAMES)
        warring_armies = [Army(country=COUNTRY_NAMES[i],
                               strategy_name=get_random_strategy_name())
                          for i in range(player_count)]

        self._write_config(seed, warring_armies)

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
                    chosen_enemy_army = p_rand.choice(enemy_armies)
                    army.attack(chosen_enemy_army)

                    if not chosen_enemy_army.is_active:
                        warring_armies.remove(chosen_enemy_army)

            print('Total moves:', move_counter)
            print('Winner:', warring_armies[0])

    def _prepare_armies(self):
        pass  # clear up!!!!


    def _write_config(self, seed, warring_armies_lst):
        structure = {
            'seed': seed,
            'constants': {
                'squad_count': SQUAD_COUNT,
                'soldier_count': SOLDIER_COUNT,
                'vehicle_count': VEHICLE_COUNT,
                'operator_count': OPERATOR_COUNT,
                'vehicle_recharge_ms': VEHICLE_RECHARGE_MS,
                'soldier_recharge_ms': SOLDIER_RECHARGE_MS,
                'soldier_exp': SOLDIER_EXP,
                'soldier_hp': SOLDIER_HP,
                'vehicle_hp': VEHICLE_HP,
            },
            'armies': [
                {
                    'name': army.country,
                    'strategy_name': army.strategy_name,

                } for army in warring_armies_lst
            ],
        }

        with open('config.json', 'w') as json_file:
            dump(structure, json_file)


if __name__ == '__main__':
    game = Game()
    game.run_game()



