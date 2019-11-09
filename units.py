"""This module contains unit classes for Battlefield game"""

from time import monotonic
from statistics import mean
from specfuncs import choose_squad, geometric_mean as gmean
import units_configuration as u_cong
from pseudo_random import PSEUDO_RAND


# abstract class
class Unit:
    """Abstract class for units"""

    def __init__(self, hp, recharge_ms):
        self.hp = hp
        self.recharge_ms = recharge_ms
        self.recharge_time = 0

    def inflict_damage(self, damage):
        """takes calculated damage in the same method of child class"""
        return damage

    def attack_success(self, probability_of_attack):
        """takes calculated attack success probability
         in the same method of child class"""
        return probability_of_attack

    def recharge(self):
        """recharges a unit"""
        # pass
        self.recharge_time = monotonic() * 1000 + self.recharge_ms

    def get_damage(self, damage):
        """takes damage value and spreads to the unit"""
        self.hp -= damage

    @property
    def is_active(self):
        """:returns bool"""
        return self.hp > 0

    @property
    def is_charged(self):
        """:returns bool"""
        return self.recharge_time < round(monotonic() * 1000)


class Soldier(Unit):
    """Soldier unit class"""

    def __init__(self, hp=u_cong.SOLDIER_HP, recharge_ms=u_cong.SOLDIER_RECHARGE_MS):
        self.exp = 0
        super().__init__(hp, recharge_ms)

    def inflict_damage(self):
        """:returns calculated damage value (float)"""
        damage = 0.05 + self.exp / 100
        return super().inflict_damage(damage)

    def attack_success(self):
        """:returns attack success probability (float)"""
        probability_of_attack = 0.5 * ((1 + self.hp / 100) *
                                       PSEUDO_RAND.randint(50 + self.exp, 100) / 100)
        return super().attack_success(probability_of_attack)

    def gain_exp(self):
        """increases the experience of the soldier"""
        self.exp += 1
        self.exp = min(self.exp, 50)  # if exp > 50 then exp == 50


class Vehicle(Unit):
    """Vehicle unit class"""

    def __init__(self, operators_lst, hp=u_cong.VEHICLE_HP, recharge_ms=u_cong.VEHICLE_RECHARGE_MS):
        self.operators = operators_lst
        hp = mean([hp, *(op.hp for op in self.operators)])
        super().__init__(hp, recharge_ms)

    def inflict_damage(self):
        """:returns calculated damage value (float)"""
        damage = 0.1 + sum(op.exp for op in self.operators if op.is_active) / 100
        return super().inflict_damage(damage)

    def attack_success(self):
        """:returns attack success probability (float)"""
        probability_of_attack = 0.5 * (1 + self.hp / 100) * gmean([op.attack_success()
                                                                   for op in self.operators
                                                                   if op.is_active])
        return super().attack_success(probability_of_attack)

    def get_damage(self, damage):
        """takes damage value and spreads to both
        vehicle hp and active operators hp"""
        active_operators = [op for op in self.operators if op.is_active]
        if len(active_operators) > 2:
            self.hp -= damage * 0.6
            unlucky_op = PSEUDO_RAND.choice(active_operators)
            for op in active_operators:
                if op is unlucky_op:
                    op.get_damage(damage * 0.2)
                else:
                    op.get_damage(damage * 0.1)
        else:
            self.hp -= damage * 0.7
            unlucky_op = PSEUDO_RAND.choice(active_operators)
            unlucky_op.get_damage(damage * 0.3)

    def gain_exp(self):
        """increases the experience of each operator"""
        active_operators = [op for op in self.operators if op.is_active]
        for op in active_operators:
            op.gain_exp()

    @property
    def is_active(self):
        """:returns Bool"""
        active_operators = any(op for op in self.operators if op.is_active)
        return self.hp > 0 and active_operators


class Squad:
    """Squad class"""

    def __init__(self, units_lst):
        self.units = units_lst

    def attack(self, enemy_squad):
        """Attack enemy squad"""
        if self.attack_success >= enemy_squad.attack_success:
            charged_units = [unit for unit in self.active_units if unit.is_charged]
            damage = self.total_damage
            enemy_squad.get_damage(damage)
            print(f'\t[Squad] is attacking [Enemy Squad]. '
                  f'(Inflicted damage: {round(damage, 2)} hp)')
            for unit in charged_units:
                unit.recharge()
                unit.gain_exp()
        else:
            print(f'\t[Squad] unsuccessfully attacked [Enemy Squad]')

    def get_damage(self, damage):
        """takes damage value and spreads evenly to active units of the squad"""
        active_units_lst = self.active_units
        damage_quotient_for_each = damage / len(active_units_lst)
        for unit in active_units_lst:
            unit.get_damage(damage_quotient_for_each)

    @property
    def total_damage(self):
        """:returns the sum of damage of all active units"""
        charged_units = [unit for unit in self.active_units if unit.is_charged]
        total_damage = sum(unit.inflict_damage() for unit in charged_units)
        return total_damage

    @property
    def total_hp(self):
        """:returns the sum of hp of all active units"""
        total_hp = sum(unit.hp for unit in self.units if unit.is_active)
        return total_hp

    @property
    def attack_success(self):
        """:returns attack success probability (float)"""
        probability_of_attack = gmean([unit.attack_success()
                                       for unit in self.units
                                       if unit.is_active])
        return probability_of_attack

    @property
    def active_units(self):
        """:returns list of active units"""
        active_units = [unit for unit in self.units if unit.is_active]
        return active_units

    @property
    def charged_unit_count(self):
        """:returns charged unit count (int)"""
        active_units = (unit for unit in self.units if unit.is_active)
        charged_unit_count = sum(1 for unit in active_units if unit.is_charged)
        return charged_unit_count

    @property
    def is_active(self):
        """:returns Bool"""
        is_active = any(unit for unit in self.units if unit.is_active)
        return is_active


class Army:
    """Army class"""

    def __init__(self, country, strategy_name, squads_lst):
        self.country = country
        self.squads = squads_lst
        self.strategy_name = strategy_name

    def __str__(self):
        return self.country

    def attack(self, enemy_army):
        """attacks enemy army"""
        if self.is_active:
            # the most charged squad of active
            chosen_squad = max(self.active_squads, key=lambda s: s.charged_unit_count)
            if chosen_squad.charged_unit_count == 0:
                print(f'[{self} Army] has no any charged units in squads '
                      f'and cannot attack [{enemy_army} Army]')
                return

            print(f'[{self} Army] is attacking [{enemy_army} Army]:')
            enemy_squad = choose_squad(enemy_army.active_squads, self.strategy_name)
            chosen_squad.attack(enemy_squad)

    @property
    def is_active(self):
        """:returns Bool"""
        is_active = any(squad for squad in self.squads if squad.is_active)
        return is_active

    @property
    def active_squads(self):
        """:returns list of active squads"""
        active_squads = [squad for squad in self.squads if squad.is_active]
        return active_squads
