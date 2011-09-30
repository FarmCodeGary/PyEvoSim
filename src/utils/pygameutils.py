'''
This module provides miscellaneous tools for use with pygame.

Created on Sep 28, 2011

@author: garrison
'''

import pygame as _pygame
from coords import Coords

def mouseButtonName(buttonNum):
    """
    Returns the name of the given mouse button number. (This is intended to be
    used with the "button" or "buttons" property of pygame mouse events.)
    
    It will return one of the following: "left", "middle", "right", "scrollUp",
    "scrollDown", or "other".
    """
    if buttonNum == 1:
        return "left"
    elif buttonNum == 2:
        return "middle"
    elif buttonNum == 3:
        return "right"
    elif buttonNum == 4:
        return "scrollUp"
    elif buttonNum == 5:
        return "scrollDown"
    else:
        return "other"

def handlePygameEvents(handlerObj):
    """
    This function will call methods on the given handlerObj to handle the
    events on pygame's event queue.
    
    handlerObj can optionally define methods with the following names to serve
    as handlers:
    on_quit
    on_keyDown
    on_keyDown_space # replace "space" with the name of the key
    on_keyUp
    on_keyUp_f4      # replace "f4" with the name of the key
    on_mouseButtonDown
    on_mouseButtonDown_left # replace "left" with the name of the button
    on_mouseButtonUp
    on_mouseButtonUp_middle # replace "middle" with the name of the button
    on_mouseMotion
    
    Each method should take the pygame event as a parameter.
    """
    for event in _pygame.event.get():
        if event.type == _pygame.QUIT:
            try:
                handler = handlerObj.on_quit
            except AttributeError: pass
            else:
                handler(event)
        
        elif event.type == _pygame.KEYDOWN:
            # General handler
            try:
                handler = handlerObj.on_keyDown
            except AttributeError: pass
            else:
                handler(event)
            
            # Specific handler
            keyName = _pygame.key.name(event.key)
            try:
                handler = getattr(handlerObj,"on_keyDown_"+keyName)
            except AttributeError: pass
            else:
                handler(event)
        
        elif event.type == _pygame.KEYUP:
            # General handler
            try:
                handler = handlerObj.on_keyUp
            except AttributeError: pass
            else:
                handler(event)
            
            # Specific handler
            keyName = _pygame.key.name(event.key)
            try:
                handler = getattr(handlerObj,"on_keyUp_"+keyName)
            except AttributeError: pass
            else:
                handler(event)
        
        elif event.type == _pygame.MOUSEBUTTONDOWN:
            # General handler
            try:
                handler = handlerObj.on_mouseButtonDown
            except AttributeError: pass
            else:
                handler(event)
            # Specific handler
            buttonName = mouseButtonName(event.button)
            try:
                handler = getattr(handlerObj,"on_mouseButtonDown_"+buttonName)
            except AttributeError: pass
            else:
                handler(event)
        
        elif event.type == _pygame.MOUSEBUTTONUP:
            # General handler
            try:
                handler = handlerObj.on_mouseButtonUp
            except AttributeError: pass
            else:
                handler(event)
            # Specific handler
            buttonName = mouseButtonName(event.button)
            try:
                handler = getattr(handlerObj,"on_mouseButtonUp_"+buttonName)
            except AttributeError: pass
            else:
                handler(event)
        
        elif event.type == _pygame.MOUSEMOTION:
            try:
                handler = handlerObj.on_mouseMotion
            except AttributeError: pass
            else:
                handler(event)


class PygameApp(object):
    """
    This class provides a basic framework for a Pygame application.
    Most subclasses will only need to override step and draw, plus provide some
    handler methods in the format used by the handlePygameEvents function
    provided in this module. A subclass will also want to provide the desired
    constructor parameters for the screen size, caption, framerate, etc.
    
    A PygameApp can be easily launched using the class method run.
    """
    @classmethod
    def run(cls,*args,**kwargs):
        """
        This method can easily be used to run a PygameApp, without having to
        construct it and run the mainLoop manually. For example:
        
        class MyPygameApp(PygameApp):
            def __init__(self,arg1,arg2,**kwargs)
        MyPygameApp.run(3,4,name="Biscuit")
        """
        app = cls(*args,**kwargs)
        app.mainLoop()
    
    def __init__(self,displaySize,maxFramerate=30,caption="Pygame App",defaultColorKey=None):
        """
        Constructs a PygameApp with the given attributes.
        
        defaultColorKey is a pygame color which, if provided, will
        automatically be used as the color key for images loaded with the
        loadImage method.
        """
        _pygame.init()
        self.displaySize = displaySize
        self.defaultColorKey = defaultColorKey
        self.maxFramerate = maxFramerate
        self.caption = caption
        self._clock = _pygame.time.Clock()
    
    @property
    def displaySize(self):
        return Coords.make(self.screen.rect.size)
    
    @displaySize.setter
    def displaySize(self,size):
        self._screen = _pygame.display.set_mode(size)
    
    @property
    def caption(self):
        return _pygame.display.get_caption()
    
    @caption.setter
    def caption(self,newValue):
        _pygame.display.set_caption(newValue)
    
    def loadImage(self,filename,colorKey=None):
        """
        Returns a pygame surface of the image in the given filename.
        The image will be converted to the correct format.
        
        If the colorKey parameter is given, it will be set as the color key for
        the image. If not, the PygameApp's defaultColorKey attribute will be
        used, unless defaultColorKey is None, in which case the color key is
        not set.
        """
        image = _pygame.image.load(filename).convert()
        if colorKey:
            image.set_colorkey(colorKey)
        elif self.defaultColorKey:
            image.set_colorkey(self.defaultColorKey)
        return image
    
    def mainLoop(self):
        """
        Run this PygameApp until the quit method is called.
        """
        self._quitFlag = False
        while not self._quitFlag:
            self._fullStep()
    
    def on_quit(self,event):
        """
        Provides a default behavior for a pygame QUIT event, which is to call
        self.quit().
        """
        self.quit()
    
    def quit(self):
        """
        Stops the program at the end of the current step.
        
        (To quit immediately, use sys.exit().)
        """
        self._quitFlag = True
    
    def _fullStep(self):
        """
        Runs one full step of the mainLoop.
        This method probably shouldn't need to be overridden.
        """
        self.tick()
        handlePygameEvents(self)
        self.step()
        self.draw(self._screen)
        _pygame.display.flip()
    
    def step(self):
        """
        Override this method to specify code that will be executed every step
        of the mainLoop. This is for updating the locations of entities, etc.,
        but NOT for drawing code. (Put drawing code in the draw method.)
        """
        pass
    
    def tick(self):
        """
        Called at the beginning of every step. Causes the program to wait, in
        order to keep the framerate below the maximum.
        
        This method could be overridden to implement some other framerate-
        management approach.
        """
        self._clock.tick(self.maxFramerate)
    
    def draw(self,screen):
        """
        Override this method to specify how the PygameApp subclass is drawn.
        """
        pass


class PygameTestApp(PygameApp):
    """
    This simple app is used to check for the name and unicode for keys pressed,
    and the numbers and names of mouse buttons pressed. (This information will
    be printed in the console.)
    """
    def __init__(self):
        PygameApp.__init__(self, (400,200), caption="Pygame Test App (type and click)")
    def on_keyDown(self,event):
        print event
    def on_mouseButtonDown(self,event):
        print event," (button name: "+mouseButtonName(event.button)+")"

if __name__ == "__main__":
    PygameTestApp.run()
