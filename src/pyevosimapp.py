'''
Created on Sep 28, 2011

@author: garrison
'''

from utils.coords import Coords
from boardelements import Monster,FOOD
from simulator import Simulation
from constants import APPNAME,VERSION
from utils.pygameutils import PygameApp
from utils.misc import Config
import pygame

CAPTION = APPNAME+" v"+VERSION

class SimulationApp(PygameApp):
    """
    This class contains all the GUI code for the PyEvoSim.
    
    It can be easily used as follows:
    SimulationApp.run()
    """
    def __init__(self):
        self.gfxConfig = Config("gfxconfig.py")
        PygameApp.__init__(self,displaySize=(1,1),maxFramerate=self.gfxConfig.MAX_FRAMERATE,caption=CAPTION,defaultColorKey=self.gfxConfig.COLOR_KEY)
        self.newSimulation()
        self.monsterImage = self.loadImage("monster.png")
        self.followedMonsterImage = self.loadImage("followedmonster.png")
        self.foodImage = self.loadImage("meat.png")
    
    def newSimulation(self):
        """
        Creates a new simulation (loading or reloading the config files). This
        is called when the app is first started, but also when F2 is pressed.
        """
        self.simConfig = Config("default_config.py","config.py")
        self.simulation = Simulation(self.simConfig)
        tileWidth = self.gfxConfig.TILE_WIDTH
        self.displaySize = (self.simConfig.BOARD_WIDTH*tileWidth,self.simConfig.BOARD_HEIGHT*tileWidth)
        self.autoplaying = False
    
    @property
    def autoplaying(self):
        return self._autoplaying
    
    @autoplaying.setter
    def autoplaying(self,newValue):
        self._autoplaying = newValue
        if newValue == True:
            self.caption = CAPTION+" (running)"
        else:
            self.caption = CAPTION
    
    def step(self):
        """
        Called every frame. Updates the simulation if it is autoplaying.
        """
        if self.autoplaying:
            self.simulation.oneStep()
    
    def draw(self,screen):
        # Draw stuff
        tileWidth = self.gfxConfig.TILE_WIDTH
        screen.fill(self.gfxConfig.BACKGROUND_COLOR)
        for coords,boardElement in self.simulation.iteritems():
            drawCoords = coords * tileWidth
            if boardElement == FOOD:
                screen.blit(self.foodImage,drawCoords)
            elif isinstance(boardElement,Monster):
                fillRect = pygame.Rect(drawCoords,(tileWidth,tileWidth))
                screen.fill(boardElement.color,fillRect)
                if boardElement.followed:
                    screen.blit(self.followedMonsterImage,drawCoords)
                else:
                    screen.blit(self.monsterImage,drawCoords)
    
    def on_quit(self,event):
        self.quit()
    def on_keyDown_escape(self,event):
        self.quit()
    
    def on_keyDown_space(self,event):
        if not self.autoplaying:
            self.simulation.oneStep()
    
    def on_keyDown_f2(self,event):
        self.newSimulation()
    
    def on_keyDown_return(self,event):
        self.autoplaying = not self.autoplaying
    
    def on_mouseButtonDown_left(self,event):
        """
        Outputs information about the monster under the cursor.
        Only works when not autoplaying.
        """
        if not self.autoplaying:
            screenCoords = Coords.make(event.pos)
            boardCoords = screenCoords // self.gfxConfig.TILE_WIDTH
            boardElement = self.simulation.get(boardCoords)
            if isinstance(boardElement,Monster):
                print "<{0}, {1}>".format(boardElement.infoString,boardCoords)
    
    def on_mouseButtonDown_right(self,event):
        """
        Follows or unfollows the monster under the cursor (naming it if it has
        not been named).
        Only works when not autoplaying.
        """
        if not self.autoplaying:
            screenCoords = Coords.make(event.pos)
            boardCoords = screenCoords // self.gfxConfig.TILE_WIDTH
            boardElement = self.simulation.get(boardCoords)
            if isinstance(boardElement,Monster):
                self.simulation.toggleMonsterFollowed(boardElement)
