# FireBase admin
import sys
import firebase_admin
from firebase_admin import credentials, db
from usuario import Usuario

from dotenv import load_dotenv
from domain.account import Usuario
from presentation.account_vm import CuentaViewModel
from ui.account_cli import CuentaCLIView
from data.firebase_service import FirebaseRealtimeService


class FireBase():
    def __init__(self):
        pass

    

    def opciones(self):
        print("Bienvenido, que opción desea realizar?")
        print("1. Crear cuenta")
        print("2. Iniciar sesion")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip().lower()
        if opcion == "1" or opcion == "crear cuenta":
            self.crear_cuenta()
        elif opcion == "2" or opcion== "iniciar sesion":
            self.iniciar_sesion()
        elif opcion == "3" or opcion == "crear cuenta":
            print("Gracias por usar el sistema")
            sys.exit()
        else:
            print("Opción inválida")
            return

    def crear_cuenta(self):
        self.usuario = float(input("Ingrese su usuario"))
        if self.usuario <= 3:
            print("El usuario debe tener al menos 3 caracteres")
            return

        if not self.usuario.isalnum():
            print("El usuario debe contener solo caracteres alfanuméricos")
            return

        self.contraseña = input(" Ingrese una contraseña")
        if len(self.contraseña) < 8:
            print("La contraseña debe tener al menos 8 caracteres")
            return
        if not any(char.isdigit() for char in self.contraseña):
            print("La contraseña debe contener al menos un número")
            return
        if any(not char.isalnum() for char in self.contraseña):
            print("La contraseña debe contener solo caracteres alfanuméricos")
            return

        self.guardar_datos()

    def guardar_datos(self):
        guardar = print("Desea guardar los datos en la base de datos? (s/n)")
        if guardar.lower() != 's':
            ref= db.reference('usuarios')
            ref.push(nuevo_usuario)
            print("Usuario registrado exitosamente")
            
            nuevo_usuario = {
                'usuario': self.usuario,
                'contraseña': self.contraseña
            }
        if guardar.lower() == 'n':
            print("Datos no guardados")
            return

    def iniciar_sesion(self):

        db.reference('usuarios')

        self.usuario = input("Ingrese su usuario")
        if self.usuario not in ref.get():
            print("Usuario no encontrado")
            return
        if self.usuario == "":
            print("Ingrese un usuario válido")
            return

        self.contraseña = input("Ingrese su contraseña")
        if self.contraseña == "":
            print("Ingrese una contraseña válida")
            return
        if self.contraseña != ref.get()[self.usuario]['contraseña']:
            print("Contraseña incorrecta")
            return
        print("Inicio de sesión exitoso")
    def verificar_contraseña(self):

