import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 750, 740
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")


RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "battery.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "turtlepic.png"))

RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "oceanbackground.jpg")), (WIDTH, HEIGHT))

class Ship:
	def __init__(self, x, y, health=100):
		self.x = x
		self.y = y 
		self.health = health
		self.ship_img = None
		self.laser_img = None
		self.laser = []
		self.cool_down_counter = 0 

	def draw(self, window):
		window.blit(self.ship_img, (self.x, self.y))

	def get_width(self):
		return self.ship_img.get_width()

	def get_height(self):
		return self.ship_img.get_height()


class Player(Ship):
	def __init__(self, x, y, health=100):
		super().__init__(x, y, health)
		self.ship_img = YELLOW_SPACE_SHIP
		self.laser_img = YELLOW_LASER
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.max_health = health

class Enemy(Ship):
	COLOR_MAP = {
				"red": (RED_SPACE_SHIP, RED_LASER),
				"green": (GREEN_SPACE_SHIP, GREEN_LASER),
				"blue": (BLUE_SPACE_SHIP, BLUE_LASER)
	}

	def __init__(self, x, y, color, health=100): 
		super().__init__(x, y, health)
		self.ship_img, self.laser_img = self.COLOR_MAP[color]
		self.mask = pygame.mask.from_surface(self.ship_img)

	def move(self, vel):
		self.y += vel


def main():
	run = True
	FPS = 60
	level = 0
	lives = 5
	ship_vel = 5
	main_font = pygame.font.SysFont("comicsans", 50)

	enemies = []
	wave_length = 5
	enemy_vel = 4

	ship = Player(300, 650)

	clock = pygame.time.Clock()

	def redraw_window():
		WIN.blit(BG, (0, 0))
		lives_label = main_font.render(f"Lives: {lives}", 1, (0, 0, 255))
		level_label = main_font.render(f"Level: {level}", 1, (0, 0, 255))

		WIN.blit(lives_label, (10,10))
		WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

		ship.draw(WIN)

		for enemy in enemies:
			enemy.draw(WIN)

		pygame.display.update()

	while run:
		clock.tick(FPS)

		if len(enemies) == 0:
			level += 1
			wave_length += 5
			for i in range(wave_length):
				enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "green", "blue"]))
				enemies.append(enemy)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		keys = pygame.key.get_pressed()
		if keys[pygame.K_a] and ship.x - ship_vel > 0:
			ship.x -= ship_vel
		if keys[pygame.K_d] and ship.x + ship_vel + ship.get_width() < WIDTH:
			ship.x += ship_vel
		if keys[pygame.K_w] and ship.y - ship_vel > 0:
			ship.y -= ship_vel
		if keys[pygame.K_s] and ship.y + ship_vel + ship.get_height() < HEIGHT:
			ship.y += ship_vel

		for enemy in enemies:
			enemy.move(enemy_vel)

		redraw_window()

main()