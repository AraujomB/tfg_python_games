import pygame
import random
import math
import sys
import os

#Iniciamos pygame
pygame.init()

#Definimos el tamaño de la pantalla de juego
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Obtenemos la ruta de los recursos
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        #devolvemos la ruta absoluta de los recursos
        return os.path.join(base_path, relative_path)
    
#cargar background
asset_background = resource_path('assets/images/background_alienwar.jpg')
background = pygame.image.load(asset_background)

#cargar icono
asset_icon = resource_path('assets/images/alienwar_icon.png')
icon = pygame.image.load(asset_icon)

#cargar sonido de fondo
asset_sound = resource_path('assets/images/neon-gaming-128925.mp3')
sound = pygame.mixer.music.load(asset_sound)

#cargar imagen nave
asset_player = resource_path('assets/images/ufo.png')
playerimg = pygame.image.load(asset_player)

#cargar imagen enemigos
asset_enemy1 = resource_path('assets/images/enemy1.png')
enemy1 = pygame.image.load(asset_enemy1)
asset_enemy2 = resource_path('assets/images/enemy2.png')
enemy2 = pygame.image.load(asset_enemy2)

#cargar imagen disparo
asset_bullet = resource_path('assets/images/bullet.png')
bulletimg = pygame.image.load(asset_bullet)

#cargar fuente para el texto de game over
asset_game_over = resource_path('assets/fonts/RAVIE.TTF')
game_over_font = pygame.font.Font(asset_game_over, 60)

#cargar fuente para marcador de puntuación
asset_font = resource_path('assets/fonts/comicbd.ttf')
font = pygame.font.Font(asset_font, 32)

#Le damos el nombre a la pantalla
pygame.display.set_caption("Alienwar")

#establecemos icono de ventana
pygame.display.set_icon(icon)

#reproducimos el sonido de fondo en bucle y ajustamos el volumen
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

#reloj para controlar la velocidad del juego
clocK = pygame.time.Clock()

#posicion inicial jugador
playerX = 370
playerY = 470
playerX_change = 0
playerY_change = 0

#lista para almacenar la posicion de los enemigos
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10

#inicializamos variables para guardar las posiciones de los enemigos
for i in range(no_of_enemies):
    enemyimg.append(enemy1)
    enemyimg.append(enemy2)

    #asignamos posicion aleatoria para el enemigo
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0, 150))

    #establecemos la velocidad de movimiento
    enemyX_change.append(5)
    enemyY_change.append(20)

    #inicializamos las variables para guardar la posicion de la bala
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    #inicializamos la puntuacion
    score = 0

    #mostramos la puntuación en la pantalla
    def show_score():
        score_value = font.render("SCORE "+str(score), True, (255, 255, 255))
        screen.blit(score_value, (10, 10))

    #mostrar al jugador en la pantalla
    def show_player(x, y):
        screen.blit(playerimg, (x, y))

    #dibujar enemigo
    def show_enemy(x, y, i):
        screen.blit(enemyimg[i], (x, y))

    #disparar la bala
    def shoot_bullet(x, y):
        global bullet_state

        bullet_state = "fire"
        screen.blit(bulletimg, (x + 16, y + 10))

    #comprobar colision entre la bala y el enemigo
    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX-bulletX, 2)) +
                             (math.pow(enemyY-bulletY, 2)))
        
        if distance < 27:
            return True
        else:
            return False
        
    #mostrar game over
    def game_over_text():
        over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
        text_rect = over_text.get_rect(center=(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2)))
        screen.blit(over_text, text_rect)

    #Bucle en el que se va a ejecutar el juego
    def gameloop():

        #variables globales
        global score
        global playerX
        global playerX_change
        global bulletX
        global bulletY
        global collision
        global bullet_state

        run = True
        while run:
            #manejamos eventos, actualizar y renderizar el juego
            #limpiar pantalla
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    #manejar los movimientos del jugador y el disparo
                    if event.key == pygame.K_LEFT:
                        playerX_change = -5

                    if event.key == pygame.K_RIGHT:
                        playerX_change = 5

                    if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                            bulletX = playerX
                            shoot_bullet(bulletX, bulletY)

                if event.type == pygame.KEYUP:
                    playerX_change = 0

            #actualizamos la posicion del jugador
            playerX += playerX_change

            if playerX <= 0:
                playerX = 0
            elif playerX >= 736:
                playerX = 736

            #bucle para cada enemigo
            for i in range(no_of_enemies):
                if enemyY[i] > 440:
                    for j in range(no_of_enemies):
                        enemyY[j] = 2000
                    game_over_text()
                
                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = 5
                    enemyY[i] += enemyY_change[i]
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -5
                    enemyY[i] += enemyY_change[i]

                #comprobamos colisiones
                collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collision:
                    bulletY = 454
                    bullet_state = "ready"
                    score += 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(0, 150)
                show_enemy(enemyX[i], enemyY[i], i)

            if bulletY < 0:
                bulletY = 454
                bullet_state = "ready"
            if bullet_state == "fire":
                shoot_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            show_player(playerX, playerY)
            show_score()

            pygame.display.update()

            #fps
            clocK.tick(60)

gameloop()