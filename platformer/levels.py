import pygame
import pickle
from os import path



pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
tile_size = 40
cols = 36
margin = 100
screen_width = 1440
screen_height = 840


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Level Editor')


#load images
bg_img = pygame.image.load('images/bg2.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
dirt_img = pygame.image.load('images/dirt.png')

brick_img = pygame.image.load('images/brick.png')
bridge_img = pygame.image.load('images/bridge_base.png')
floor_img = pygame.image.load('images/floor_1.png')
spike_img = pygame.image.load('images/spike1.png')
diablo_img = pygame.image.load('images/diablo_1.png')
exit_img = pygame.image.load('images/baddie.png')
rose_img = pygame.image.load('images/rose_main_template.png')
floor_horiz_img = pygame.image.load('images/floor_horiz.png')
floor_vert_img = pygame.image.load('images/floor_vert.png')
slime_img = pygame.image.load('images/slime1.png')

grass_img = pygame.image.load('images/grass.png')




save_image = pygame.image.load('images/start.png')
save_img = pygame.transform.scale(save_image, (save_image.get_width(), 80))
load_img = pygame.image.load('images/reset_button.png')


#define game variables
clicked = False
level = 1

#define colours
white = (255, 255, 255)
green = (144, 201, 120)

font = pygame.font.SysFont('Futura', 24)

#create empty tile list
world_data = []
for row in range(21):
	r = [0] * 36
	world_data.append(r)

#create boundary
for tile in range(0, 36):
	world_data[20][tile] = 1
	world_data[0][tile] = 1
for tile in range(0, 21):
	world_data[tile][0] = 1
	world_data[tile][35] = 1

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_grid():
	for c in range(cols):
		#vertical lines
		pygame.draw.line(screen, white, (c * tile_size, 0), (c * tile_size, screen_height))
		#horizontal lines
		pygame.draw.line(screen, white, (0, c * tile_size), (screen_width, c * tile_size))


def draw_world():
	for row in range(21):
		for col in range(36):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					#brick blocks
					img = pygame.transform.scale(brick_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 2:
					#bridge blocks
					img = pygame.transform.scale(bridge_img, (tile_size, int(tile_size * (3/8))))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 3:
					#floor blocks
					img = pygame.transform.scale(floor_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 4:
					#spikes
					img = pygame.transform.scale(spike_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
					pass
				if world_data[row][col] == 5:
					#diablos
					img = pygame.transform.scale(diablo_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size))
					pass
				if world_data[row][col] == 6:
					#exit/girl
					img = pygame.transform.scale(exit_img, (tile_size, int(tile_size * 1.5)))
					screen.blit(img, (col * tile_size, row * tile_size - (tile_size // 2)))
				if world_data[row][col] == 7:
					#rose
					img = pygame.transform.scale(rose_img, (tile_size // 2, tile_size))
					screen.blit(img, (col * tile_size + 10, row * tile_size + 4))
				if world_data[row][col] == 8:
					#floor blocks
					img = pygame.transform.scale(floor_horiz_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 9:
					#floor blocks
					img = pygame.transform.scale(floor_vert_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size))
				if world_data[row][col] == 10:
					#floor blocks
					img = pygame.transform.scale(slime_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
				



class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

#create load and save buttons
save_button = Button(screen_width // 2 - save_img.get_width() // 2, screen_height - 80, save_img)


#main game loop
run = True
while run:
	
	
        
	

	clock.tick(fps)

	#draw background
	screen.fill((200,200,200))
	#screen.blit(bg_img, (0, 0))


	


	#show the grid and draw the level tiles
	draw_grid()
	draw_world()


	#text showing current level
	

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#mouseclicks to change tiles
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			#check that the coordinates are within the tile area
			if x < 36 and y < 21:
				#update tile value
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 10:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 10
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#up and down key presses to change level number
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	#update game display window
	pygame.display.update()
	
print("WORLD CREATED:\n", world_data)

pygame.quit()