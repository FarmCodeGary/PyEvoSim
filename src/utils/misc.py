'''
This module defines miscellaneous utilities that don't fit into another module,
but are too trivial for a new module.

Created on Sep 29, 2011

@author: garrison
'''

class Config(dict):
    """
    This class provides a dead-simple mechanism for loading config files
    written in Python. The constructor takes in any number of filenames,
    and "reads" them into the Config object in the given order.
    
    Options can be defined in one file and overwritten in another. This is
    useful if you load a default config file, then a user config file.
    
    Options can be read from the config option using either member access or
    dict-style key access.
    
    For an example, suppose you have the following three lines in a file called
    "gameconfig.py":
    SAVE_LOCATION = "~/AwesomeGameSaves"
    RESOLUTION = 1024,768
    USERS = ["Guybrush","Murray","LeChuck"]
    
    You could then execute the following code:
    config = Config("gameconfig.py")
    print config.SAVE_LOCATION
    print config["SAVE_LOCATION"]
    for user in config.USERS:
        print user
    
    NOTE that the config files should NEVER contain any untrusted code. This
    class is not suitable for production applications, only quick-and-dirty
    ones.
    """
    def __init__(self,*filenames):
        """
        Creates a Config object, loading from one or more filenames in the
        given order.
        """
        dict.__init__(self)
        for filename in filenames:
            execfile(filename,self)
    
    def __getattr__(self,name):
        try:
            value = self[name]
        except KeyError:
            raise AttributeError
            # TODO: Make the AttributeError include more useful information.
        else:
            return value
    