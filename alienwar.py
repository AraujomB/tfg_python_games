import pygame
import random
import math
import sys
import os

#Iniciamos pygame
pygame.init()

#Definimos el tamaño de la pantalla de juego
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#Le damos el nombre a la pantalla
pygame.display.set_caption("Alienwar")

#Bucle en el que se va a ejecutar el juego
run = True
while run:
    
    #Event handler para capturar el cierre del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#Salimos de pygame y finalizamos la ejecución
pygame.quit()