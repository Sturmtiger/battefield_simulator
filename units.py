from units_consts import *
from random import randint, choice, shuffle
from statistics import mean
from specfuncs import unit_iterator, geometric_mean as gmean


# abstract class
class Unit:
    def __init__(self, hp, recharge):   # make recharge work!!!!
        self.hp = hp
        self.recharge = recharge

    def inflict_damage(self, damage):
        return damage
        # if self.attack_success() >= enemy_unit.attack_success():  # attack_success may be from Soldier or from Vehicle
        # enemy_unit.hp -= damage
        # enemy_unit.hp = max(enemy_unit.hp, 0)  # if hp <= 0 then hp == 0

    def attack_success(self, probability_of_attack):  # if self success >= enemy success then attack is success!
        return probability_of_attack

    @property
    def is_active(self):
        return self.hp > 0


class Soldier(Unit):
    def __init__(self, hp=SOLDIER_HP, recharge=SOLDIER_RECHARGE, exp=SOLDIER_EXP):
        self.exp = exp
        super().__init__(hp, recharge)

    def inflict_damage(self):
        damage = 0.05 + self.exp / 100
        return super().inflict_damage(damage)

    def attack_success(self):
        probability_of_attack = 0.5 * (1 + self.hp / 100) * randint(50 + self.exp, 100) / 100
        return super().attack_success(probability_of_attack)

    def gain_exp(self):
        self.exp += 1
        self.exp = min(self.exp, 50)  # if exp > 50 then exp == 50


class Vehicle(Unit):
    def __init__(self, hp=VEHICLE_HP, recharge=VEHICLE_RECHARGE, operator_count=OPERATOR_COUNT):
        self.operators = [Soldier() for _ in range(operator_count)]
        hp = mean([hp, *(op.hp for op in self.operators)])  # mean of vehicle hp and its operators hp
        super().__init__(hp, recharge)

    def inflict_damage(self):
        damage = 0.1 + sum(soldier.exp for soldier in self.operators) / 100
        return super().inflict_damage(damage)

    def attack_success(self):
        probability_of_attack = 0.5 * (1 + self.hp / 100) * gmean([sold.attack_success()
                                                                  for sold in self.operators if sold.is_active])
        return super().attack_success(probability_of_attack)

    @property
    def is_active(self):
        active_operators = any(op for op in self.operators if op.is_active)
        return self.hp > 0 and active_operators


class Squad:
    def __init__(self, soldier_count=SOLDIER_COUNT, vehicle_count=VEHICLE_COUNT):
        self.soldiers = [Soldier() for _ in range(soldier_count)]
        self.vehicles = [Vehicle() for _ in range(vehicle_count)]

    def attack_success(self):
        probability_of_attack = gmean([sold.attack_success() for sold in self.soldiers if sold.is_active] +
                                      [veh.attack_success() for veh in self.vehicles if veh.is_active])
        return probability_of_attack

    def inflict_damage(self):
        damage = sum(unit.inflict_damage() for unit in unit_iterator('is_active', self.soldiers, self.vehicles))
        return damage  # total damage of all units

    @property
    def total_hp(self):
        total_hp = sum(unit.hp for unit in unit_iterator('is_active', self.soldiers, self.vehicles))
        return total_hp

    @property
    def is_active(self):
        is_active = any(unit_iterator('is_active', self.soldiers, self.vehicles))
        return is_active


class Army:
    def __init__(self, squad_count=SQUAD_COUNT, strategy=STRATEGIES[0]):
        self.squads = [Squad() for _ in range(squad_count)]
        self.strategy = strategy

    def attack(self, enemy_army):
        if self.is_active:
            chosen_squad = choice([squad for squad in self.squads if squad.is_active])

            if self.strategy == 'random':
                enemy_squad = choice([squad for squad in enemy_army.squads if squad.is_active])
            elif self.strategy == 'weakest':
                enemy_squad = min((squad for squad in self.squads if squad.is_active), key=lambda s: s.total_hp)
            elif self.strategy == 'strongest':
                enemy_squad = max((squad for squad in self.squads if squad.is_active), key=lambda s: s.total_hp)

            if chosen_squad.attack_success() > enemy_squad.attack_success():
                damage_quotient_for_each = chosen_squad.inflict_damage() / len(list(unit_iterator('is_active',
                                                                                                  enemy_squad.soldiers,
                                                                                                  enemy_squad.vehicles))
                                                                               )
                for sold in enemy_squad.soldiers:
                    if sold.is_active:
                        sold.hp -= damage_quotient_for_each
                for veh in enemy_squad.vehicles:
                    if veh.is_active:
                        active_operators = [op for op in veh.operators if op.is_active]
                        if len(active_operators) > 2:
                            shuffle(active_operators)
                            veh.hp -= damage_quotient_for_each * 0.6
                            active_operators[0].hp -= damage_quotient_for_each * 0.2
                            for op in active_operators[1:3]:
                                op.hp -= damage_quotient_for_each * 0.1

                for unit in unit_iterator('is_active', chosen_squad.soldiers, chosen_squad.vehicles):  # give exp
                    if isinstance(unit, Vehicle):
                        for op in unit.operators:
                            op.gain_exp()
                    else:
                        unit.gain_exp()

    @property
    def is_active(self):
        is_active = any(squad for squad in self.squads if squad.is_active)
        return is_active
