import pygame, sys, os
from pygame.locals import *
import random

pygame.init()

#creamos la ventana
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Rápido & Furioso')

#Obtenemos la ruta de los recursos para evitar conflictos al ejecutar desde el index
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        #devolvemos la ruta absoluta de los recursos
        return os.path.join(base_path, relative_path)

#colores
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

#cargar sonido de fondo
asset_sound = resource_path('assets/sounds/pollo-loco.mp3')
sound = pygame.mixer.music.load(asset_sound)

#reproducimos el sonido de fondo en bucle y ajustamos el volumen
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

#configuración del juego
gameover = False
speed = 2
score = 0

#marcadores
marker_width = 10
marker_height = 50

#medidas para la carretera
road_width = 300
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

#coordenadas de las líneas
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

#animar movimiento de los marcadores de línea
lane_marker_move_y = 0

#coordenadas de inicio del jugador
player_x = 250
player_y = 400

#reloj para controlar la velocidad del juego
clocK = pygame.time.Clock()
fps = 120

class Vehicle(pygame.sprite.Sprite): #Sprite es una clase de pygame que nos permite manejar sprites (objetos con movimiento)
    '''
    Clase vehiculo heredada de la clase sprite de pygame para el manejo de objetos con movimiento o sprites
    '''
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        #ajustar la imagen para que no supere el tamaño del carril
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class PlayerVehicle(Vehicle):
    '''
    Clase para el vehículo del jugador heredada de la clase Vehicle
    '''
    #establecemos una imagen para el coche dentro del constructor
    def __init__(self, x, y):
        image = pygame.image.load('assets/images/cars/pickup.png')
        super().__init__(image, x, y)

#conjuntos de sprites
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

#crear el coche del jugador
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

#cargar las imágenes de los distintos vehículos
image_filenames = ['car.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('assets/images/cars/' + image_filename)
    vehicle_images.append(image)

#cargar imagen para colisión
crash = pygame.image.load('assets/images/cars/crash.png')
crash_rect = crash.get_rect() #coger el rectángulo de la imagen de crash dentro de pygame

#bucle del juego
def gameloop():
    #hacer globales las variables para poder acceder a ellas y evitar errores
    global lane_marker_move_y
    global speed
    global score
    global gameover

    run = True
    while run:

        clocK.tick(fps)

        for event in pygame.event.get():
            #controlar si se cierra la ventana para finalizar el juego
            if event.type == QUIT:
                run = False

            #mover al jugador con las flechas izquierda/derecha
            if event.type == KEYDOWN:
                #mover un carril a la izquierda siempre que no esté ya lo máximo
                if event.key == K_LEFT and player.rect.center[0] > left_lane:
                    player.rect.x -= 100
                #mover un carril a la derecha siempre que no esté ya lo máximo
                elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                    player.rect.x += 100
                    
                #verificar si hay colisión al cambiar de carril
                for vehicle in vehicle_group:
                    if pygame.sprite.collide_rect(player, vehicle): #collide_rect() función de pygame para controlar si dos sprites están colisionando
                        
                        gameover = True
                        
                        #colocar el coche del jugador cerca de otro vehículo y mostrar la imagen de choque
                        if event.key == K_LEFT:
                            player.rect.left = vehicle.rect.right
                            crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                        elif event.key == K_RIGHT:
                            player.rect.right = vehicle.rect.left
                            crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]

        #pintamos de verde el fondo para el escenario del juego
        screen.fill(green)

        #dibujamos la carretera
        pygame.draw.rect(screen, gray, road)

        #dibujamos los bordes de la carretera
        pygame.draw.rect(screen, yellow, left_edge_marker)
        pygame.draw.rect(screen, yellow, right_edge_marker)

        #dibujar los marcadores de las líneas
        lane_marker_move_y += speed * 2
        if lane_marker_move_y >= marker_height * 2:
            lane_marker_move_y = 0
        for y in range(marker_height * -2, height, marker_height * 2):
            pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
            pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

        #coche del jugador
        player_group.draw(screen)

        #añadir vehículo
        if len(vehicle_group) < 2:
            
            #asegurarse de que hay suficiente distancia entre ambos vehículos
            add_vehicle = True
            for vehicle in vehicle_group:
                if vehicle.rect.top < vehicle.rect.height * 1.5:
                    add_vehicle = False
                    
            if add_vehicle:
                
                #ubicarlo en una de las líneas aleatoriamente
                lane = random.choice(lanes)
                
                #seleccionar una imagen aleatoria para el vehículo
                image = random.choice(vehicle_images)
                vehicle = Vehicle(image, lane, height / -2)
                vehicle_group.add(vehicle)
            
        #mover los vehículos
        for vehicle in vehicle_group:
            vehicle.rect.y += speed
            
            #eliminar vehículo una vez desaparezca de la pantalla
            if vehicle.rect.top >= height:
                vehicle.kill()
                
                #sumar marcador
                score += 1
                
                #aumentar la velocidad por cada 5 vehículos superados
                if score > 0 and score % 5 == 0:
                    speed += 1
        
        #dibujar los vehículos
        vehicle_group.draw(screen)

        #dibujar marcador
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Score: ' + str(score), True, white)
        text_rect = text.get_rect()
        text_rect.center = (50, 400)
        screen.blit(text, text_rect)

        #comprobar colisiones frontales
        if pygame.sprite.spritecollide(player, vehicle_group, True):
            gameover = True
            crash_rect.center = [player.rect.center[0], player.rect.top]

        pygame.display.update()

        #display para el game over
        if gameover:
            screen.blit(crash, crash_rect)
            
            pygame.draw.rect(screen, red, (0, 50, width, 100))
            
            font = pygame.font.Font(pygame.font.get_default_font(), 16)
            text = font.render('Game over. ¿Jugar de nuevo? Sí(y)/No(n)', True, white)
            text_rect = text.get_rect()
            text_rect.center = (width / 2, 100)
            screen.blit(text, text_rect)
                
            pygame.display.update()

            #esperar a que el usario decida si seguir jugando o salir
            while gameover:  
                
                clocK.tick(fps)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        gameover = False
                        run = False
                        
                    #coger el input si(y)/no(n) para reiniciar o salir del juego
                    if event.type == KEYDOWN:
                        if event.key == K_y:
                            #reiniciar el juego
                            gameover = False
                            speed = 2
                            score = 0
                            vehicle_group.empty()
                            player.rect.center = [player_x, player_y]
                        elif event.key == K_n:
                            #salir del bucle
                            gameover = False
                            run = False

    pygame.quit()

gameloop()