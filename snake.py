import turtle
import time
import random

#Clásico juego de Snake usando la librería turtle de Python

delay = 0.1 #para posponer la ejecución del programa

#marcador
score = 0
high_score = 0

#Establecemos la configuración de la pantalla del juego
screen = turtle.Screen()
screen.title("Juego de Snake con Turtle")
screen.bgcolor('green')
screen.setup(width=800, height=800)
screen.tracer(0)

#creamos la serpiente, en este caso la cabeza
snake = turtle.Turtle() #creamos objeto turtle
snake.speed(0)
snake.shape("square") #definimos la forma del objeto
snake.color('black')
snake.penup() #quitamos el rastro del objeto al moverse
snake.goto(0, 0)
snake.direction = "stop"

#creamos la comida de la serpierte
comida = turtle.Turtle()
comida.speed(0)
comida.shape("turtle")
comida.color("red")
comida.penup()
comida.goto(0,100)

#cuerpo serpiente
segmentos = []

#marcador
texto = turtle.Turtle()
texto.speed(0) #para que al abrir la pantalla el texto esté ya dibujado
texto.color("white")
texto.penup()
texto.hideturtle()
texto.goto(0,360)
texto.write("Puntuación: 0       Máxima puntuación: 0", align="center", font=("Courier", 22, "normal"))

#funciones para el movimiento
def arriba():
    snake.direction = "up"
def abajo():
    snake.direction = "down"
def izquierda():
    snake.direction = "left"
def derecha():
    snake.direction = "right"

def mov():
    if snake.direction == "up":
        y = snake.ycor()
        snake.sety(y+20)
    if snake.direction == "down":
        y = snake.ycor()
        snake.sety(y-20)
    if snake.direction == "left":
        x = snake.xcor()
        snake.setx(x-20)
    if snake.direction == "right":
        x = snake.xcor()
        snake.setx(x+20)

#configuramos el teclado
screen.listen()
screen.onkeypress(arriba, "Up")
screen.onkeypress(abajo, "Down")
screen.onkeypress(derecha, "Right")
screen.onkeypress(izquierda, "Left")

#bucle del juego
while True:
    screen.update()

    #interaccion con la comida
    if snake.distance(comida) < 20:
        x = random.randint(-360, 360)
        y = random.randint(-360, 360)
        comida.goto(x,y)
        #creamos los nuevos segmentos para alargar la serpiente
        segmento = turtle.Turtle()
        segmento.speed(0)
        segmento.shape("square")
        segmento.color('grey')
        segmento.penup()
        segmentos.append(segmento)

        #aumentar marcador
        score += 10

        if score > high_score:
            high_score = score

        texto.clear()
        texto.write("Puntuación: {}       Máxima puntuación: {}".format(score, high_score), align="center", font=("Courier", 22, "normal"))

    #movemos el cuerpo de la serpiente
    total_segmentos = len(segmentos)
    for elemento in range(total_segmentos -1, 0, -1): #hacemos que cada elemento siga a su predecesor para animar el cuerpo, decrecemos el valor de la lista para que no nos de error al intentar interactuar con el último elemento
        x = segmentos[elemento - 1].xcor()
        y = segmentos[elemento - 1].ycor()
        segmentos[elemento].goto(x,y)

    if total_segmentos > 0:
        x = snake.xcor()
        y = snake.ycor()
        segmentos[0].goto(x,y)

    #controlar las colisiones con los bordes de la pantalla
    if snake.xcor() > 380 or snake.xcor() < -380 or snake.ycor() > 380 or snake.ycor() < -380:
        time.sleep(1)
        snake.goto(0,0)
        snake.direction = "stop"
        
        #eliminamos los segmentos de la pantalla al reiniciar
        for segmento in segmentos:
            segmento.goto(1000,1000)

        segmentos.clear()
        #reseteamos marcador
        score = 0
        texto.clear()
        texto.write("Puntuación: {}       Máxima puntuación: {}".format(score, high_score), align="center", font=("Courier", 22, "normal"))

        
    mov()

    #controlamos la colision con el cuerpo
    for segmento in segmentos:
        if segmento.distance(snake) < 20:
            time.sleep(1)
            snake.goto(0,0)
            snake.direction = "stop"
        
            #eliminamos los segmentos de la pantalla al reiniciar
            for segmento in segmentos:
                segmento.goto(1000,1000)

            segmentos.clear()
            #reseteamos marcador
            score = 0
            texto.clear()
            texto.write("Puntuación: {}       Máxima puntuación: {}".format(score, high_score), align="center", font=("Courier", 22, "normal"))

    time.sleep(delay)