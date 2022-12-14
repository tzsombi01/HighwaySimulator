import pygame
import random
import time

# TODO PLAY/PAUSE button

# TODO Timer

GREEN = (70, 160, 0)
WHITE = (255, 255, 255)

HEIGHT = 600
WIDTH = 1000

vehicle_images = {"car": [pygame.image.load("vehicles/car1.png"), pygame.image.load("vehicles/car2.png")],
				  "motorcycle": [pygame.image.load("vehicles/motorcycle1.png"), pygame.image.load("vehicles/motorcycle2.png")]}
on_screen_vehicles = []
number_of_lanes = 3
smoothness = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Highway Simulator')


class Vehicle:

	def __init__(self, type_of_vehicle, position, speed, image_representation):
		self.type_of_vehicle = type_of_vehicle
		self.position = [position[0], position[1]]
		self.speed = speed
		self.image_representation = image_representation
		self.is_changing_lanes = False
		self.last_lane = self.position[1]
		self.desired_lane = None

	def move(self):
		self.position[0] += self.speed

	def change_lanes(self):
		self.position[0] += self.speed
		self.position[1] += (self.desired_lane - self.last_lane) / smoothness

	def is_faster(self, speed):
		return self.speed > speed

	def is_the_same_lane(self, vehicle):
		return self.position[1] == vehicle.position[1]

	def is_ahead_of_target_vehicle(self, vehicle, lane):
		safe_amount_of_self_length = 3
		if self.position[1] == lane[1]:
			return vehicle.position[0] < self.position[0] <= vehicle.position[0] + \
				   vehicle.image_representation.get_width() * safe_amount_of_self_length
		return False

	def is_behind_of_target_vehicle(self, vehicle, lane):
		safe_amount_of_self_length = 3
		if self.position[1] == lane[1]:
			return vehicle.position[0] > self.position[0] >= vehicle.position[0] - \
				   vehicle.image_representation.get_width() * safe_amount_of_self_length
		return False


def main():
	run = True
	while run:
		draw_background()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		if 0 < random.randint(0, 100) < 10:
			create_vehicle()

		draw_vehicle()
		change_lanes()
		move_vehicles_and_delay()
		remove_vehicle_when_off_screen()
		check_if_end_of_lane_change()
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
		if vehicle.is_changing_lanes:
			vehicle.change_lanes()
		else:
			vehicle.move()
	time.sleep(0.2)


def check_if_end_of_lane_change():
	for vehicle in on_screen_vehicles:
		if vehicle.desired_lane == vehicle.position[1]:
			vehicle.last_lane = vehicle.desired_lane
			vehicle.is_changing_lanes = False


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
									  pick_random_lane(),
									  pick_random_speed(),
									  pick_image_representation(type_of_vehicle)))


def pick_random_vehicle_type():
	return random.choice(list(vehicle_images.keys()))


def pick_random_lane():
	pos_x, pos_y = 0, random.randint(0, number_of_lanes - 1) / number_of_lanes * HEIGHT
	tries = 0
	threshold = number_of_lanes
	while lane_is_occupied_at_position((pos_x, pos_y)):
		if tries == threshold:
			return WIDTH + 1, pos_y
		pos_y = random.randint(0, number_of_lanes - 1) / number_of_lanes * HEIGHT
		tries += 1
	return pos_x, pos_y


def lane_is_occupied_at_position(position):
	for vehicle in on_screen_vehicles:
		if  position[1] == vehicle.position[1] and \
		    position[0] <= vehicle.position[0] <= position[0] + vehicle.image_representation.get_width():
			return True
	return False


def change_lanes():
	for vehicle in on_screen_vehicles:
		if check_if_changing_lanes_is_needed(vehicle) and changing_lanes_is_safe(vehicle):
			vehicle.is_changing_lanes = True


def check_if_changing_lanes_is_needed(tested_vehicle):
	for vehicle in on_screen_vehicles:
		if  tested_vehicle.is_faster(vehicle.speed) and \
			tested_vehicle.is_the_same_lane(vehicle) and \
			vehicle.is_ahead_of_target_vehicle(tested_vehicle, tested_vehicle.position):
			return True
	return False


def changing_lanes_is_safe(tested_vehicle):
	if check_up_down_a_lane_and_set_desired_lane(tested_vehicle):
		return True
	return False


def check_up_down_a_lane_and_set_desired_lane(tested_vehicle):
	upper_lane = tested_vehicle.position[0], tested_vehicle.position[1] - HEIGHT / number_of_lanes
	downward_lane = tested_vehicle.position[0], tested_vehicle.position[1] + HEIGHT / number_of_lanes
	lanes = [upper_lane, downward_lane]
	for lane in lanes:
		if lane_is_on_screen(lane) and check_for_vehicle_back_and_forth(tested_vehicle, lane): #TODO
			tested_vehicle.desired_lane = lane[1]
			return True
	return False


def check_for_vehicle_back_and_forth(tested_vehicle, lane):
	for vehicle in on_screen_vehicles:
		if vehicle.is_ahead_of_target_vehicle(tested_vehicle, lane) or vehicle.is_behind_of_target_vehicle(tested_vehicle, lane):
			return False
	return True


def lane_is_on_screen(lane):
	# 0 <= lane[1] <= (number_of_lanes - 1 / number_of_lanes) * HEIGHT
	return  0 <= lane[1] < HEIGHT


def pick_random_speed():
	return random.randint(10, 20)


def pick_image_representation(type_of_vehicle):
	return random.choice(vehicle_images[type_of_vehicle])


if __name__ == "__main__":
	main()
