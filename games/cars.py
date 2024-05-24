import pygame
from pygame.locals import *
import random

pygame.init()

#creamos la ventana
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Rápido & Furioso')

#colores
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

#configuración del juego
gameover = False
speed = 2
score = 0

#marcadores
marker_width = 10
marker_height = 50

#medidas para la carretera
road = (100, 0, 300, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)


#reloj para controlar la velocidad del juego
clocK = pygame.time.Clock()
fps = 120

#bucle del juego
def gameloop():
    clocK.tick(fps)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        #pintamos de verde el fondo para el escenario del juego
        screen.fill(green)

        #dibujamos la carretera
        pygame.draw.rect(screen, gray, road)

        #dibujamos los bordes de la carretera
        pygame.draw.rect(screen, yellow, left_edge_marker)
        pygame.draw.rect(screen, yellow, right_edge_marker)

        pygame.display.update()

    pygame.quit()

gameloop()