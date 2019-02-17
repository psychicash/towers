import pygame
from pygame import freetype
import os
import random
from math import sin, cos, pi, atan2, degrees
import os.path
from os import path
import sys
import xlsxwriter
import xlrd
import numpy as np

import astar_path
import wang









pygame.init()
if not pygame.display.get_init():
    pygame.display.init()
if not pygame.freetype.was_init():
    pygame.freetype.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()


#---------CONSTANTS
FPSCLOCK = pygame.time.Clock() #sets up a clock used for throttleing the fps
BOARDWIDTH = 12
BOARDHEIGHT = 7
TILESIZE = 100
FPS = 60
BLANK = None




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

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900



_image_library = {}

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
    return image


def get_angle(origin, destination):
    """Returns angle in radians from origin to destination.
    This is the angle that you would get if the points were
    on a cartesian grid. Arguments of (0,0), (1, -1)
    return .25pi(45 deg) rather than 1.75pi(315 deg).
    """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return atan2(-y_dist, x_dist) % (2 * pi)



def project(pos, angle, distance):
    """Returns tuple of pos projected distance at angle
    adjusted for pygame's y-axis.
    """
    return (pos[0] + (cos(angle) * distance),
            pos[1] - (sin(angle) * distance))
#TODO fix looking up rect values in dictionary
def find_rect(key1, key2):
    for key1, p_info in grid_dict.grid_squares.items():
        for key2 in p_info:
            return p_info[key2]



#######################
########   Classes
#########################
class Level(object):
    def __init__(self, level = 1):

        self.level_num = level
        self.outter_ring = [[0,0], [0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [0,7],[0,8], [0,9], [0,10], [0,11], 
                            [1,0], [1,1], [1,2], [1,3], [1,4], [1,5], [1,6], [1,7],[1,8], [1,9], [1,10], [1,11],
                            [2,0], [2,1], [2,2], [2,9], [2,10], [2,11],
                            [3,0], [3,1], [3,2], [3,9], [3,10], [3,11],
                            [4,0], [4,1], [4,2], [4,9], [4,10], [4,11],
                            [5,0], [5,1], [5,2], [5,3], [5,4], [5,5], [5,6], [5,7], [5,8], [5,9], [5,10], [5,11],
                            [6,0], [6,1], [6,2], [6,3], [6,4], [6,5], [6,6], [6,7], [6,8], [6,9], [6,10], [6,11]
                            ]
        self.inner_ring = [[2,3], [2,4], [2,5], [2,6], [2,7], [2,8],
                           [3,3], [3,4], [3,5], [3,6], [3,7], [3,8],
                           [4,3], [4,4], [4,5], [4,6], [4,7], [4,8],
                           ]
        self.all_coords = [ [0,0], [0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [0,7], [0,8], [0,9], [0,10], [0,11],
                            [1,0], [1,1], [1,2], [1,3], [1,4], [1,5], [1,6], [1,7], [1,8], [1,9], [1,10], [1,11],
                            [2,0], [2,1], [2,2], [2,3], [2,4], [2,5], [2,6], [2,7], [2,8], [2,9], [2,10], [2,11],
                            [3,0], [3,1], [3,2], [3,3], [3,4], [3,5], [3,6], [3,7], [3,8], [3,9], [3,10], [3,11],
                            [4,0], [4,1], [4,2], [4,3], [4,4], [4,5], [4,6], [4,7], [4,8], [4,9], [4,10], [4,11],
                            [5,0], [5,1], [5,2], [5,3], [5,4], [5,5], [5,6], [5,7], [5,8], [5,9], [5,10], [5,11],
                            [6,0], [6,1], [6,2], [6,3], [6,4], [6,5], [6,6], [6,7], [6,8], [6,9], [6,10], [6,11]
                           ]
        self.tower_pool = []
        self.launcher_location = []
        self.bunker_location = []
        self.num_of_towers = 4


    def random_tower_local(self):
        self.tower_pool = [sample for sample in random.sample(self.outter_ring, k=10)] + [s for s in random.sample(self.inner_ring, k=4)]
        self.tower_pool.sort()
        while len(self.launcher_location) == 0:
            launch_local = random.choice(self.outter_ring)
            print("Launch_local set to " + str(launch_local))

            if not (launch_local in self.tower_pool):
                print("launch local not found in tower pool, appending launch_local")
                self.launcher_location = launch_local
        while len(self.bunker_location) == 0:
            bunk_local = random.choice(self.inner_ring)
            print("Bunker local set to " + str(bunk_local))

            if not (bunk_local in self.tower_pool):
                print("Bunk local not found in tower pool")
                self.bunker_location = bunk_local

class Cl_Tower(pygame.sprite.Sprite):
    def __init__(self, tower_pool_local):
        pygame.sprite.Sprite.__init__(self)
        self.creation_time = pygame.time.get_ticks()
        self.detection_level = 0.0
        self.health = 0
        self.location = [tower_pool_local]
        self.detection_level_max = 100
        self.state = ['sending', 'receiving', 'resting']
        self.base_detection_gain = 1.0
        self.images = []
        img = get_image('./images/sprites/blue_tower_wdish.gif')
        self.images.append(img)
        img = get_image('./images/sprites/green_tower_wdish.gif')
        self.images.append(img)
        img = get_image('./images/sprites/red_tower_wdish.gif')
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        #TODO - set x and y according to grid location on the screen
        #self.rect.x =
        #self.rect.y =
        self.last = pygame.time.get_ticks()
        self.initial_path = []
        self.current_state = self.state[2]

    def resting_state(self):
        self.detection_level -= 1
        self.image = self.images[0]
        self.current_state = self.state[2]

    def sending_state(self):
        self.detection_level += self.base_detection_gain
        self.image = self.images[2]
        self.current_state = self.state[0]

    def receiving_state(self):
        self.detection_level += (self.base_detection_gain / 4)
        self.image = self.images[1]
        self.current_state = self.state[1]

    def update(self):
        pass


class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = get_image(filename)
        except pygame.error as message:
            print('Unable to load spritesheet image:' + filename)
            raise SystemExit
    # Load a specific image from a specific rectangle

    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list

    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images

    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

class Cl_Bunker(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.location = []
        self.location.append(x)
        self.location.append(y)

        img = get_image('./images/sprites/bunker_icon.png')
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = (self.location[1] * 100) + 100
        self.rect.y = (self.location[0] * 100) + 50

class Cl_Launcer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.location = []
        self.location.append(x)
        self.location.append(y)
        img = get_image('./images/sprites/launcher_icon.png')
        self.image = img
        self.rect = self.image.get_rect()

        self.rect.x = (self.location[1] * 100) + 100
        self.rect.y = (self.location[0] * 100) + 50

class Cl_Terrain(pygame.sprite.Sprite):
    def __init__(self, x, y, value):
        pygame.sprite.Sprite.__init__(self)
        self.location = []
        self.location.append(x)
        self.location.append(y)
        img = []
        img.append(get_image(self.set_terrain_image(value)))
        self.image = img[0]
        self.rect = self.image.get_rect()
        self.rect.x = (self.location[1] * 100) + 100
        self.rect.y = (self.location[0] * 100) + 50

    def set_terrain_image(self, value):
        if value == 0:
            return './images/sprites/terrain/tile000.png'
        elif value == 1:
            return './images/sprites/terrain/tile001.png'
        elif value == 2:
            return './images/sprites/terrain/tile002.png'
        elif value == 3:
            return './images/sprites/terrain/tile003.png'
        elif value == 4:
            return './images/sprites/terrain/tile004.png'
        elif value == 5:
            return './images/sprites/terrain/tile005.png'
        elif value == 6:
            return './images/sprites/terrain/tile006.png'
        elif value == 7:
            return './images/sprites/terrain/tile007.png'
        elif value == 8:
            return './images/sprites/terrain/tile008.png'
        elif value == 9:
            return './images/sprites/terrain/tile009.png'
        elif value == 10:
            return './images/sprites/terrain/tile010.png'
        elif value == 11:
            return './images/sprites/terrain/tile011.png'
        elif value == 12:
            return './images/sprites/terrain/tile012.png'
        elif value == 13:
            return './images/sprites/terrain/tile013.png'
        elif value == 14:
            return './images/sprites/terrain/tile014.png'
        elif value == 15:
            return './images/sprites/terrain/tile015.png'



    
class Game(object):                                     #class reps an instance of the game
    def __init__(self):                                 #creates all attributes of the game
        self.game_over = False
        self.grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.terrain_list = list()
        self.terrain = wang.wang_set(width = 12, height = 7)
        print(self.terrain)
        print(self.terrain[4][5])
        self.terrain_sprites = pygame.sprite.Group()

        for i in range(len(self.terrain)):
            for j in range(len(self.terrain[0])):
                x = i
                y = j
                value = self.terrain[i][j]

                self.terrain_list.append(Cl_Terrain(x, y, value))
                self.terrain_sprites.add(self.terrain_list[-1])


        self.wire_image = []
        self.set_wire_images()
        self.set_wire_images()
        self.wire_locations = []
        self.all_sprites_list = pygame.sprite.Group()         #create sprite lists
        self.level = Level(level=1)
        self.level.random_tower_local()
        self.towers = []
        self.tower_sprite_list = pygame.sprite.Group()
        self.bunker = Cl_Bunker(self.level.bunker_location[0], self.level.bunker_location[1])
        self.all_sprites_list.add(self.bunker)
        self.grid[self.level.bunker_location[0]][self.level.bunker_location[1]] = 'B'
        self.grid[self.level.launcher_location[0]][self.level.launcher_location[1]] = 'L'
        self.launcher = Cl_Launcer(self.level.launcher_location[0], self.level.launcher_location[1] )
        self.all_sprites_list.add(self.launcher)
        self.tower_generation(self.level.num_of_towers)


    def set_wire_images(self):
        self.wire_ss = spritesheet('./images/sprites/wangtiles.png')
        for i in range(0,4):
            for j in range(0, 4):
                image = self.wire_ss.image_at(rectangle = (0 + (100 * i), 0 + (100 * j), 99 + (100 * i), 99 + (100 * j)))
                self.wire_image.append(image)




    def set_wires_on_ground(self):
        #for i in range(len(self.towers)):
        pass


    def set_tower_images(self):
        pass



    def tower_generation(self, qty):
        print("Tower generation stage 1...")
        for i in range(qty):
            z = random.choice(self.level.tower_pool)
            self.towers.append(Cl_Tower(z))
            x = self.towers[i].location[0][0]
            y = self.towers[i].location[0][1]
            self.towers[i].rect.x = y * 100 + 100
            self.towers[i].rect.y = x * 100 + 50
            self.grid[x][y] = 'T'

        print("Tower generation stage 1 complete")
        print("Prepare for stage 2...")
        for i in range(len(self.towers)):
            self.towers[i].initial_path = astar_path.astar(self.grid, start= self.level.bunker_location, end= (self.towers[i].location[0][0], self.towers[i].location[0][1]))
            print(self.towers[i].initial_path)
            self.tower_sprite_list.add(self.towers[i])
            self.all_sprites_list.add(self.towers[i])
            self.wire_locations.append(self.towers[i].initial_path)



        self.tower_cleanup()

    def tower_cleanup(self):
        #for loop for all T's in grid grab location and remove all values of self.towers that match 0
        for set in self.towers:
            if self.grid[set.location[0][0]][set.location[0][1]] == 0:
                self.towers.remove(set)
        if len(self.towers) < self.level.num_of_towers:
            x = self.level.num_of_towers - len(self.towers)
            self.tower_generation(x)
        elif len(self.towers) == self.level.num_of_towers:
            pass





    def process_events(self):                           #process all the events and return true if we close the window
        pygame.event.pump()
        keyinput = pygame.key.get_pressed()
        if keyinput[pygame.K_ESCAPE]:
            raise SystemExit



    def run_logic(self):                                #method runs each frame and updates positions
        if not self.game_over:                          #and checks for collisions

            self.all_sprites_list.update()              #move all sprites









    def display_frame(self, screen):
            screen.fill(DK_GREEN)
            #screen.blit(BG1, [0,0])


            #todo display player lives and level information
            #todo customize game over window

            if self.game_over:                      #game over text on screen
                text_var = pygame.freetype.Font('./images/font/future_thin.ttf', 16, False, False)
                text_var2 = text_var.render("Game Over, click to restart", fgcolor = BLACK)
                center_x = (SCREEN_WIDTH // 2) - (text_var2[0].get_width() // 2)
                center_y = (SCREEN_HEIGHT // 2) - (text_var2[0].get_height() // 2)
                screen.blit(text_var2[0], [center_x, center_y])

            if not self.game_over:
                self.terrain_sprites.draw(screen)
                self.all_sprites_list.draw(screen)


            pygame.display.flip()






def main():
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    #screen = pygame.display.set_mode([1600, 900])                  #comment this out and uncomment the fullscreen
    #TODO make fullscreen toggle and make images scale with the playing field
    pygame.display.set_caption('') #TODO make a title for the window

    pygame.mouse.set_visible(True)

    #create our objects and set data
    done = False
    clock = pygame.time.Clock()

    #creates gme instance
    global game
    game = Game()

    print(np.matrix(game.grid))
    # for i in range(0,7,1):
    #     for j in range (0, 11, 1):
    #         grid_squares(screen= screen, coords = (j, i))
    # print("\n Printing Grid dict")
    # print(grid_dict)
    #TODO title screen insert here

    #main game loop
    while not done:
        #process events
        done = game.process_events()
        #update stuff
        game.run_logic()
        #draw
        game.display_frame(screen)
        #pause for the next frame
        clock.tick(60)


    pygame.quit() # closes window and exits

#BG1 = get_image('') #TODO set file path for background image
#call the main function and start up the game

if __name__ == '__main__':
    main()




#TODO startup screen / movie intro
#TODO Title Screen
#TODO Controls - setup mouse controls - collision of sprite group with mouse runs function of class display menu
#TODO setup game screen
#TODO setup level creation -
'''10% to 20% are water (+5% per skill increase)
     8 to 17 squares have water in them
solid 90% to 80%
	30% to 25%are grass
	40% to 35% dirt
	20% sand
'''
#TODO randomly seclect site for bunker on map in the inner circle
#TODO randomly select 10 tower sites on the outter and 4 on the inner
#TODO randomly select sites for obsticles - hills, trees, buildings, vehicles 10 to 20% of the dirt blocks
# are set aside for hills trees buildings and vehicles and 5 to 10% of the grass blocks for vehicles
# buildings and trees

#TODO random location sleected for missle truck
#TODO calculate the path from station to tower location and assign to lines for all but 3 of the potential
#tower locations
#max mountains is 7

'''

max mountains is 7...
morse code is sent when enough towers are active to send signal  take the number of hills total and convert that to percent.  then multiply by the level and floor it,  and that gives you the number of extra towers beyond 1 needed for transmission

number of lines transmitted and recieved and transmitted is equal to 2 * level the number per action

ex: level 1 - transmitting 2 lines, recieve 2 lines, transmit 2 lines - firing solution calculation - fire

generic morse code sound plays while sending and then a quieter one plays while recieving
red light goes hot on bunker when transmitting
green light when no activity 
blue light when recieving


detection meter = 0 to 100% ... 100% fires missle towards tower with a random time of 10 seconds to 20 seconds counting down over the tower 
dm is gained while transmitting at a rate of some amount per active frame
dm is lost while inactive down to half it's highest value
dm is gained at half value while reciving

missle fires at tower, tower doesn't move it gets destroyed, can be repaired/fixed once with a spare part powerup
missle fires at tower, tower moves, bomb explodes, destroyes the 9 blocks around it and the target block with impact crater
wire is broken for those squares, can move towers inward

if 4+ towers are within a certain number of squares (10) then the base gains detection at 1/8 the rate of the active towers 

fire missle to win 

powerup processing power gives 10% boost to formula calculation

after each level, + points to score for the following

# of towers undetected
base undetected at all
# of towers standing
# of towers in original location

lose points for lost bunker, tower, missle truck 

purchase powerups between levels

each additional level subtracts 0.05% from the ceiling of the dm max penalty is 50%
each additional level adds possible interferance

*maybe add weather issues

each additional level gives computer opponent faster reloads
each additional level gives slower reloads on truck
each additional level gives more targets and increases the timer tick rate


controls are as follows, left click on inactive wire to activate and left click again to reactivate

click on tower to pull up tower menu, (options: power off/on, move, repair (if damaged), 
click on missle truck to pull up truck menu (options: request firing solution, request reload, move)
click on bunker to pull up menu (radio silence on/off, transmit, recieve, compute firing solution)

click on broken wire to slect repair if repair is available

screen has the following readouts

main grid

current battle info : number of soldiers vs number of robots/aliens
number of targets needed to turn the tide fo the battle
ammo available limited number of shots (can request resupply - takes time, increases detection by lowering max detection fro the round by 5%)

tower/truck readout 


3 levels created on new game
1 level created every level after (starting points)



POWERUP ideas - faster cpu - increases fire solution calculation
    

'''





