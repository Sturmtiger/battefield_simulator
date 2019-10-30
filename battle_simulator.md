## Introduction

The focus of the test is to asses the maintainability and extendability of the code the candidate presents.

The candidate is required to create a new branch on the repository and send an email once the task is completed.

There are **NO** time nor any technology constraints. The candidate should feel free to use any technology he/she feels comfortable in.

If the candidate is picked for an interview, he/she will be required to provide an explanation on how the application could be extended with additional features.

## Description

This simulator is supposed to determine a battle outcome based on probability calculations.

Once the simulator is started all the army squads will start attacking each other until there is only one army left.


## Units

Each unit represents either a soldier or a vehicle maned by a predetermined number of soldiers.

All units have the following properties:


| Property |     Range    |                             Description                                 |
|----------|--------------|-------------------------------------------------------------------------| 
| health   | % \[0-100\]  | Represents the health of the unit                                       |
| recharge | \[100-2000\] | Represents the number of ms required to recharge the unit for an attack |


### Soldiers

Soldiers are units that have an additional property:


|  Property  |   Range  |            Description            |
|------------|----------|-----------------------------------|
| experience | \[0-50\] | Represents the soldier experience |

The **experience**  property is incremented after each successful attack, and is sed to calculate the attack success probability and the amount of damage inflicted

Soldiers are considered active as long as they have any health.

#### Attack

Soldiers attack success probability is calculated:

0.5 * (1 + health/100) * random(50 + experience, 100) / 100

where **random(min, max)** returns a random number between min and max (inclusive)

#### Damage

The amount of damage a soldier can afflict is calculated as follows:

0.05 + experience / 100


### Vehicles

A battle vehicle has these additional properties:


|   Property  |  Range  |                        Description                     |
|-------------|---------|--------------------------------------------------------|
|  operators  | \[1-3\] | The number of soldiers required to operate the vehicle |     

The **recharge** property for a vehicle must be greater than 1000 (ms).

The total health of a vehicle unit is represented as the average health of all it's operators and the health of the vehicle.

A vehicle is considered active as long as it self has any health and there is an vehicle operator with any health.
If the vehicle is destroyed, any remaining vehicle operator is considered as inactive (killed).


#### Attack
The Vehicle attack success probability is determined as follows:

0.5 * (1 + vehicle.health / 100) * gavg(operators.attack_success)

where **gavg** is the geometric average of the attack success of all the vehicle operators

#### Damage

The damage afflicted by a vehicle is calculated:

0.1 + sum(operators.experience / 100)

The total damage inflicted on the vehicle is distributed to the operators as follows:
60% of the total damage is inflicted on the vehicle
20% of the total damage is inflicted on a random vehicle operator
The rest of the damage is inflicted evenly to the other operators (10% each)



## Squads

Squads are consisted out of a number of units (soldiers or vehicles), that behave as a coherent group.

A squad is active as long as is contains an active unit.

#### Attack

The attack success probability of a squad is determined as the geometric average o the attack success probability of each member.

#### Damage

The damage received on a successful attack is distributed evenly to all squad members.
The damage inflicted on a successful attack is the accumulation of the damage inflicted by each squad member.

## Attacking & Defending

Each time a squad attacks it must choose a target squad, depending on the chosen strategy:


| Strategy  |              Description              |
|-----------|---------------------------------------|
| random    | attack any random squad               |
| weakest   | attack the weakest opposing squad     |
| strongest | attack the strongest opposing squad   |

Once the target is determined both the attacking and defending squads calculate their attack probability success and the squad with the highest probability wins.
If the attacking squad wins, damage is dealt to the defending side, otherwise no damage is inflicted to the attacking side.

------If the attacking squad wins, damage is dealt to the defending side.
------If the attacking squad loses, no damage is dealt to either side.


## Configuration

The following constraints should be configurable:

- The number of armies: 2 <= n
- The choice of attack strategy per army: random|weakest|strongest
- The number of squads per army: 2 <= n
- The number of units per squad: 5 <= n <= 10
