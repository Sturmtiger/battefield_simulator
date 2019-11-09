"""Special functions for battlefield-simulator game"""

from math import exp, fsum, log
from random import choice
from strategies import STRATEGY_REGISTRY


def geometric_mean(iterable):
    """Takes an iterable argument and returns its geometric mean"""
    return exp(fsum(log(x) for x in iterable) / len(iterable))


def choose_squad(squads, strategy_name):
    """Selects a squad by strategy and returns it"""
    defined_strategy = STRATEGY_REGISTRY[strategy_name]
    chosen_squad = defined_strategy.choose_squad(squads)
    return chosen_squad


def get_random_strategy_name():
    """Returns random strategy name"""
    strategy_names = list(STRATEGY_REGISTRY.keys())
    return choice(strategy_names)
