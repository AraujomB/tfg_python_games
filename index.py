import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from register import RegisterWindow
from PIL import Image, ImageTk
import subprocess, pygame

class GamesInterface:
    '''
    Clase para crear nuestra interfaz de juegos en la que establecemos una configuración predeterminada para cuando sea instanciada
    '''
    def __init__(self, master):
        '''
        constructor en el cual creamos todos los apartados de nuestra interfaz y definimos los botones de cada juego y la configuración de la ventana
        '''
        self.master = master #ventana principal
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

        #cargar las imágenes y crear los botones para cada juego
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

        #botón de Cerrar Sesión
        self.logout_button = ttk.Button(self.master, text="Cerrar Sesión", command=self.logout)
        self.logout_button.pack(side=tk.BOTTOM, padx=20, pady=10)

    def logout(self):
        '''
        método para cerrar sesión desde la interfaz de juegos y volver al login
        '''
        #detener la música de fondo
        pygame.mixer.music.stop()

        #destruir la ventana actual (interfaz de juegos)
        self.master.destroy()

        #crear una nueva ventana de inicio de sesión
        root = tk.Tk()
        login = LoginWindow(root)
        root.geometry("300x200")
        root.resizable(False, False)
        root.mainloop()

    def play_snake(self):
        """
        Método para ejecutar el script del juego Snake
        """
        #detenemos la música de la interfaz
        pygame.mixer.music.stop()
        subprocess.run(["python", "games/snake.py"])
        #reanudamos la música una vez salgamos del juego
        pygame.mixer.music.play(-1)

    def play_alien(self):
        """
        Método para ejecutar el script del juego Alienwar
        """
        pygame.mixer.music.stop()
        subprocess.run(["python", "games/alienwar.py"])
        pygame.mixer.music.play(-1)

    def play_cars(self):
        """
        Método para ejecutar el script del juego Cars
        """
        pygame.mixer.music.stop()
        subprocess.run(["python", "games/cars.py"])
        pygame.mixer.music.play(-1)

class LoginWindow:
    """
    Clase para crear una ventana de login y tener un control de usuarios para poder acceder a nuestra interfaz de juegos
    """
    def __init__(self, master):
        '''
        Declaramos todos los campos para el nombre de usuario y la contraseña
        y los botones para iniciar sesión o registrarse
        '''
        self.master = master
        self.master.title("Inicio de Sesión")

        self.frame = tk.Frame(master)
        self.frame.pack(pady=20, padx=20)

        self.label_username = tk.Label(self.frame, text="Usuario:")
        self.label_username.grid(row=0, column=0, pady=5, padx=5)

        self.entry_username = tk.Entry(self.frame)
        self.entry_username.grid(row=0, column=1, pady=5, padx=5)

        self.label_password = tk.Label(self.frame, text="Contraseña:")
        self.label_password.grid(row=1, column=0, pady=5, padx=5)

        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.grid(row=1, column=1, pady=5, padx=5)

        self.login_button = ttk.Button(self.frame, text="Iniciar Sesión", command=self.check_credentials)
        self.login_button.grid(row=2, columnspan=2, pady=10)

        self.register_button = ttk.Button(self.frame, text="Registrarse", command=self.open_register_window)
        self.register_button.grid(row=3, columnspan=2, pady=10)

        #centramos la ventana en la pantalla
        self.center_window()

    def center_window(self):
        '''
        Método para centrar la ventana de inicio de sesión en nuestra pantalla
        '''
        #obtener las dimensiones de la pantalla
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        #calcular las coordenadas para centrar la ventana
        x_coordinate = int((screen_width / 2) - (300 / 2))  #ancho de la ventana emergente
        y_coordinate = int((screen_height / 2) - (200 / 2))  #alto de la ventana emergente

        #establecer la posición de la ventana en las coordenadas calculadas
        self.master.geometry("+{}+{}".format(x_coordinate, y_coordinate))

    def check_credentials(self):
        '''
        Comprobar si el usuario y la contraseña dados en el inicio de sesión corresponden con la base de datos
        '''
        username = self.entry_username.get()
        password = self.entry_password.get()

        #conexión con la base de datos usando el user predeterminado root
        connection = mysql.connector.connect(
            host='localhost',
            database='tfg',
            user='root',
            password=''
        )

        #comprobar que la conexión con la base de datos ha ido correctamente
        if connection.is_connected():
            cursor = connection.cursor() #cursor para mandar peticiones a la base de datos
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password)) #petición que queremos ejecutar, en este caso que nos recoja los datos del usuario con el nombre y contraseña introducidos
            user = cursor.fetchone() #recoger la primera línea de la respuesta a la petición echa en el execute
            
            #comprobar si ha devuelto el usuario
            if user:
                messagebox.showinfo("Inicio de sesión exitoso", f"Bienvenido, {username}!")
                self.master.destroy()
                main()
            else:
                messagebox.showerror("Fallo en el inicio de sesión", "Usuario o contraseña incorrecto/a")
        else:
            messagebox.showerror("Error de conexión", "No se pudo conectar a la base de datos")

        #cerrar conexión
        cursor.close()
        connection.close()

    def open_register_window(self):
        '''
        Mostrar la ventana de registro de usuario
        '''
        self.master.withdraw() #ocultar la ventana de login sin destruirla
        register_root = tk.Toplevel(self.master) #crear una ventana independiente para el registro de usuarios asociada a la ventana de login
        RegisterWindow(register_root)
        register_root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(register_root)) #protocolo para llamar al método on_closing() cuando el usuario cierre la ventana

    def on_closing(self, register_root):
        '''
        Función para restaurar la visibilidad de la ventana de inicio de sesión una vez se cierre la de registro de usuario
        '''
        register_root.destroy() #cerrar la ventana liberando los recursos asociados a ella
        self.master.deiconify() #restaurar la visibilidad de la ventana principal a la que está asociada

def main():
    #Crear la ventana principal
    root = tk.Tk()

    #Crear la interfaz de juegos con las configuraciones definidas en la clase
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

if __name__ == "__main__":
    root = tk.Tk()
    login = LoginWindow(root)
    root.geometry("300x200")
    root.mainloop()