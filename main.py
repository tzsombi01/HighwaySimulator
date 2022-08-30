import time
import pygame

HEIGHT = 500
WIDTH = 500

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption('Highway Simulator')

class Vehicle:
	def __init__(self, typeOfVehicle, posX, posY, speed):
		self.typeOfVehicle = typeOfVehicle
		self.posX = posX
		self.posY = posY
		self.speed = speed

	def move(self):
		self.posX += self.speed

	# def set_type(self, type):
	# 	return self.typeOfVehicle = type

	def get_type(self):
		return self.typeOfVehicle
