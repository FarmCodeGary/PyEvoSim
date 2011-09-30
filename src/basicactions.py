'''
This module contains implementations of monster actions, which are used to form
monster "DNA".

Created on Sep 28, 2011

@author: garrison
'''

from boardelements import Monster,FOOD
from actions import monsterAction,CannotPerformActionException
import random

@monsterAction
def wander(simulator,monster,monsterCoords):
    """
    Causes the monster to move into an adjacent empty space.
    Preconditions: An adjacent space is empty.
    """
    neighbors = simulator.getNeighbors(monsterCoords)
    emptyNeighbors = [neighbor for neighbor in neighbors if not isinstance(simulator.get(neighbor),Monster)]
    if not emptyNeighbors:
        raise CannotPerformActionException
    else:
        chosenNeighbor = random.choice(emptyNeighbors)
        simulator.moveMonster(monster,monsterCoords,chosenNeighbor)

@monsterAction
def flee(simulator,monster,monsterCoords):
    """
    Causes the monster to move into an adjacent empty space.
    Preconditions: An adjacant space is empty, and another adjacent space
    contains another monster.
    """
    neighbors = simulator.getNeighbors(monsterCoords)
    emptyNeighbors = [neighbor for neighbor in neighbors if not isinstance(simulator.get(neighbor),Monster)]
    monsterNeighbors = [neighbor for neighbor in neighbors if isinstance(simulator.get(neighbor),Monster)]
    if not monsterNeighbors or not emptyNeighbors:
        raise CannotPerformActionException
    else:
        chosenNeighbor = random.choice(emptyNeighbors)
        simulator.moveMonster(monster,monsterCoords,chosenNeighbor)

@monsterAction
def attack(simulator,monster,monsterCoords):
    """
    Attacks an adjacent monster, causing damage given by the configurable value
    ATTACK_HP_DECREASE.
    Preconditions: At least one adjacent space contains another monster.
    """
    neighbors = simulator.getNeighbors(monsterCoords)
    monsterNeighbors = [neighbor for neighbor in neighbors if isinstance(simulator.get(neighbor),Monster)]
    if not monsterNeighbors:
        raise CannotPerformActionException
    else:
        chosenVictimCoords = random.choice(monsterNeighbors)
        chosenVictim = simulator[chosenVictimCoords]
        simulator.changeMonsterHP(chosenVictim,chosenVictimCoords,-simulator.config.ATTACK_HP_DECREASE)

@monsterAction
def idle(simulator,monster,monsterCoords):
    """
    Does absolutely nothing.
    Preconditions: None.
    
    Note that this effectively terminates the monster's search for an
    appropriate action: Any actions prioritized below idle will NEVER be
    performed.
    """
    pass

@monsterAction
def rest(simulator,monster,monsterCoords):
    """
    Increases the monster's HP by the configurable quantity REST_HP_INCREASE.
    Preconditions: The HP is below the configurable value REST_MAX_HP.
    """
    if monster.hp < simulator.config.REST_MAX_HP:
        monster.hp += simulator.config.REST_HP_INCREASE
    else:
        raise CannotPerformActionException

@monsterAction
def heal(simulator,monster,monsterCoords):
    """
    Increases the HP of an adjacent monster by the configurable value
    HEAL_HP_INCREASE.
    Preconditions: There is at least one adjacent space containing a monster.
    """
    neighbors = simulator.getNeighbors(monsterCoords)
    monsterNeighbors = [neighbor for neighbor in neighbors if isinstance(simulator.get(neighbor),Monster)]
    if not monsterNeighbors:
        raise CannotPerformActionException
    else:
        chosenMonsterCoords = random.choice(monsterNeighbors)
        chosenMonster = simulator[chosenMonsterCoords]
        simulator.changeMonsterHP(chosenMonster,chosenMonsterCoords,simulator.config.HEAL_HP_INCREASE)

@monsterAction
def eat(simulator,monster,monsterCoords):
    """
    Moves onto a space with food (thus consuming the food).
    Preconditions: There is at least one adjacent space containing food.
    
    NOTE that a monster can still eat even without performing this action, if
    it happens to move onto a space with food. This action makes the monster
    always move to a food space if one is available.
    """
    neighbors = simulator.getNeighbors(monsterCoords)
    foodNeighbors = [neighbor for neighbor in neighbors if simulator.get(neighbor) == FOOD]
    if not foodNeighbors:
        raise CannotPerformActionException
    else:
        chosenCoords = random.choice(foodNeighbors)
        simulator.moveMonster(monster,monsterCoords,chosenCoords)

@monsterAction
def divide(simulator,monster,monsterCoords):
    """
    Causes the monster to divide in two. The offspring will have a chance of
    mutation given by the configurable value MUTATION_RATE. If the monster
    mutates, one component of its RGB color will increase or decrease by
    COLOR_CHANGE_OFFSET.
    Preconditions: The monster's HP is at least the configurable value
    DIVIDE_MIN_HP, and at least one adjacent space is empty.
    """
    # TODO: This needs to be cleaned up and refactored.
    if monster.hp < simulator.config.DIVIDE_MIN_HP:
        raise CannotPerformActionException
    neighbors = simulator.getNeighbors(monsterCoords)
    emptyNeighbors = [neighbor for neighbor in neighbors if not isinstance(simulator.get(neighbor),Monster)]
    if not emptyNeighbors:
        raise CannotPerformActionException
    else:
        chosenNeighbor = random.choice(emptyNeighbors)
        if random.random() < simulator.config.MUTATION_RATE:
            # Mutate!
            childDNA = list(monster.dna) # Copy the DNA
            # Choose any two adjacent DNA elements and swap them.
            swapIndex = random.randint(0,len(childDNA)-2) # Must not be the last index.
            childDNA[swapIndex],childDNA[swapIndex+1] = childDNA[swapIndex+1],childDNA[swapIndex]
            
            # Change the color
            colorComponentToChange = random.choice([0,1,2])
            changeOffset = random.choice([-simulator.config.COLOR_CHANGE_OFFSET,simulator.config.COLOR_CHANGE_OFFSET])
            newColorList = list(monster.color)
            # Change the color, preventing it from going out of range.
            newColorList[colorComponentToChange] = min(255,max(0,newColorList[colorComponentToChange] + changeOffset))
            childColor = tuple(newColorList)
        else:
            # Don't mutate. :(
            childDNA = monster.dna # Use the exact same DNA
            childColor = monster.color # and color
        halfHP = monster.hp // 2
        simulator.changeMonsterHP(monster, monsterCoords, -halfHP)
        childHP = halfHP
        if simulator.get(chosenNeighbor) == FOOD:
            childHP += simulator.config.FOOD_HP_INCREASE
        child = Monster(childDNA,childHP,childColor)
        simulator[chosenNeighbor] = child
