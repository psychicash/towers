from main import pygame
from library1 import get_image



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
            self.bar_images = []
            self.load_images()
            self.image = self.bar_images[0]
            self.rect = self.image.get_rect()
            self.rect.x = self.location[0]
            self.rect.y = self.location[1] - 8

            self.det = 0
            self.reference_num = 0
            self.creation_time = pygame.time.get_ticks()
            self.last = pygame.time.get_ticks()


        def update(self, game):
            now = pygame.time.get_ticks()
            x = self.reference_num
            if now - self.last > (5 * 1000):
                x = self.detect(game)
            if x == 0:
                if now - self.last > (20 * 1000):
                    self.kill()

            self.image = self.bar_images[x]

        def detect(self, game):
            for s in game.tower_sprite_list:
                if s.rect.x == self.location[0] and s.rect.y == self.location[1]:
                    print(int(myround(s.detection_level ) /5))
                    self.det = int(myround(s.detection_level ) /5)
                    self.reference_num = self.det
                    return self.det

        def load_images(self):

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

        def clicked(self, game):
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

    def bar_idle(self, game):
        if self.detection_level > 0:
            self.bar = self.Cl_detection_bar(self.rect.x, self.rect.y)
            game.bar_sprite_list.add(self.bar)


    def close_menu(self):
        self.open_menu = False


    def menu_open(self, game):
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
