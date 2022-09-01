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

# car_images = [pygame.image.load("vehicles/car.png")]
# motorcycle_images = [pygame.image.load("vehicles/motorcycle.png")]

vehicle_images = {"car": [pygame.image.load("vehicles/car.png")], "motorcycle": [pygame.image.load("vehicles/motorcycle.png")]}
on_screen_vehicles = []
number_of_lanes = 2

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


def pick_image_representation(type_of_vehicle):
	return random.choice(vehicle_images[type_of_vehicle])


def draw_background():
	pygame.draw.line(screen, WHITE, (0, 1 / 3 * HEIGHT), (WIDTH, 1 / 3 * HEIGHT))
	pygame.draw.line(screen, WHITE, (0, 2 / 3 * HEIGHT), (WIDTH, 2 / 3 * HEIGHT))


def draw_game_window():
	screen.fill(GREEN)
	draw_background()


def draw_vehicle():
	if len(on_screen_vehicles) == 0:
		pass
	for vehicle in on_screen_vehicles:
		# print(f"Type of vehicle: {vehicle.type_of_vehicle}, position: {vehicle.position}" )
		screen.blit(vehicle.image_representation, (vehicle.position[0], vehicle.position[1]))


def create_vehicle():
	type_of_vehicle = pick_random_vehicle_type()
	on_screen_vehicles.append(Vehicle(type_of_vehicle,
							  pick_random_lane_to_spawn(),
							  pick_random_speed(),
							  pick_image_representation(type_of_vehicle)))


def pick_random_speed():
	return random.randint(10, 20)


# TODO refactor
def pick_random_lane_to_spawn():
	pos_x, pos_y = 0, 1 / random.randint(2, 3) * HEIGHT
	tries = 0
	threshold = number_of_lanes
	while lane_is_occupied_at_position(pos_y):
		if tries == threshold:
			return WIDTH + 1, pos_y
		pos_y = 1 / random.randint(2, 3) * HEIGHT
		tries += 1
	return pos_x, pos_y


def lane_is_occupied_at_position(pos_y):
	if len(on_screen_vehicles) == 0:
		return False

	for vehicle in on_screen_vehicles:
		if pos_y <= vehicle.position[1] <= pos_y + vehicle.image_representation.get_width():
			print(f"Occupied, vehicles at scene: {len(on_screen_vehicles)}")
			return True
	return False


def pick_random_vehicle_type():
	return random.choice(list(vehicle_images.keys()))


def move_vehicles():
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


def main():
	run = True
	while run:
		draw_game_window()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.key.get_pressed()[pygame.K_SPACE]:
				create_vehicle()

		draw_vehicle()
		move_vehicles()
		remove_vehicle_when_off_screen()
		pygame.display.update()

	pygame.quit()


if __name__ == "__main__":
	main()
