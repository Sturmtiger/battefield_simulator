"""You can add new strategies in this module"""

from pseudo_random import PSEUDO_RAND

STRATEGY_REGISTRY = dict()


def registry(cls):
    STRATEGY_REGISTRY[cls.name] = cls


class Strategy:
    name = None

    def choose_squad(squads):
        raise NotImplementedError


@registry
class RandomStrategy(Strategy):
    name = 'random'

    def choose_squad(squads_iterable):
        # chosen_squad = choice(squads_iterable)
        chosen_squad = PSEUDO_RAND.choice(squads_iterable)
        return chosen_squad


@registry
class WeakestStrategy(Strategy):
    name = 'weakest'

    def choose_squad(squads_iterable):
        chosen_squad = min(squads_iterable, key=lambda s: s.total_hp)
        return chosen_squad


@registry
class StrongestStrategy(Strategy):
    name = 'strongest'

    def choose_squad(squads_iterable):
        chosen_squad = max(squads_iterable, key=lambda s: s.total_hp)
        return chosen_squad
