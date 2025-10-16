# Crea el sistema de registro e inicio de sesion para usuarios

class usuario:
    def __init__(self, opciones, crear_cuenta, iniciar_sesion, guardar_datos):
        self.opciones = opciones
        self.crear_cuenta = crear_cuenta
        self.iniciar_sesion = iniciar_sesion
        self.guardar_datos = guardar_datos
        self.verificar_contraseña = verificar_contraseña
        self.usuario = ""
        self.edad = 0
        self.contraseña = ""
        self.guardar = ""
        self.iniciar_sesion = ""   
        self.nuevo_usuario = {}
        self.ref = db.reference('usuarios')


        def opciones(self):
            print("Bienvenido, que opción desea realizar?")
            print("1. Crear cuenta")
            print("2. Iniciar sesión")
            print("3. Salir")
            opcion = int(input("Seleccione una opción: "))
           
            if opcion == 1:
                self.crear_cuenta() 
            elif opcion == 2:
                self.iniciar_sesion()
            elif opcion == 3:
                print("Gracias por usar el sistema")
                exit()
            else:
                print("Opción inválida")
                return
            
        def crear_cuenta(self, usuario, edad, contraseña):
            self.usuario = float(input("Ingrese su usuario"))
            if self.nombre <=3:
                print("El usuario debe tener al menos 3 caracteres")
                return
            
            if not self.usuario.isalnum():
                print("El usuario debe contener solo caracteres alfanuméricos")
                return

            self.edad = int(input(" ingrese su edad"))
            if self.edad < 0 or self.edad > 120:
                print("Edad inválida")
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

        def guardar_datos(self, guardar):
            guardar = print("Desea guardar los datos en la base de datos? (s/n)")
            if guardar.lower() != 's':
                ref = db.reference('usuarios')
                ref.push(nuevo_usuario)
                print("Usuario registrado exitosamente")
                nuevo_usuario = {
                    'usuario': self.usuario,
                    'edad': self.edad,
                    'contraseña': self.contraseña
                }
               
            if guardar.lower() == 'n':
                print("Datos no guardados")
                return

    def iniciar_sesion(self, iniciar_sesion, contraseña,):
            ref = db.reference('usuarios')

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