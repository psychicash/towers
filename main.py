import pygame
from pygame import freetype
import random
from math import sin, cos, pi, atan2, degrees

#import sys
import xlsxwriter
import xlrd
import numpy as np

import astar_path
import wang
import wire_placement

from library1 import get_image
from library1 import myround
from terrain import Cl_Terrain
from bunker import Cl_Bunker
from launcher import Cl_Launcher
from tower import Cl_Tower

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
DEBUG = False



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
            if DEBUG:
                print("Launch_local set to " + str(launch_local))

            if not (launch_local in self.tower_pool):
                if DEBUG:
                    print("launch local not found in tower pool, appending launch_local")
                self.launcher_location = launch_local
        while len(self.bunker_location) == 0:
            bunk_local = random.choice(self.inner_ring)
            if DEBUG:
                print("Bunker local set to " + str(bunk_local))

            if not (bunk_local in self.tower_pool):
                if DEBUG:
                    print("Bunk local not found in tower pool")
                self.bunker_location = bunk_local

    def random_obsticals(self):
        pass

    def enemy_army(self):
        self.enemy_army_numbers = (level * self.num_of_towers) * 100000
        self.enemy_hard_targets = (level * self.num_of_towers) * (100/random.choice(range(1,100)))



class Game(object):                                     #class reps an instance of the game
    def __init__(self, screen):                                 #creates all attributes of the game
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
        self.screen = screen
        self.terrain_list = list()
        self.terrain = wang.wang_set(width = 12, height = 7)
        self.game_running = True
        self.menu_sprites = pygame.sprite.Group()
        self.terrain_sprites = pygame.sprite.Group()

        for i in range(len(self.terrain)):
            for j in range(len(self.terrain[0])):
                x = i
                y = j
                value = self.terrain[i][j]

                self.terrain_list.append(Cl_Terrain(x, y, value))
                self.terrain_sprites.add(self.terrain_list[-1])
        self.BG1 = get_image('./images/sprites/background.png')
        if DEBUG == True:
            print(np.matrix(self.terrain))
            print("Above is the terrain spread")
        self.all_sprites_list = pygame.sprite.Group()         #create sprite lists
        self.bar_sprite_list = pygame.sprite.Group()
        self.level = Level(level=1)
        self.level.random_tower_local()
        self.towers = []
        self.wire_locations = []
        self.tower_sprite_list = pygame.sprite.Group()
        self.bunker = Cl_Bunker(self.level.bunker_location[0], self.level.bunker_location[1])
        self.all_sprites_list.add(self.bunker)
        self.grid[self.level.bunker_location[0]][self.level.bunker_location[1]] = 'B'
        self.grid[self.level.launcher_location[0]][self.level.launcher_location[1]] = 'L'
        self.launcher = Cl_Launcher(self.level.launcher_location[0], self.level.launcher_location[1] )
        self.all_sprites_list.add(self.launcher)
        self.tower_generation(self.level.num_of_towers)
        self.wire_loc = wire_placement.wire_placement(self.grid, self.towers, self.wire_locations)
        self.wires_group = pygame.sprite.Group()
        for i in range(len(self.wire_loc)):
            self.wires_group.add(self.wire_loc[i])
        self.wire_show = False
        self.last_time = pygame.time.get_ticks()
        self.cooldown = 400  # cool down
        self.is_menu_open = False

    def wire_toggle(self):
        now = pygame.time.get_ticks()
        if now - self.last_time >= self.cooldown:
            sound = pygame.mixer.Sound('./sound/menuclick.wav')
            sound.play()
            self.last_time = now
            if self.wire_show == False:
                self.wire_show = True
            elif self.wire_show == True:
                self.wire_show = False

    def set_wires_on_ground(self):
        #for i in range(len(self.towers)):
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
            #i know this is a long line of code but... pathfinding needs stuff passed to it...
            self.towers[i].initial_path = astar_path.astar(self.grid, start= self.level.bunker_location, end= (self.towers[i].location[0][0], self.towers[i].location[0][1]))
            print(self.towers[i].initial_path)
            temp = []
            for j in range(len(self.towers[i].initial_path)):
                if j is 0:
                    pass
                else:
                    temp.append(self.towers[i].initial_path[j])

            self.tower_sprite_list.add(self.towers[i])
            self.all_sprites_list.add(self.towers[i])
            self.wire_locations.append(temp)



        self.tower_cleanup()

    def tower_cleanup(self):
        #for loop for all T's in grid grab location and remove all values of self.towers that match 0
        for set in self.towers:
            if self.grid[set.location[0][0]][set.location[0][1]] is 0:
                self.towers.remove(set)
        if len(self.towers) < self.level.num_of_towers:
            x = self.level.num_of_towers - len(self.towers)
            self.tower_generation(x)
        elif len(self.towers) == self.level.num_of_towers:
            pass





    def process_events(self):                           #process all the events and return true if we close the window
        pygame.event.pump()
        keyinput = pygame.key.get_pressed()
        mouseinput = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()


        if keyinput[pygame.K_ESCAPE]:
            raise SystemExit
        if mouseinput[0] is 1:
            if mouse_pos[0] > 100 and mouse_pos[0] < 350 and mouse_pos[1] > 770 and mouse_pos[1] < 825:
                self.wire_toggle()

        for s in self.tower_sprite_list:
            if s.rect.collidepoint(mouse_pos):
                if mouseinput[0] == 1:
                    s.menu_open(game)
        if self.is_menu_open:
            for s in self.menu_sprites:
                if s.rect.collidepoint(mouse_pos):
                    if mouseinput[0] == 1:
                        s.clicked(game)




    def run_logic(self):                                #method runs each frame and updates positions
        if not self.game_over:                          #and checks for collisions
            for s in self.all_sprites_list:
                try:
                    s.update(game)
                except:
                    s.update() # move all sprites
            for s in self.all_sprites_list:
                try:
                    s.bar_idle(game)
                except:
                    pass
                finally:
                    pass
            self.menu_sprites.update()







    def display_frame(self, screen):
            screen.fill(DK_GREEN)
            screen.blit(self.BG1, [0,0])



            #todo display and level information
            #todo customize game over window

            if self.game_over:                      #game over text on screen
                text_var = pygame.freetype.Font('./images/font/future_thin.ttf', 16, False, False)
                text_var2 = text_var.render("Game Over, click to restart", fgcolor = BLACK)
                center_x = (SCREEN_WIDTH // 2) - (text_var2[0].get_width() // 2)
                center_y = (SCREEN_HEIGHT // 2) - (text_var2[0].get_height() // 2)
                screen.blit(text_var2[0], [center_x, center_y])

            elif self.game_running:
                self.terrain_sprites.draw(screen)
                self.all_sprites_list.draw(screen)
                if self.wire_show:
                    self.wires_group.draw(screen)
                if self.is_menu_open:
                    self.menu_sprites.draw(screen)
                self.bar_sprite_list.draw(screen)
            pygame.display.flip()






def main():

    screen = pygame.display.set_mode([1600, 900])                  #comment this out and uncomment the fullscreen

    #screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    #TODO make fullscreen toggle and make images scale with the playing field

    pygame.display.set_caption('') #TODO make a title for the window

    pygame.mouse.set_visible(True)

    #create our objects and set data
    done = False
    clock = pygame.time.Clock()

    #creates gme instance
    global game
    game = Game(screen)

    if DEBUG:
        print(np.matrix(game.grid))
        print("above is the grid")

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

if __name__ == '__main__':
    main()