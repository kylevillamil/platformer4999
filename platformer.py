import pygame
from pygame.locals import *

#Video 1: loading images/world data
#Video 2: loading player, drawing player, moving sideways and jumping
#Video 3: animation for character
#Video 4: 

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

#load sounds
rose_fx = pygame.mixer.Sound('audio/rose_2.wav')
rose_fx.set_volume(0.2)


pygame.mixer.music.load('audio/main_option_2.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#clock for fps
fps = 60
clock = pygame.time.Clock()

#define font and colors
font = pygame.font.SysFont('Bahaus 93', 70)
font_score = pygame.font.SysFont('Bahaus 93', 30)

white = (255,255,255)


#initialize size variables
screen_width = 1440
screen_height = 840

tile_size = 40
game_over = 0
main_menu = True
level = 0
world_data = []
score = 0
all_roses = False


#NOTE: with this tile size and these screen dimensions, the "grid" is 36x21 tiles, exactly

#initialize the game window with caption
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Monster Hunter 2: Trial Edition')

#STILL NEED THESE IMAGES
    #DEFINITELY
        #GRASS, ENEMY, MAIN_CHAR, DIRT, GOAL (not sure what this will be/look like), 
    #BONUS
        #FIRE(animated?), LAVA(animated?), 

#importing all images
bg_img = pygame.image.load('images/bg_image.png')
bg_img3 = pygame.image.load('images/background.png')
bg_img2 = pygame.image.load('images/bg2.png')
goal_img = pygame.image.load('images/baddie_test.png')
reset_image = pygame.image.load('images/reset_button.png')
reset_img = pygame.transform.scale(reset_image, (screen_width // 5, screen_height // 7))
start_img = pygame.image.load('images/start.png')
exit_img = pygame.image.load('images/exit.png')



#NOTE: to scale a image, if we change the screen/tile size, use:
    #img = pygame.transform.scale(IMAGE_TO_SCALE, (tile_size, tile_size))


#scaling bg image, setting to bg
bg = pygame.transform.scale(bg_img2, (screen_width, screen_height))


#drawing a grid

def draw_grid():
    for row in range(0, screen_height, tile_size):
        for col in range(0, screen_width, tile_size):
            pygame.draw.line(screen, (255,255,255), (col, row), (col+tile_size, row))
            pygame.draw.line(screen, (255,255,255), (col, row), (col, row+tile_size))


#draw text function
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))




#function to reset level/load new level
def reset_level(level):
    #HERE, WE CAN USE LEVEL SPECIFIC COORDINATES TO PLACE THE PLAYER IN CORRECT SPOT WHEN NEW LEVEL LOADS
    player.reset(tile_size * 4, screen_height - ((2* tile_size) + (1.5 * tile_size)))
    global all_roses
    all_roses = False
    slime_group.empty()
    diablo_group.empty()
    spike_group.empty()
    exit_group.empty()
    dirt_group.empty()
    bridge_group.empty()
    rose_group.empty()
    platform_group.empty()
    score_rose = Rose(tile_size // 2, tile_size // 2 + 3)
    rose_group.add(score_rose)
    world = World(world_data[level])

    
    return world




class World():
    def __init__(self, data):
        self.tile_list = []
        self.bridge_list = []
        self.bridge_thresh_list = []
        self.rose_count = 0

        #load images
        brick_img = pygame.image.load('images/brick.png')
        brick2_img = pygame.image.load('images/brick2.png')
        brick3_img = pygame.image.load('images/brick3.png')

        floor1_img = pygame.image.load('images/floor_1.png')
        floor2_img = pygame.image.load('images/floor_2.png')
        floor3_img = pygame.image.load('images/floor_3.png')

        bridge_top_img = pygame.image.load('images/bridge_top.png')
        bridge_thresh_img = pygame.image.load('images/bridge_thresh.png')


        brick_count = 0
        floor_count = 0
        plat_count = 0

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1: #BRICK
                    brick_count +=1
                    if brick_count %3 == 0:
                        img = pygame.transform.scale(brick_img, (tile_size, tile_size))
                    elif brick_count %3 == 1:
                        img = pygame.transform.scale(brick2_img, (tile_size, tile_size))
                    else:
                        img = pygame.transform.scale(brick3_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2: #BRIDGE
                    bridge = Bridge(col_count * tile_size, row_count * tile_size)
                    bridge_group.add(bridge)
                    bridge_top = (bridge_top_img, (col_count * tile_size, row_count * tile_size - bridge_top_img.get_height()))
                    self.bridge_list.append(bridge_top)
                    bridge_thresh = (bridge_thresh_img, (col_count * tile_size, row_count * tile_size - 2))
                    self.bridge_thresh_list.append(bridge_thresh)
                if tile == 3: #FLOOR
                    floor_count += 1
                    if floor_count %3 == 0:
                        img = pygame.transform.scale(floor1_img, (tile_size, tile_size // 2))
                    elif floor_count %3 == 1:
                        img = pygame.transform.scale(floor2_img, (tile_size, tile_size // 2))
                    else:
                        img = pygame.transform.scale(floor3_img, (tile_size, tile_size // 2))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4: #SPIKES
                    spike = Spike(col_count * tile_size, row_count * tile_size)
                    spike_group.add(spike)
                if tile == 5: #DIABLOS
                    diablo = Diablo(col_count * tile_size, row_count * tile_size)
                    diablo_group.add(diablo)
                if tile == 6: #EXIT/GIRL
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                if tile == 7: #ROSES
                    rose = Rose(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    rose_group.add(rose)
                    self.rose_count += 1
                if tile == 8: #HORIZONTAL moving platforms
                    plat_count += 1
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0, plat_count)
                    platform_group.add(platform)
                    dirt = Dirt(col_count * tile_size, row_count * tile_size - 2, 1, 0)
                    dirt_group.add(dirt)
                if tile == 9: #VERTICAL moving platforms
                    plat_count += 1
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0 ,1, plat_count)
                    platform_group.add(platform)
                    dirt = Dirt(col_count * tile_size, row_count * tile_size - 2, 0, 1)
                    dirt_group.add(dirt)
                if tile == 10: #DIABLOS
                    slime = Slime(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    slime_group.add(slime)
                col_count += 1
            row_count += 1
        
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (150,150,150), tile[1], 2)
        for bridge in self.bridge_list:
            screen.blit(bridge[0], bridge[1])
        for bridge_thresh in self.bridge_thresh_list:
            screen.blit(bridge_thresh[0], bridge_thresh[1])

    def rose_return(self):
        print(len(rose_group))

        



class Diablo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/diablo_1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

        self.image_index = 0
        self.image_counter = 0
        self.cooldown = 6
        self.images_right = []
        self.images_left = []

        #LOAD IMAGES into arrays, FLIP
        for num in range(1, 5):
            image_r = pygame.image.load(f'images/diablo_{num}.png')
            self.images_right.append(image_r)
            image_l = pygame.transform.flip(image_r, True, False)
            self.images_left.append(image_l)
        



    def update(self):

        self.rect.x += self.move_direction
        self.move_counter += 2
        self.image_counter += 1

        if self.move_direction >= 0 and self.image_counter > self.cooldown:
            self.image_counter = 0
            self.image_index += 1
            if self.image_index >= len(self.images_right):
                self.image_index = 0
            self.image = self.images_right[self.image_index]
        elif self.move_direction < 0 and self.image_counter > self.cooldown:
            self.image_counter = 0
            self.image_index += 1
            if self.image_index >= len(self.images_left):
                self.image_index = 0
            self.image = self.images_left[self.image_index]
            

        if abs(self.move_counter) > 120:
            self.move_direction *= -1
            self.move_counter *= -1


class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/slime1.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.image_index = 0
        self.image_counter = 0
        self.cooldown = 5
        self.images = []

        #Load images into array of images
        for num in range(1, 5):
            img = pygame.image.load(f'images/slime{num}.png')
            self.images.append(img)

    def update(self):
        self.image_counter += 1
        if self.image_counter > self.cooldown:
            self.image_counter = 0
            self.image_index += 1
            if self.image_index >= len(self.images):
                self.image_index = 0
            self.image = self.images[self.image_index]

class Bridge(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/bridge_base.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * (3/8))))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/spike1.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        


class Rose(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/rose1.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.image_index = 0
        self.image_counter = 0
        self.cooldown = 5
        self.images = []
        self.images_flipped = []

        for num in range(1, 5):
            img = pygame.image.load(f'images/rose{num}.png')
            self.images.append(img)
            img_flip = pygame.transform.flip(img, True, False)
            self.images_flipped.append(img_flip)
        
        for i in range(4):
            self.images.append(self.images_flipped[i])

    def update(self):
        self.image_counter += 1
        if self.image_counter > self.cooldown:
            self.image_counter = 0
            self.image_index += 1
            if self.image_index >= len(self.images):
                self.image_index = 0
            self.image = self.images[self.image_index]


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y, plat_count):
        pygame.sprite.Sprite.__init__(self)
        img1 = pygame.image.load('images/floor_1.png')
        img2 = pygame.image.load('images/floor_2.png')
        img3 = pygame.image.load('images/floor_3.png')

        if plat_count %3 == 0:
            self.image = pygame.transform.scale(img1, (tile_size, tile_size // 2))
        elif plat_count %3 == 1:
            self.image = pygame.transform.scale(img2, (tile_size, tile_size // 2))
        else:
            self.image = pygame.transform.scale(img3, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
        
class Dirt(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/plat_thresh.png')
        self.image = pygame.transform.scale(img, (tile_size, 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y
        
    def update(self):
        
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
        

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('images/baddie.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# 36 x 21
level0_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 1, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 10, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
level1_data = [
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
 [1, 0, 0, 0, 0, 0, 0, 0, 1, 10, 10, 10, 1, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1], 
 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
 ]

level2_data = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 1], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 1], 
               [1, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
               [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 1], 
               [1, 1, 1, 1, 1, 0, 0, 8, 8, 0, 0, 2, 2, 2, 0, 0, 8, 8, 8, 0, 0, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1], 
               [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
               [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 1], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 3, 3, 0, 1], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 2, 2, 3, 0, 0, 0, 1, 1, 1, 10, 10, 1, 1, 1, 1, 1, 1, 1, 10, 10, 10, 1], 
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 10, 10, 10, 10, 10, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
               ]

level3_data =  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1], 
                [1, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1], 
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
                [1, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 10, 10, 1, 4, 1, 10, 10, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
                [1, 0, 0, 0, 0, 9, 9, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1], 
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
                [1, 0, 2, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
                [1, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1], 
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 8, 8, 8, 0, 0, 1, 1, 0, 0, 8, 8, 8, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 1], 
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1], 
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 9, 0, 0, 9, 0, 0, 3, 0, 0, 1], 
                [1, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1], 
                [1, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 4, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1, 1], 
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                [1, 1, 1, 1, 1, 10, 10, 10, 10, 10, 10, 1, 2, 2, 2, 1, 10, 10, 10, 10, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                ]


world_data.append(level0_data)
world_data.append(level1_data)
world_data.append(level2_data)
world_data.append(level3_data)


class Button():
    def __init__(self, x, y, image, type):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.type = type

    def draw(self):
        action = False

        #get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.type == 1:
            action = True
            self.clicked = True
            
            


        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouse over and click conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
                #pygame.time.delay()
                
                

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw the button
        screen.blit(self.image, self.rect)

        return action



class Player():
    def __init__(self, x, y):
        self.reset(x, y)
    

    def update(self, game_over):
        dx = 0
        dy = 0
       
        walk_cooldown = 5
        acc_cooldown = 2
        crouch_cooldown = 8
        col_thresh = 10

        if game_over == 0:
            #get keypresses
            key = pygame.key.get_pressed()

            #CROUCHING
            if (key[pygame.K_DOWN] and self.in_air == False) and self.direction == 1 or self.direction == 2:
                self.counter_crouch += 1
                self.direction = 2
            if key[pygame.K_DOWN] == False and self.direction == 2:
                self.direction = 1

            if (key[pygame.K_DOWN] and self.in_air == False) and self.direction == -1 or self.direction == -2:
                self.counter_crouch += 1
                self.direction = -2
            if key[pygame.K_DOWN] == False and self.direction == -2:
                self.direction = -1


            #JUMPING
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False






            #LEFT AND RIGHT MOVEMENT
            if key[pygame.K_RIGHT] and key[pygame.K_LEFT] == False:
                self.acc_counter += 1
                if self.acc_counter > 1:
                    if self.vel_x < 1:
                        self.vel_x = 1
                    self.vel_x += 1
                    self.acc_counter = 0
                dx = self.vel_x
                if dx > 6:
                    dx = 6
                self.counter += 1
                self.direction = 1
                #print("dx Right: ", dx)

            if key[pygame.K_LEFT] and key[pygame.K_RIGHT] == False:
                self.acc_counter += 1
                if self.acc_counter > acc_cooldown:
                    if self.vel_x > -1:
                        self.vel_x = -1
                    self.vel_x -= 1
                    self.acc_counter = 0
                dx = self.vel_x
                if dx < -6:
                    dx = -6
                self.counter += 1
                self.direction = -1
                #print("dx Left: ", dx)
                    

            if key[pygame.K_LEFT] and key[pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]

                if self.direction == -1:
                    self.image = self.images_left[self.index]
                
                self.vel_x = 0
                


            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False and key[pygame.K_DOWN] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                
                self.vel_x = 0
                dx = 0
                


                

            #handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            


            if self.counter_crouch > crouch_cooldown:  
                self.counter_crouch = 0
                self.index_crouch += 1
                if self.index_crouch >= len(self.images_crouch_right):
                    self.index_crouch = 0
                if self.direction == 2:
                    self.image = self.images_crouch_right[self.index_crouch]
                if self.direction == -2:
                    self.image = self.images_crouch_left[self.index_crouch]
                    

            #add gravity
            self.vel_y +=1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y


            #CHECK FOR COLLISION
            self.in_air = True
            for tile in world.tile_list:
                #check x direction collision
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                    self.vel_x = 0
                #check y direction collision
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the tile(jumping)
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above the tile(standing/falling)
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            #check for collision with enemies
            if pygame.sprite.spritecollide(self, diablo_group, False):
                game_over = -1

            if pygame.sprite.spritecollide(self, slime_group, False):
                game_over = -1
            
            #check for collision with spikes
            if pygame.sprite.spritecollide(self, spike_group, False):
                game_over = -1

            #check for collision with GOAL GIRL / EXIT
            if pygame.sprite.spritecollide(self, exit_group, False) and all_roses == True:
                game_over = 1

            #check collsion with moving platforms
            for platform in platform_group:
                #collision in x direction
                #if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    #dx = 0
                #collision in y direction
                if dy >= 0:
                    if platform.rect.colliderect(self.rect.x, self.rect.bottom + dy, self.width, self.height):
                        #check if below platform
                        #if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        #    self.vel_y = 0
                        #    dy = platform.rect.bottom - self.rect.top
                        #check if above platform
                        if (abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh) and (self.vel_y > 0):
                            self.rect.bottom = platform.rect.top - 2
                            self.in_air = False
                            dy = 0
                        #move sideways with platform
                        if platform.move_x != 0:
                            self.rect.x += platform.move_direction
                            self.in_air = False

            #check collision with bridge(only if on top)
            for bridge in bridge_group:
                if bridge.rect.colliderect(self.rect.x, self.rect.bottom + dy, self.width, self.height) and self.vel_y > 0:
                    
                    
                     if abs((self.rect.bottom + dy) - bridge.rect.top) < col_thresh:
                                self.rect.bottom = bridge.rect.top - 2
                                self.in_air = False
                                dy = 0    
                        
                        
                        #dy = bridge.rect.top - self.rect.bottom
                        #self.in_air = False

                        #elif self.vel_y >= 0:
                        #dy = tile[1].top - self.rect.bottom
                        #self.vel_y = 0
                        #self.in_air = False


            #UPDATE PLAYER COORDINATES
            self.rect.x += dx
            self.rect.y += dy


        elif game_over == -1:
            self.image = self.dead_image
            draw_text("You died!", font, white, screen_width // 2 - 260, screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5


        #draw player on screen
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255,255,255), self.rect, 2)

        return game_over


    def reset(self, x, y):
        self.dead_img = pygame.image.load('images/rizz_demon_bg.png')
        self.images_right = []
        self.images_left = []
        self.images_crouch_right = []
        self.images_crouch_left = []
        self.index = 0
        self.index_crouch = 0
        self.counter = 0
        self.counter_crouch = 0
        self.direction = 1

        for num in range(1, 5):
            img_right = pygame.image.load(f'images/main_char_{num}.png')
            self.images_right.append(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_left.append(img_left)
            
        for num in range(1, 5):
            img_crouch_right = pygame.image.load(f'images/main_char_crouch_{num}.png')
            self.images_crouch_right.append(img_crouch_right)
            img_crouch_left = pygame.transform.flip(img_crouch_right, True, False)
            self.images_crouch_left.append(img_crouch_left)

        self.image = self.images_right[self.index]

        self.dead_image = pygame.transform.scale(self.dead_img, (tile_size, int(tile_size * 1.5)))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.vel_x = 0
        self.x_acc = .0005
        self.jumped = False
        self.in_air = True
        self.acc_counter = 0



player = Player(tile_size * 4, screen_height - ((2* tile_size) + (1.5 * tile_size)))
slime_group = pygame.sprite.Group()
diablo_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
dirt_group = pygame.sprite.Group()
bridge_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
rose_group = pygame.sprite.Group()

#create dummy rose to show score with
score_rose = Rose(tile_size // 2, tile_size // 2 + 3)
rose_group.add(score_rose)

if level < len(world_data):
    world = World(world_data[level])

#creating buttons
reset_button = Button(screen_width // 2 - (reset_img.get_width() // 2), screen_height // 2 + 50, reset_img, 1)
start_button = Button(int(screen_width * 1 / 4), int(screen_height * 1 / 4), start_img, 1)
exit_button = Button(int(screen_width * 3 / 4), int(screen_height * 1 / 4), exit_img, 0)




run = True

while run:
    
    clock.tick(fps)

    #drawing background to screen
    screen.blit(bg, (0,0))
    #screen.fill((150,150,150))
    #draw_grid()
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False

    else:
        world.draw()
        print(len(rose_group))

        if game_over == 0:
            slime_group.update()
            rose_group.update()
            diablo_group.update()
            dirt_group.update()
            platform_group.update()

            #check if rose collected
            if pygame.sprite.spritecollide(player, rose_group, True):
                #update rose scount (SCORE)
                rose_fx.play()
                score += 1
                if len(rose_group) <= 1:
                    all_roses = True

                
            #display score on screen
            draw_text("x  " + str(score), font_score, white, tile_size, 6)


        slime_group.draw(screen)
        diablo_group.draw(screen)
        spike_group.draw(screen)
        dirt_group.draw(screen)
        platform_group.draw(screen)
        bridge_group.draw(screen)
        exit_group.draw(screen)
        rose_group.draw(screen)

        game_over = player.update(game_over)

        #if player has died
        if game_over == -1:
            if reset_button.draw():
                #player.reset(tile_size * 4, screen_height - ((2* tile_size) + (1.5 * tile_size)))
                world = reset_level(level)
                game_over = 0
                score = 0
                pygame.time.delay(300)

        #if player beats level
        if game_over == 1:
            #reset and go to next level
            level += 1
            if level < len(world_data):
                #reset next level
                world = reset_level(level)
                game_over = 0
                score = 0
                pygame.time.delay(300)
            else: 
                draw_text("You won!", font, white, screen_width // 2 - 260, screen_height // 2)
                #restart game
                if reset_button.draw():
                    level = 0
                    world = reset_level(level)
                    game_over = 0
                    score = 0

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.mixer.music.stop()

pygame.quit()
