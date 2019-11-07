from pseudo_random import p_rand
from specfuncs import get_random_strategy_name
from random import randint, shuffle, choice
from json_listener import JsonListener
from units import Army, Squad, Soldier, Vehicle
from units_configuration import *


class Game:
    def __init__(self, armies):
        self.armies = armies

    def run_game(self):
        for army in self.armies:
            print(f'Army of {army.country} joined the game... Commander of army chose the strategy -> '
                  f'({army.strategy_name})')

        move_counter = 0
        while len([army for army in self.armies if army.is_active]) != 1:
            move_counter += 1
            print('Move:', move_counter)
            for attacking_army in [army for army in self.armies if army.is_active]:
                enemy_armies = [army for army in self.armies if army.is_active and army is not attacking_army]
                chosen_enemy_army = p_rand.choice(enemy_armies)
                attacking_army.attack(chosen_enemy_army)

        print('Total moves:', move_counter)
        winner = [army for army in self.armies if army.is_active][0]
        print('Winner:', winner)

    @classmethod
    def load_json_structure(cls):
        structure = JsonListener.load_structure()
        seed = structure['seed']
        p_rand.seed(seed)

        armies = list()
        for army in structure['armies']:
            army_data = army

            armies.append(
                cls.create_army(
                    country=army_data['country'],
                    strategy_name=army_data['strategy'],
                    squads_data=army_data['squads'],
                )
            )

        return cls(armies)

    @classmethod
    def create_new_structure(cls):
        rand_seed = randint(0, 1000)
        p_rand.seed(rand_seed)
        country_names = COUNTRY_NAMES.copy()
        shuffle(country_names)

        armies = list()

        army_count = randint(MIN_ARMY_COUNT, MAX_ARMY_COUNT)
        for i in range(army_count):
            armies.append(
                cls.create_army(
                    country=country_names[i],
                    strategy_name=get_random_strategy_name(),
                )
            )

        JsonListener.dump_structure(seed=rand_seed, armies_lst=armies)

        return cls(armies)

    @classmethod
    def create_soldier(cls):
        soldier = Soldier()
        return soldier

    @classmethod
    def create_vehicle(cls, operator_count=None):
        operators = list()

        if operator_count is not None:
            operator_count = operator_count
            for _ in range(operator_count):
                operators.append(cls.create_soldier())
        else:
            operator_count = randint(MIN_OPERATOR_COUNT, MAX_OPERATOR_COUNT)
            for _ in range(operator_count):
                operators.append(cls.create_soldier())

        vehicle = Vehicle(operators_lst=operators)

        return vehicle

    @classmethod
    def create_squad(cls, units_data=None):
        units = list()

        if units_data is not None:
            for unit in units_data:
                if unit['type'] == 'Soldier':
                    units.append(cls.create_soldier())
                elif unit['type'] == 'Vehicle':
                    units.append(cls.create_vehicle(len(unit['operators'])))
        else:
            unit_count = randint(MIN_UNIT_COUNT, MAX_UNIT_COUNT)
            for _ in range(unit_count):
                unit = choice([cls.create_soldier, cls.create_vehicle])()
                units.append(unit)

        squad = Squad(units_lst=units)

        return squad

    @classmethod
    def create_army(cls, country, strategy_name, squads_data=None):
        squads = list()

        if squads_data is not None:
            for squad in squads_data:
                squad_data = squad
                squads.append(
                    cls.create_squad(squad_data['units'])
                )
        else:
            squad_count = randint(MIN_SQUAD_COUNT, MAX_SQUAD_COUNT)
            for squad in range(squad_count):
                squads.append(
                    cls.create_squad()
                )

        army = Army(
            country=country,
            strategy_name=strategy_name,
            squads_lst=squads,
        )
        return army
