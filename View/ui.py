class UsuarioView:
    # Constructor: recibe el ViewModel
    def __init__(self, vm):
        self.vm = vm  # Guarda el ViewModel para usarlo

    # Muestra el menú y ejecuta comandos
    def run(self):
        print("Bienvenido al sistema de usuarios.\n")
        print("Comandos: new, save, del, login, exit")
        while True:
            comando = input("\nIngrese un comando:\n> ").strip().lower()
            if comando == "new":
                usuario = input("Ingrese nombre de usuario: ")
                clave = input("Ingrese clave: ")
                self.vm.crear_usuario(usuario, clave)
            elif comando == "save":
                self.vm.guardar_usuario()
            elif comando == "del":
                usuario = input("Ingrese nombre de usuario a eliminar: ")
                self.vm.eliminar_usuario(usuario)
            elif comando == "login":
                usuario = input("Ingrese nombre de usuario: ")
                clave = input("Ingrese clave: ")
                self.vm.iniciar_sesion(usuario, clave)
            elif comando == "exit":
                print("Gracias por usar el sistema")
                break
            else:
                print("Comando inválido. Usa: new, save, del, login, exit.")