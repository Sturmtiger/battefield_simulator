"""
Special functions for battlefield-simulator game
"""

from pseudo_random import p_rand
from strategies import STRATEGY_REGISTRY


def choose_squad(squads, strategy_name):
    defined_strategy = STRATEGY_REGISTRY[strategy_name]
    chosen_squad = defined_strategy.choose_squad(squads)
    return chosen_squad


def get_random_strategy_name():
    strategy_names = list(STRATEGY_REGISTRY.keys())
    return p_rand.choice(strategy_names)
