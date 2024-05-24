import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess, pygame

class GamesInterface:
    
    def __init__(self, master):
        self.master = master
        self.master.title("Portal de Juegos TFG PABLO ARAUJO")

        window_width = 900
        window_height = 620

        #configurar el fondo de pantalla
        background_img = Image.open("assets/images/background_interface.jpg")
        background_img = background_img.resize((window_width, window_height), Image.BILINEAR)
        self.background_image = ImageTk.PhotoImage(background_img)
        self.background_label = tk.Label(master, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        #iniciamos pygame para poner música de fondo
        pygame.init()
        pygame.mixer.music.load("assets\sounds\good-night-160166.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

        #obtener el color predominante de la imagen de fondo
        colors = background_img.getcolors(window_width * window_height)
        dominant_color = max(colors, key=lambda x: x[0])[1]
        rgb_color = "#%02x%02x%02x" % dominant_color
        
        #area para los botones de los juegos
        self.frame = tk.Frame(master, bg=rgb_color)
        self.frame.pack(pady=50)

        #https://docs.python.org/es/3.9/library/tkinter.font.html
        title_font =  ('Verdana', 16)
        self.label = tk.Label(self.frame, text=f"MinijuegosTFG.com", font=title_font, bg=rgb_color, fg="white")
        self.label.pack(pady=20)

        #cargar las imágenes y creamos los botones para cada juego
        image_snake = Image.open("assets/images/snake_button.jpeg")
        image_snake = image_snake.resize((100, 100), Image.BILINEAR)
        self.photo_snake = ImageTk.PhotoImage(image_snake)

        self.button_snake = ttk.Button(self.frame, text="Jugar Snake", command=self.play_snake, image=self.photo_snake, compound=tk.TOP)
        self.button_snake.pack(side=tk.LEFT, padx=20, pady=10) #con la propiedad side y tk.left colocamos los botones de los juegos uno al lado del otro como si fuera un float en html

        image_alien = Image.open("assets/images/alienwar_button.jpg")
        image_alien = image_alien.resize((100, 100), Image.BILINEAR)
        self.photo_alien = ImageTk.PhotoImage(image_alien)

        self.button_alien = ttk.Button(self.frame, text="Jugar Alienwar", command=self.play_alien, image=self.photo_alien, compound=tk.TOP)
        self.button_alien.pack(side=tk.LEFT, padx=20, pady=10)

        image_cars = Image.open("assets/images/cars_button.jpg")
        image_cars = image_cars.resize((100, 100), Image.BILINEAR)
        self.photo_cars = ImageTk.PhotoImage(image_cars)

        self.button_cars = ttk.Button(self.frame, text="Jugar Cars", command=self.play_cars, image=self.photo_cars, compound=tk.TOP)
        self.button_cars.pack(side=tk.LEFT, padx=20, pady=10)

    def play_snake(self):
        #detenemos la música de la interfaz
        pygame.mixer.music.stop()
        subprocess.run(["python", "games/snake.py"])
        #reanudamos la música una vez salgamos del juego
        pygame.mixer.music.play(-1)

    def play_alien(self):
        pygame.mixer.music.stop()
        subprocess.run(["python", "games/alienwar.py"])
        pygame.mixer.music.play(-1)

    def play_cars(self):
        pygame.mixer.music.stop()
        subprocess.run(["python", "games/cars.py"])
        pygame.mixer.music.play(-1)

#Crear la ventana principal
root = tk.Tk()

#Crear la interfaz de juegos
interfaz = GamesInterface(root)

#Centrar la ventana en la pantalla del usuario
window_width = 900
window_height = 620
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

#evitar que el usuario pueda redimensionar la ventana
root.resizable(False, False)

#iniciar el bucle de eventos
root.mainloop()