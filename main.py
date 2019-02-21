### Third Party library imports
import pygame
from pygame import freetype
from math import sin, cos, pi, atan2, degrees
import numpy as np 

### Personal libraries
from my_lib import get_image
from my_lib import myround

### game files
from terrain import Cl_Terrain
from bunker import Cl_Bunker
from launcher import Cl_Launcher
from tower import Cl_Tower
import cl_level


#initializers
pygame.init()
if not pygame.display.get_init():
    pygame.display.init()
if not pygame.freetype.was_init():
    pygame.freetype.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()

#constants

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 225
FPSCLOCK = pygame.time.Clock() #sets up a clock used for throttleing the fps
BOARDWIDTH = 12
BOARDHEIGHT = 7
TILESIZE = 100
FPS = 60
BLANK = None
DEBUG = False


#color constants
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (12, 255, 0)
DK_GREEN = (51, 102, 0)
BLUE = (18, 0, 255)
ORANGE = (255, 186, 0)
SKYBLUE = (39, 145, 251)
PURPLE = (153, 51, 255)
DK_PURPLE = (102, 0, 204)
BROWN = (204, 153, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#GLOBALS
_Current_scene = 'Title'
_Fullscreen_flag = False
_Multiplier = 4

class Cl_Scene_controller():
    def __init__(self):
        last_scene = ''
        initial_scene_class = getattr('Cl_' + _Current_scene)
        create_instance(_Current_scene, initial_scene)

    def create_instance(self, name_of_object, name_of_class, *args):
        getattr(name_of_object) = getattr(name_of_class)(*args)

    def scene_controller(str:scene):
        getattr(last_scene).kill()
        last_scene = scene
        global getattr('scene')
        _Current_scene = scene
        new_class = getattr('Cl_' + scene)
        create_instance(scene, new_class)
    
    def process_events(screen):
        getattr(_Current_scene).process_events(screen)
    
    def run_logic():
        getattr(_Current_scene).run_logic()



#follow the rabit hole, all classes run their calls to functions in game and main talks to game

def main():
    if _Fullscreen_flag == True:
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    else: 
        screen = pygame.display.set_mode([SCREEN_WIDTH * _Multiplier, SCREEN_HEIGHT * _Multiplier])              

    pygame.display.set_caption('Firing Solution') #TODO make a title for the window
    pygame.mouse.set_visible(True)

    #create our objects and set data
    done = False
    global scene_controller
    scene_controller = Cl_Scene_controller()

    while not done:
        #process events
        scene_controller.process_events(screen)
        #update stuff
        scene_controller.run_logic()
        #draw
        scene_controller.display_frame(screen)
        #pause for the next frame

        FPSCLOCK.tick(60)


    pygame.quit() # closes window and exits

if __name__ == '__main__':
    main()
