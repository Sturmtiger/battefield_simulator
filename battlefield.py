"""This module consists of army create structures and game logic"""

from random import randint, shuffle, choice
from pseudo_random import PSEUDO_RAND
from specfuncs import get_random_strategy_name
from json_listener import JsonListener
from units import Army, Squad, Soldier, Vehicle
import units_configuration as u_conf


class Game:
    """This class creates army structure and may run a game (war between armies)"""

    def __init__(self, armies):
        self.armies = armies

    def run_game(self):
        """This method runs game"""
        for army in self.armies:
            print(f'Army of {army.country} joined the game...'
                  f' Commander of army chose the strategy -> ({army.strategy_name})')

        move_counter = 0
        while len([army for army in self.armies if army.is_active]) != 1:
            move_counter += 1
            print('Move:', move_counter)
            for attacking_army in [army for army in self.armies if army.is_active]:
                enemy_armies = [army for army in self.armies
                                if army.is_active and army is not attacking_army]
                chosen_enemy_army = PSEUDO_RAND.choice(enemy_armies)
                attacking_army.attack(chosen_enemy_army)

        print('Total moves:', move_counter)
        winner = [army for army in self.armies if army.is_active][0]
        print('Winner:', winner)

    @classmethod
    def create_from_json_structure(cls):
        """This method create armies structure from JSON config file
        and return Game class instance that takes it
        """
        structure = JsonListener.load_structure()
        seed = structure['seed']
        PSEUDO_RAND.seed(seed)

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
        """This method create new armies structure and return Game class instance that takes it"""
        rand_seed = randint(0, 1000)
        PSEUDO_RAND.seed(rand_seed)
        country_names = u_conf.COUNTRY_NAMES.copy()
        shuffle(country_names)

        armies = list()

        army_count = randint(u_conf.MIN_ARMY_COUNT, u_conf.MAX_ARMY_COUNT)
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
        """This method returns Soldier class instance"""
        soldier = Soldier()
        return soldier

    @classmethod
    def create_vehicle(cls, operator_count=None):
        """This method returns Vehicle class instance

        :arg operator_count:
            Operator count(int) (for 'create_from_json_structure' method)
            Default value: None (for 'create_new_structure' method)

        :return:
            Vehicle class instance

        """
        operators = list()

        if operator_count is not None:
            for _ in range(operator_count):
                operators.append(cls.create_soldier())
        else:
            operator_count = randint(u_conf.MIN_OPERATOR_COUNT, u_conf.MAX_OPERATOR_COUNT)
            for _ in range(operator_count):
                operators.append(cls.create_soldier())

        vehicle = Vehicle(operators_lst=operators)

        return vehicle

    @classmethod
    def create_squad(cls, units_data=None):
        """This method returns Squad class instance

        :arg units_data:
            1.For 'create_from_json_structure' method: List of dicts with units data
            Example: [{'type': 'Soldier'}, ... , {'type': 'Soldier'}]

            2.For 'create_new_structure' method: Default to None

        :return:
            Squad class instance

        """
        units = list()

        if units_data is not None:
            for unit in units_data:
                if unit['type'] == 'Soldier':
                    units.append(cls.create_soldier())
                elif unit['type'] == 'Vehicle':
                    units.append(cls.create_vehicle(len(unit['operators'])))
        else:
            unit_count = randint(u_conf.MIN_UNIT_COUNT, u_conf.MAX_UNIT_COUNT)
            for _ in range(unit_count):
                unit = choice([cls.create_soldier, cls.create_vehicle])()
                units.append(unit)

        squad = Squad(units_lst=units)

        return squad

    @classmethod
    def create_army(cls, country, strategy_name, squads_data=None):
        """This method creates and returns Army class instance

        :arg country:
            Country name(str)
        :arg strategy_name:
            Strategy name(str) (from 'strategies.py' module)
        :arg squads_data:
            1.For 'create_from_json_structure' method:
            List of squad dicts containing unit data dicts
            Example: [[{'type': 'Soldier'}, ...], ..., [{'type': 'Soldier'}, ...]]

            2.For 'create_new_structure' method: Default to None

        """
        squads = list()

        if squads_data is not None:
            for squad in squads_data:
                squad_data = squad
                squads.append(
                    cls.create_squad(squad_data['units'])
                )
        else:
            squad_count = randint(u_conf.MIN_SQUAD_COUNT, u_conf.MAX_SQUAD_COUNT)
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
