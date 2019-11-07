from json import load, dump
import os
from units import Soldier, Vehicle


class JsonListener:
    @staticmethod
    def dump_structure(seed, armies_lst):
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
        with open('config/config.json', 'w') as f:
            dump(structure, f)

    @staticmethod
    def load_structure():
        try:
            with open('config/config.json', 'r') as f:
                structure = load(f)
        except FileNotFoundError:
            raise FileNotFoundError('Last game not found!')

        return structure
