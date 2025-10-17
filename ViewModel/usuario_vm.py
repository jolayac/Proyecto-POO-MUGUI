import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
# import json
from Model.usuario import Usuario
class UsuarioViewModel:
    def __init__(self):
        self.usuario_actual = None  # Almacena el usuario en memoria
        # Configura Firebase
        cred_path = os.getenv('FIREBASE_CREDENTIALS_JSON')  # Lee la ruta del archivo .json
        cred = credentials.Certificate(cred_path)  # Carga las credenciales
        firebase_admin.initialize_app(cred, {
            'databaseURL': os.getenv('FIREBASE_DB_URL')  # Lee la URL de la BD
        })
        self.ref = db.reference('usuarios')  # Referencia a la tabla 'usuarios' en Firebase

    # Crea un nuevo usuario y lo guarda en memoria
    def crear_usuario(self, usuario, clave):
        # Valida que el usuario no exista en la base de datos
        usuarios = self.ref.get()
        if usuarios:
            for key, data in usuarios.items():
                if data['usuario'] == usuario:
                    print("Error: El usuario ya existe")
                    return False
        # Valida el nombre de usuario
        if len(usuario) < 3:
            print("Error: El usuario debe tener al menos 3 caracteres")
            return False
        if not usuario.isalnum():
            print("Error: El usuario debe ser alfanumérico")
            return False
        # Valida la clave
        if len(clave) < 8:
            print("Error: La clave debe tener al menos 8 caracteres")
            return False
        if not any(char.isdigit() for char in clave):
            print("Error: La clave debe tener al menos un número")
            return False
        # Crea el usuario en memoria
        self.usuario_actual = Usuario(usuario, clave)
        print("Usuario creado en memoria. Usa 'save' para guardar en la base de datos.\n")
        return True

    # Guarda el usuario actual en Firebase
    def guardar_usuario(self):
        if self.usuario_actual is None:
            print("Error: No hay usuario para guardar")
            return
        # Convierte el usuario a diccionario y lo guarda
        data = self.usuario_actual.to_dict()
        self.ref.child(self.usuario_actual.usuario).set(data)
        print("Usuario guardado en Firebase\n")

    # Inicia sesión verificando usuario y clave
    def iniciar_sesion(self, usuario, clave):
        usuarios = self.ref.get()
        if usuarios is None:
            print("Error: No hay usuarios registrados")
            return False
        for key, data in usuarios.items():
            if data['usuario'] == usuario:
                if data['clave'] == clave:
                    self.usuario_actual = Usuario(usuario, clave)
                    print("Inicio de sesión exitoso\n")
                    print(f"Datos del perfil: usuario={data['usuario']}, clave={data['clave']}")
                    return True
                else:
                    print("Error: clave incorrecta\n")
                    return False
        print("Error: Usuario no encontrado\n")
        return False

    # Elimina un usuario de Firebase
    def eliminar_usuario(self, usuario):
        usuarios = self.ref.get()
        if usuarios is None:
            print("Error: No hay usuarios registrados\n")
            return False
        for key, data in usuarios.items():
            if data['usuario'] == usuario:
                self.ref.child(key).delete()
                print(f"Usuario {usuario} eliminado\n")
                if self.usuario_actual and self.usuario_actual.usuario == usuario:
                    self.usuario_actual = None
                return True
        print("Error: Usuario no encontrado\n")
        return False