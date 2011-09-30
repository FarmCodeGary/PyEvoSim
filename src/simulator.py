'''
Created on Sep 28, 2011

@author: garrison
'''

from utils.board import Board
import actions
from boardelements import Monster,FOOD
from random import shuffle,random as probcheck

class Simulation(Board):
    """
    This class represents the simulation as a whole (including the board).
    It's unfortunately a non-homogenous data structure. The keys are always
    Coords, but the values can be Monsters or FOOD. In the future it would
    be very good to make this structure homogenous, and elsewhere stop using
    isinstance to check if something's a monster. For now... oh well.
    """
    def __init__(self,config):
        Board.__init__(self,config.BOARD_WIDTH,config.BOARD_HEIGHT)
        self.config = config
        with open("names.txt") as namesFile:
            self._namesList = [line.replace("\n","") for line in namesFile.readlines()]
        shuffle(self._namesList)
        initialDNAString = config.INITIAL_DNA
        if initialDNAString:
            startDNA = [actions.DNA_MAP[char] for char in initialDNAString.upper()]
        else:
            startDNA = list(actions.ALL_ACTIONS) # Copy the list
            shuffle(startDNA)
        
        totalMonsters = 0
        totalFood = 0
        for x in range(self.width):
            for y in range(self.height):
                if probcheck() < config.MONSTER_DENSITY and totalMonsters < config.MAX_NUM_MONSTERS:
                    self[x,y] = Monster(startDNA, config.INITIAL_HP, config.INITIAL_COLOR)
                    totalMonsters += 1
                elif probcheck() < config.FOOD_DENSITY and totalFood < config.MAX_NUM_FOOD:
                    self[x,y] = FOOD
                    totalFood += 1
    
    def oneStep(self):
        """
        Executes one step of the simulation. Each monster performs one action,
        the first applicable action in its DNA. (In other words, the first
        action that does not throw a CannotPerformActionException.)
        
        The order in which the monsters move is, for now, non-deterministic,
        as it is based on the "order" of the keys in the underlying dict.
        """
        for coords,element in self.items():
            if isinstance(element,Monster):
                monster = element
                self.changeMonsterHP(monster, coords, -self.config.HP_LOSS_PER_TURN)
                if monster.hp > 0:
                    for action in monster.dna:
                        try:
                            action(self,monster,coords)
                            break
                        except actions.CannotPerformActionException:
                            pass
    
    def moveMonster(self,monster,oldCoords,newCoords):
        """
        Moves a monster to a different location. If the location contains food,
        the monster will eat it, gaining HP of configurable amount
        FOOD_HP_INCREASE.
        """
        existing = self.get(newCoords)
        if existing == FOOD:
            # The monster gets to eat the food.
            monster.hp += self.config.FOOD_HP_INCREASE
        elif existing:
            raise Exception # Trying to move a monster on top of another monster
        del self[oldCoords]
        self[newCoords] = monster
    
    def changeMonsterHP(self,monster,monsterCoords,offset):
        """
        Changes the monster's HP by the given offset, possibly killing it and
        replacing it with food.
        """
        monster.hp += offset
        if monster.hp <= 0:
            # The monster is dead. Replace it with FOOD!
            self[monsterCoords] = FOOD
    
    def toggleMonsterFollowed(self,monster):
        """
        Toggles whether or not the given monster is followed. If this is the
        first time the monster has been followed, it will also be named.
        """
        monster.followed = not monster.followed
        if not monster.name:
            name = self._namesList.pop(0)
            monster.name = name
            print "Monster {0} renamed {1}.".format(id(monster),name)
    