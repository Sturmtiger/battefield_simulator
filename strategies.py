from pseudo_random import p_rand

STRATEGY_REGISTRY = dict()


def registry(cls):
    STRATEGY_REGISTRY[cls.name] = cls


class Strategy:
    name = None

    def choose_squad(squads):
        pass


@registry
class RandomStrategy(Strategy):
    name = 'random'

    def choose_squad(squads_iterable):
        # chosen_squad = choice(squads_iterable)
        chosen_squad = p_rand.choice(squads_iterable)
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
