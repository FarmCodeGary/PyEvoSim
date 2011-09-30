'''
Utilities for a game or simulation taking place on a grid.
The primary two classes of this module are Coords and _Direction.

_Direction cannot be instantiated, but nine direction constants are defined,
along with four lists of directions.

Created on Sep 28, 2011

@author: Garrison Benson
'''

from collections import namedtuple
import math

class Coords(namedtuple("Coords",["x","y"])):
    """
    Coords represent two-dimensional coordinates, usually integers. The class
    behaves as a tuple with some additional math functionality.
    """
    __slots__ = ()
    
    @classmethod
    def make(cls,*args,**kwargs):
        """
        Makes a Coords given some input of possibly unknown type.
        The parameters can be any of the following:
        -an existing Coords object.
        -a 2-tuple of numbers.
        -two numbers.
        -two keyword arguments x and y (numbers).
        """
        if not kwargs and len(args) == 1:
            return cls._make(args[0])
        else:
            return cls(*args,**kwargs)
    
    def __repr__(self):
        return "Coords({0},{1})".format(self.x,self.y)
    
    def __neg__(self):
        return Coords(-self.x, -self.y)
    
    def __add__(self,other):
        return Coords(self.x + other.x, self.y + other.y)
    
    def __radd__(self,other):
        return self.__add__(other)
    
    def __sub__(self,other):
        return self + (-other)
    
    def __rsub__(self,other):
        return other + (-self)
    
    def __mul__(self,scalar):
        """
        Returns a new Coords with x and y each multiplied by the given number.
        """
        return Coords(self.x * scalar, self.y * scalar)
    
    def __rmul__(self,scalar):
        return self.__mul__(scalar)
    
    def __floordiv__(self,integer):
        """
        Returns a new Coords with x and y each integer-divided by the given
        integer.
        """
        return Coords(self.x // integer, self.y // integer)
    
    def __mod__(self,integer):
        """
        Returns a new Coords with x mod i, y mod i, where i is the parameter.
        """
        return Coords(self.x % integer, self.y % integer)
    
    @property
    def hypot(self):
        """
        Returns the distance to these coords from the origin.
        This can be used to find the distance between two coords as following:
        (c1-c2).hypot
        """
        return math.hypot(self.x, self.y)


class Direction(object):
    """
    This class represents compass directions. It is intended to be used as
    an enumeration. Each direction is primarily described using an offset (as a
    Coords object). Adding coords+dir.offset will find the neighboring coords
    in direction dir.
    Each direction also has a base cost, which is a scaled approximation of the
    hypotenuse of the offset.
    The name of a direction is its full name in lowercase, such as "north" or "southwest".
    The abbreviation is something like "N" or "SW".
    The oppositeDir is the dir with the inverse offset.
    
    The functions directionFromOffset, directionFromName, and
    directionFromAbbreviation (which are not part of this class itself, but
    related) are used to get a direction given its offset, name, or
    abbreviation.
    
    The lists CARDINAL_DIRECTIONS and DIAGONAL_DIRECTIONS should be self-
    explanatory. ALL_REAL_DIRECTIONS is a concatenation of CARDINAL_DIRECTIONS
    and DIAGONAL_DIRECTIONS. ALL_DIRECTIONS is like ALL_REAL_DIRECTIONS, but
    also includes the non-direction HERE.
    """
    def __init__(self,name,abbreviation,offset,baseCost,oppositeDir=None):
        self._name = name.lower()
        self._abbreviation = abbreviation.upper()
        self._offset = offset
        self._baseCost = baseCost
        if oppositeDir:
            self._oppositeDir = oppositeDir
            oppositeDir._oppositeDir = self
    
    @property
    def name(self):
        return self._name
    
    @property
    def abbreviation(self):
        return self._abbreviation
    
    @property
    def offset(self):
        return self._offset
    
    @property
    def baseCost(self):
        return self._baseCost
    
    @property
    def oppositeDir(self):
        return self._oppositeDir
    
    def __repr__(self):
        return "<{0}>".format(self.name.upper())
    
    
    # The reason that the following three methods are defined (which wouldn't
    # be necessary under normal circumstances) is on the chance that a
    # Direction gets pickled - on unpickling it will not be the canonical
    # direction object, but it will be otherwise equal. So, these methods
    # should make it compatible.
    def __eq__(self,other):
        try:
            return self.offset == other.offset
        except AttributeError:
            return False
    
    def __ne__(self,other):
        return not (self.__eq__(other))
    
    def __hash__(self):
        return hash(self.offset)


NORTH = Direction("north","N",Coords(0,-1),2)
SOUTH = Direction("south","S",Coords(0,1),2,NORTH)
EAST = Direction("east","E",Coords(1,0),2)
WEST = Direction("west","W",Coords(-1,0),2,EAST)
NORTHEAST = Direction("northeast","NE",Coords(1,-1),3,)
SOUTHWEST = Direction("southwest","SW",Coords(-1,1),3,NORTHEAST)
NORTHWEST = Direction("northwest","NW",Coords(-1,-1),3)
SOUTHEAST = Direction("southeast","SE",Coords(1,1),3,NORTHWEST)
HERE = Direction("here","H",Coords(0,0),0)
HERE._oppositeDir = HERE

CARDINAL_DIRECTIONS = [NORTH, SOUTH, EAST, WEST]
DIAGONAL_DIRECTIONS = [NORTHEAST, SOUTHWEST, NORTHWEST, SOUTHEAST]
ALL_REAL_DIRECTIONS = CARDINAL_DIRECTIONS + DIAGONAL_DIRECTIONS
ALL_DIRECTIONS = ALL_REAL_DIRECTIONS + [HERE]

_OFFSETMAP = dict([(dir.offset,dir) for dir in ALL_DIRECTIONS])
_NAMEMAP = dict([(dir.name,dir) for dir in ALL_DIRECTIONS])
_ABBREVIATIONMAP = dict([(dir.abbreviation,dir) for dir in ALL_DIRECTIONS])

# Three functions for looking up a direction.
directionFromOffset = _OFFSETMAP.__getitem__
directionFromName = _NAMEMAP.__getitem__
directionFromAbbreviation = _ABBREVIATIONMAP.__getitem__
