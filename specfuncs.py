"""
Special functions for battlefield-simulator game
"""

from random import choice
from strategies import STRATEGY_REGISTRY


def choose_squad(squads, strategy_name):
    defined_strategy = STRATEGY_REGISTRY[strategy_name]
    chosen_squad = defined_strategy.choose_squad(squads)
    return chosen_squad


def get_random_strategy_name():
    strategy_names = list(STRATEGY_REGISTRY.keys())
    return choice(strategy_names)
