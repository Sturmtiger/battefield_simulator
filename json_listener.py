"""This module contains JsonListener class for processing JSON data
for the Battlefield game
"""

from json import load, dump
import os
from units import Vehicle


class JsonListener:
    """This class may dump armies structure to JSON and load JSON-structured armies data"""

    @staticmethod
    def dump_structure(seed, armies_lst):
        """Dumps armies structure to JSON file"""
        structure = {
            'seed': seed,
            'armies': [
                {
                    'country': army.country,
                    'strategy': army.strategy_name,
                    'squads': [
                        {
                            'units': [
                                {
                                    'type': unit.__class__.__name__,
                                    'operators': [
                                        {'type': op.__class__.__name__}
                                        for op in unit.operators
                                    ]
                                }
                                if isinstance(unit, Vehicle)
                                else
                                {'type': unit.__class__.__name__}
                                for unit in squad.units
                            ]
                        } for squad in army.squads
                    ]
                } for army in armies_lst
            ]
        }

        if not os.path.exists('config'):
            os.mkdir('config')
        with open('config/config.json', 'w') as json_file:
            dump(structure, json_file)

    @staticmethod
    def load_structure():
        """Loads armies structure of the last game from JSON file"""
        try:
            with open('config/config.json', 'r') as json_file:
                structure = load(json_file)
        except FileNotFoundError:
            raise FileNotFoundError('Last game not found!')

        return structure
