import pygame
from pygame import freetype

import random
from math import sin, cos, pi, atan2, degrees

import sys
import xlsxwriter
import xlrd
import numpy as np

import astar_path
import wang
import wire_placement
from wire_placement import get_image



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




def myround(x, base=5):
    return (base * round(float(x)/base))

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







class Cl_Tower(pygame.sprite.Sprite):
    def __init__(self, tower_pool_local):
        pygame.sprite.Sprite.__init__(self)
        self.creation_time = pygame.time.get_ticks()
        self.detection_level_max = 100
        self.detection_level = 0.0
        if self.detection_level >= self.detection_level_max:
            self.detection_level = self.detection_level_max
        self.health = 0
        self.location = [tower_pool_local]
        self.state = ['sending', 'receiving', 'resting']
        self.base_detection_gain = 0.15
        self.images = []
        img = get_image('./images/sprites/blue_tower_wdish.gif')
        self.images.append(img)
        img = get_image('./images/sprites/green_tower_wdish.gif')
        self.images.append(img)
        img = get_image('./images/sprites/red_tower_wdish.gif')
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.open_menu = False
        self.last = pygame.time.get_ticks()
        self.initial_path = []
        self.current_state = self.state[2]
        self.flag = False



    def move(self):
        pass

    def resting_state(self):
        self.image = self.images[0]
        self.current_state = self.state[2]

    def sending_state(self):
        self.image = self.images[2]
        self.current_state = self.state[0]

    def receiving_state(self):
        self.image = self.images[1]
        self.current_state = self.state[1]

    class Cl_detection_bar(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.location = []
            self.location.append(x)
            self.location.append(y)
            self.load_images()
            self.image = self.bar_images[0]
            self.rect = self.image.get_rect()
            self.rect.x = self.location[1]
            self.rect.y = self.location[0] - 8

            self.det = 0
            self.reference_num = 0
            self.creation_time = pygame.time.get_ticks()
            self.last = pygame.time.get_ticks()


        def update(self):
            now = pygame.time.get_ticks()
            x = self.reference_num
            if now - self.last > (10 * 1000):
                x = self.detect()
            if x == 0:
                if now - self.last > (20 * 1000):
                    self.kill()

            self.image = self.bar_images[x]

        def detect(self):
            for s in game.tower_sprite_list:
                if s.rect.x == self.location[0] and s.rect.y == self.location[1]:
                    self.det = myround(s.detection_level)
                    self.reference_num = self.dat
                    return self.det

        def load_images(self):
            self.bar_images = []
            img = get_image('./images/sprites/bar/bar0.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar5.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar10.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar15.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar20.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar25.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar30.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar35.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar40.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar45.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar50.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar55.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar60.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar65.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar70.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar75.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar80.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar85.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar90.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar95.png')
            self.bar_images.append(img)
            img = get_image('./images/sprites/bar/bar100.png')
            self.bar_images.append(img)


    class Cl_Tower_menu(pygame.sprite.Sprite):
        def __init__(self, brian, fred, type):
            pygame.sprite.Sprite.__init__(self)
            self.x = brian
            self.y = fred
            self.type = type
            self.last = pygame.time.get_ticks()
            self.menu_images = []
            self.menu_images_inactive = []
            img = get_image('./images/sprites/menu_move_full.png')
            self.menu_images.append(img)
            img = get_image('./images/sprites/menu_move_inactive.png')
            self.menu_images_inactive.append(img)
            img = get_image('./images/sprites/reciving.png')
            self.menu_images.append(img)
            img = get_image('./images/sprites/reciving_not_active.png')
            self.menu_images_inactive.append(img)
            img = get_image('./images/sprites/transmitting.png')
            self.menu_images.append(img)
            img = get_image('./images/sprites/transmitting_not_active.png')
            self.menu_images_inactive.append(img)
            img = get_image('./images/sprites/cutpower.png')
            self.menu_images.append(img)
            img = get_image('./images/sprites/cutpower_not_active.png')
            self.menu_images_inactive.append(img)
            self.image = self.menu_images_inactive[0]
            self.rect = self.image.get_rect()
            self.rect.x = brian
            self.rect.y = fred
            if self.type == 'move':
                self.image = self.menu_images_inactive[0]
                # self.rect.x += 50
                # self.rect.y -= 100

            elif self.type == 'reciving':
                self.image = self.menu_images_inactive[1]
                # self.rect.x += 150
                # self.rect.y -= 50

            elif self.type == 'transmitting':
                self.image = self.menu_images_inactive[2]
                # self.rect.x += 150
                # self.rect.y += 50

            elif self.type == 'cutpower':
                self.image = self.menu_images_inactive[3]
                # self.rect.x += 50
                # self.rect.y += 100


        def image_flip(self):
            if self.type == 'move':
                self.image = self.menu_images[0]
            elif self.type == 'reciving':
                self.image = self.menu_images[1]
            elif self.type == 'transmitting':
                self.image = self.menu_images[2]
            elif self.type == 'cutpower':
                self.image = self.menu_images[3]

        def image_flop(self):
            if self.type == 'move':
                self.image = self.menu_images_inactive[0]
            elif self.type == 'reciving':
                self.image = self.menu_images_inactive[1]
            elif self.type == 'transmitting':
                self.image = self.menu_images_inactive[2]
            elif self.type == 'cutpower':
                self.image = self.menu_images_inactive[3]

        def delete(self):
            self.kill()

        def clicked(self):
            if pygame.time.get_ticks() > self.last + 300:
                for s in game.tower_sprite_list:
                    if s.flag == True:
                        if self.type == 'move':
                            s.flag = False
                            Cl_Tower.close_menu(s)
                            Cl_Tower.move(s)
                            for t in game.menu_sprites:
                                t.delete()
                            game.menu_sprites.empty()
                        elif self.type == 'reciving':
                            s.flag = False
                            Cl_Tower.close_menu(s)
                            Cl_Tower.receiving_state(s)
                            for t in game.menu_sprites:
                                t.delete()
                            game.menu_sprites.empty()
                        elif self.type == 'transmitting':
                            s.flag = False
                            Cl_Tower.close_menu(s)
                            Cl_Tower.sending_state(s)
                            for t in game.menu_sprites:
                                t.delete()
                            game.menu_sprites.empty()
                        elif self.type == 'cutpower':
                            s.flag = False
                            Cl_Tower.close_menu(s)
                            Cl_Tower.resting_state(s)
                            for t in game.menu_sprites:
                                t.delete()
                            game.menu_sprites.empty()




        def update(self):
            if pygame.time.get_ticks() > self.last + 300:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.image_flip()
                else:
                    self.image_flop()


            self.menu_speed = 15
            if self.type == 'move':
                if self.rect.x < self.x + 50:
                    self.rect.x += self.menu_speed
                if self.rect.y > self.y - 100:
                    self.rect.y -= self.menu_speed
            elif self.type == 'reciving':
                if self.rect.x < self.x + 150:
                    self.rect.x += self.menu_speed
                if self.rect.y < self.y + 50:
                    self.rect.y += self.menu_speed
            elif self.type == 'transmitting':
                if self.rect.x < self.x + 150:
                    self.rect.x += self.menu_speed
                if self.rect.y > self.y - 50:
                    self.rect.y -= self.menu_speed
            elif self.type == 'cutpower':
                if self.rect.x < self.x + 50:
                    self.rect.x += self.menu_speed
                if self.rect.y < self.y + 100:
                    self.rect.y += self.menu_speed

    def update(self):
        if self.current_state == self.state[1]:
            self.detection_level += (self.base_detection_gain / 4)
        elif self.current_state == self.state[0]:
            self.detection_level += self.base_detection_gain
        elif self.current_state == self.state[2]:
            self.detection_level -= (self.base_detection_gain / 2)
        if self.detection_level >= self.detection_level_max:
            pass
        if self.detection_level > 0:
           self.bar = self.Cl_detection_bar(self.rect.x, self.rect.y)
            game.bar_sprite_list.add(self.bar)


      
    def close_menu(self):
        self.open_menu = False


    def menu_open(self):
        if self.open_menu == False:
            self.move = self.Cl_Tower_menu(self.rect.x, self.rect.y, type = 'move')
            self.receiving = self.Cl_Tower_menu(self.rect.x, self.rect.y, type = 'reciving')
            self.transmitting = self.Cl_Tower_menu(self.rect.x, self.rect.y, type = 'transmitting')
            self.cutpower = self.Cl_Tower_menu(self.rect.x, self.rect.y, type = 'cutpower')


            game.menu_sprites.add(self.move)
            game.menu_sprites.add(self.receiving)
            game.menu_sprites.add(self.transmitting)
            game.menu_sprites.add(self.cutpower)
            game.is_menu_open = True
            self.open_menu = True
            self.flag = True


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
        self.launcher = Cl_Launcer(self.level.launcher_location[0], self.level.launcher_location[1] )
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
                    s.menu_open()
        if self.is_menu_open:
            for s in self.menu_sprites:
                if s.rect.collidepoint(mouse_pos):
                    if mouseinput[0] == 1:
                        s.clicked()




    def run_logic(self):                                #method runs each frame and updates positions
        if not self.game_over:                          #and checks for collisions

            self.all_sprites_list.update()              #move all sprites
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

if __name__ is '__main__':
    main()
else:
    main()


