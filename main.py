import pygame
import random
import time

# TODO PLAY/PAUSE button

GREEN = (70, 160, 0)
WHITE = (255, 255, 255)

HEIGHT = 600
WIDTH = 1000

CAR_IMAGES = [pygame.image.load("vehicles/car.png")]
MOTORCYCLE_IMAGES = [pygame.image.load("vehicles/motorcycle.png")]
SPEED_OF_VEHICLES = {"car": 10, "motorcycle": 15}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Highway Simulator')


class Vehicle:

	def __init__(self, typeOfVehicle, posX, posY, speed):
		self.typeOfVehicle = typeOfVehicle
		self.posX = posX
		self.posY = posY
		self.speed = speed

	def start(self):
		pass

	def change_lanes(self):
		pass

	def move(self):
		self.posX += self.speed

	def get_type(self):
		return self.typeOfVehicle


def pick_random_car_image():
	return random.choice(CAR_IMAGES)


def pick_random_motorcycle_image():
	return random.choice(MOTORCYCLE_IMAGES)


def draw_lanes():
	pygame.draw.line(screen, WHITE, (0, 1 / 3 * HEIGHT), (WIDTH, 1 / 3 * HEIGHT))
	pygame.draw.line(screen, WHITE, (0, 2 / 3 * HEIGHT), (WIDTH, 2 / 3 * HEIGHT))


def redraw_game_window():
	screen.fill(GREEN)
	draw_lanes()
	pygame.display.update()


def main():
	run = True
	while run:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		redraw_game_window()
	pygame.quit()


if __name__ == "__main__":
	main()
