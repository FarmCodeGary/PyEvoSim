from coords import Coords,CARDINAL_DIRECTIONS

class Board(dict):
    """
    This class represents the game board. Note that it subclasses dict.
    The keys are always Coords, and they are checked to ensure they are within
    the bounds given in the constructor.
    
    If width and height are not provided (or are None), then they are not limited,
    and nothing is considered out-of-bounds in that dimension.
    """
    def __init__(self,width=None,height=None,neighborDirs=CARDINAL_DIRECTIONS):
        dict.__init__(self)
        self.width = width
        self.height = height
        self._neighborDirs = neighborDirs
    
    def __setitem__(self,key,value):
        """
        This wraps dict's __setitem__, ensuring that the key is an instance of
        Coords. (You can pass in a regular 2-tuple and it will be converted.)
        It also ensures the coords are within the bounds of the board.
        """
        coords = Coords.make(key) # Make sure everything is a Coord
        if not self.checkWithinBounds(coords):
            raise Exception, "{0} out of bounds.".format(coords)
        else:
            dict.__setitem__(self,coords,value)
    
    def __getitem__(self,key):
        coords = Coords.make(key)
        if not self.checkWithinBounds(coords):
            raise Exception, "{0} out of bounds.".format(coords)
        else:
            return dict.__getitem__(self,coords)
    
    def checkWithinBounds(self,coords):
        """Returns true if the given coords are within the board's bounds."""
        trueCoords = Coords.make(coords)
        withinXBounds = (self.width == None) or (trueCoords.x >= 0 and trueCoords.x < self.width)
        withinYBounds = (self.height == None) or (trueCoords.y >= 0 and trueCoords.y < self.height)
        return withinXBounds and withinYBounds
    
    def getNeighbors(self,coords):
        return [coords+dir.offset for dir in self._neighborDirs if self.checkWithinBounds(coords+dir.offset)]
