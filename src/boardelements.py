'''
Aside from the Monster class, this module also defines the constant FOOD.

Created on Sep 28, 2011

@author: garrison
'''

FOOD = object()
# Since food doesn't have any properties at all, we might as well only have one
# instance of it and use that everywhere. (...For now.)

class Monster(object):
    """
    This class represents one monster. At the moment hardly any of the actual
    behavior is represented here. In the future this may or may not be the case.
    """
    
    __slots__ = ("hp","dna","color","followed","name")
    # Slots may improve performance a bit.
    
    def __init__(self,dna,hp,color):
        """
        Creates a new monster.
        dna is the monsters DNA represented as a list of action functions.
        hp is the monster's starting health points, represented as an integer.
        color is the monster's color, represented as a 3-tuple of integers
        ranging from 0-255 (RGB values).
        """
        self.hp = hp
        self.dna = dna # dna is a list of action functions.
        self.color = color
        
        self.followed = False
        # Marked as true when the monster is being "tracked" or closely
        # observed. Note that at this time, all it means is that the monster
        # has a different-shaped sprite.
        
        self.name = None
        # The monster's name. Monsters have no name by default, but can be
        # given one later, to help keep them straight.
    
    @property
    def dnaString(self):
        """Formats the DNA as a string, such as "DWIAFEHR"."""
        return "".join([action.letter for action in self.dna])
    
    @property
    def infoString(self):
        """
        Returns a string with info about the monster.
        Examples:
        "Cameron (147379148), dna=DWIAFEHR, hp=364"
        "147341644, dna=EDIAWFHR, hp=34"
        """
        if self.name:
            return "{0} ({1}), dna={2}, hp={3}".format(self.name,id(self),self.dnaString,self.hp)
        else:
            return "{0}, dna={1}, hp={2}".format(id(self),self.dnaString,self.hp)
    
    def __repr__(self):
        return "<Monster {0}>".format(self.infoString)
