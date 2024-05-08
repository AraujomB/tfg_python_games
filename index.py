import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess

class GamesInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Portal de Juegos TFG PABLO ARAUJO")

        self.frame = tk.Frame(master, bg="white")
        self.frame.pack(pady=50)

        self.label = tk.Label(self.frame, text=f"Portal de juegos TFG Pablo Araujo", font=("Helvetica", 16), bg="white")
        self.label.pack(pady=20)

        # Cargar la imagen para el botón de Snake
        image_snake = Image.open("assets/images/snake_button.jpeg")
        image_snake = image_snake.resize((50, 50), Image.BILINEAR)
        self.photo_snake = ImageTk.PhotoImage(image_snake)

        self.button_snake = ttk.Button(self.frame, text="Jugar Snake", command=self.play_snake, image=self.photo_snake, compound=tk.LEFT)
        self.button_snake.pack(padx=20, pady=10)

        # Cargar la imagen para el botón de Alienwar
        image_alien = Image.open("assets/images/alienwar_button.jpg")
        image_alien = image_alien.resize((50, 50), Image.BILINEAR)
        self.photo_alien = ImageTk.PhotoImage(image_alien)

        self.button_alien = ttk.Button(self.frame, text="Jugar Alienwar", command=self.play_alien, image=self.photo_alien, compound=tk.LEFT)
        self.button_alien.pack(padx=20, pady=10)

    def play_snake(self):
        subprocess.run(["python", "snake.py"])

    def play_alien(self):
        subprocess.run(["python", "alienwar.py"])

# Crear la ventana principal
root = tk.Tk()

# Crear la interfaz de juegos
interfaz = GamesInterface(root)

# Centrar la ventana en la pantalla
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

# Evitar que el usuario pueda redimensionar la ventana
root.resizable(False, False)

# Iniciar el bucle de eventos
root.mainloop()