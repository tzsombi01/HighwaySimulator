import pygame
import random
import time

# TODO PLAY/PAUSE button

# TODO timer, multiple random lane spawn, overtaking/lane changing - also smoothing

# TODO fix spawning bug - Check whether there's a vehicle in the place of the spawn

# TODO resizing images

GREEN = (70, 160, 0)
WHITE = (255, 255, 255)

HEIGHT = 600
WIDTH = 1000

vehicle_images = {"car": [pygame.image.load("vehicles/car.png")],
				  "motorcycle": [pygame.image.load("vehicles/motorcycle.png")]}
on_screen_vehicles = []
number_of_lanes = 3

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Highway Simulator')


class Vehicle:

	def __init__(self, type_of_vehicle, position, speed, image_representation):
		self.type_of_vehicle = type_of_vehicle
		self.position = [position[0], position[1]]
		self.speed = speed
		self.image_representation = image_representation

	def move(self):
		self.position[0] += self.speed


def main():
	run = True
	while run:
		draw_background()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		if 0 < random.randint(0, 100) < 10:
			create_vehicle()

		for i, vehicle in enumerate(on_screen_vehicles):
			print(len(on_screen_vehicles))
			print(i + 1)
			print(f"X:{vehicle.position[0]}, Y:{vehicle.position[1]}")

		draw_vehicle()
		move_vehicles_and_delay()
		remove_vehicle_when_off_screen()
		pygame.display.update()

	pygame.quit()


def draw_background():
	screen.fill(GREEN)
	draw_lanes()


def draw_lanes():
	pygame.draw.line(screen, WHITE, (0, 1 / number_of_lanes * HEIGHT), (WIDTH, 1 / number_of_lanes * HEIGHT))
	pygame.draw.line(screen, WHITE, (0, 2 / number_of_lanes * HEIGHT), (WIDTH, 2 / number_of_lanes * HEIGHT))


def draw_vehicle():
	for vehicle in on_screen_vehicles:
		screen.blit(vehicle.image_representation, (vehicle.position[0], vehicle.position[1]))


def move_vehicles_and_delay():
	for vehicle in on_screen_vehicles:
		vehicle.move()
	time.sleep(0.2)


def remove_vehicle_when_off_screen():
	for vehicle in on_screen_vehicles:
		if vehicle_out_of_screen(vehicle.position):
			on_screen_vehicles.remove(vehicle)


def vehicle_out_of_screen(position):
	if position[0] > WIDTH:
		return True
	return False


def create_vehicle():
	type_of_vehicle = pick_random_vehicle_type()
	on_screen_vehicles.append(Vehicle(type_of_vehicle,
							  pick_random_lane_to_spawn(),
							  pick_random_speed(),
							  pick_image_representation(type_of_vehicle)))


def pick_random_vehicle_type():
	return random.choice(list(vehicle_images.keys()))


def pick_random_lane_to_spawn():
	pos_x, pos_y = 0, random.randint(0, number_of_lanes - 1) / number_of_lanes * HEIGHT
	tries = 0
	threshold = number_of_lanes
	while lane_is_occupied_at_position(pos_y):
		if tries == threshold:
			return WIDTH + 1, pos_y
		pos_y = random.randint(0, number_of_lanes - 1) / number_of_lanes * HEIGHT
		tries += 1
	return pos_x, pos_y


def lane_is_occupied_at_position(pos_y):
	for vehicle in on_screen_vehicles:
		if pos_y == vehicle.position[1] and 0 <= vehicle.position[0] <= vehicle.image_representation.get_width():
			return True
	return False


def pick_random_speed():
	return random.randint(10, 20)


def pick_image_representation(type_of_vehicle):
	return random.choice(vehicle_images[type_of_vehicle])


if __name__ == "__main__":
	main()
