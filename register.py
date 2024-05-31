import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

class RegisterWindow:
    '''
    Clase para crear una ventana que nos permita registrar usuarios en nuestra base de datos
    '''
    def __init__(self, master):
        '''
        Constructor en el que creamos la interfaz con los campos para el nombre de usuario y la contraseña y un botón para registrarlo
        '''
        self.master = master #ventana principal
        self.master.title("Registro de usuario")

        self.frame = tk.Frame(master)
        self.frame.pack(pady=20, padx=20)

        self.label_username = tk.Label(self.frame, text="Nuevo Usuario:")
        self.label_username.grid(row=0, column=0, pady=5, padx=5)

        self.entry_username = tk.Entry(self.frame)
        self.entry_username.grid(row=0, column=1, pady=5, padx=5)

        self.label_password = tk.Label(self.frame, text="Contraseña:")
        self.label_password.grid(row=1, column=0, pady=5, padx=5)

        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.grid(row=1, column=1, pady=5, padx=5)

        self.register_button = ttk.Button(self.frame, text="Registrarse", command=self.register_user)
        self.register_button.grid(row=2, columnspan=2, pady=10)

    def register_user(self):
        '''
        Método que coge el nombre y la contraseña introducidas en las cajas de texto para guardarlas en la base de datos en el caso de que no estén vacíos los campos
        '''
        username = self.entry_username.get()
        password = self.entry_password.get()

        #comprobar que los dos campos han sido rellenados
        if username and password:
            try:
                #conexión con la base de datos usando el usuario predeterminado root
                connection = mysql.connector.connect(
                    host='localhost',
                    database='tfg',
                    user='root',
                    password=''
                )

                cursor = connection.cursor() #cursor para realizar peticiones a la base de datos
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password)) #ejecutar la petición
                connection.commit() #hacer commit de la petición para que quede guardada
                messagebox.showinfo("Registro Exitoso", "Usuario registrado con éxito")
            except Error as e:
                messagebox.showerror("Error", str(e))
            finally:
                cursor.close()
                connection.close()
        else:
            messagebox.showerror("Error", "Por favor ingresa un nombre de usuario y contraseña")