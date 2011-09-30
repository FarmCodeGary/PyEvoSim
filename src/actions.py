'''
Created on Sep 29, 2011

@author: garrison
'''

import string

class CannotPerformActionException(Exception):
    """
    An exception thrown when an action cannot be performed.
    (Note that this is perfectly normal behavior: it just means the
    preconditions for the action aren't met.)
    """
    pass

ALL_ACTIONS = []
DNA_MAP = {}

def monsterAction(actionFunction,letter=None):
    """
    This is a decorator function for monster action declarations.
    The "letter" parameter specifies the letter representing the action, used
    for compact string representations of monster DNA. If the parameter is not
    provided, the first letter of the function name will be used.
    
    Example usage:
    @monsterAction("Z")
    def sleep(simulator,monster,monsterCoords:
        ...
    
    @monsterAction  # Parameter is not provided, so letter will be "S"
    def selfDestruct(simulator,monster,monsterCoords):
        ...
    """
    if letter == None:
        letter = actionFunction.__name__[0].upper()
    else:
        letter = letter.upper()
    assert len(letter) == 1 and letter in string.ascii_uppercase
    actionFunction.letter = letter
    actionFunction.name = actionFunction.__name__
    ALL_ACTIONS.append(actionFunction)
    assert letter not in DNA_MAP
    DNA_MAP[letter] = actionFunction
    return actionFunction

import basicactions
# This is the only place the actions themselves are actually imported.
# (Perhaps in the future they should be loaded in automatically from some
# folder.)
