import tkinter as tk
import threading
from importmusic import MusicImporter
from detector_notas import DetectorNotas

root=tk.Tk()
root.title("MUGUI APP") # Configurar el título de la ventana
root.geometry("450x550") # Configurar el tamaño de la ventana
root.config(bg="#323232")  # Configurar el color de fondo de la ventana

actual_frame = None  # Referencia al frame actualmente mostrado

def mostrar_frame(nuevo_frame):

    global actual_frame
    if actual_frame is not None:
        actual_frame.destroy()

    actual_frame = nuevo_frame
    actual_frame.pack(fill="both", expand=True)

 # -----SPLASH SCREEN-----
def ir_splash_screen():
    splash = tk.Frame(root, bg="#323232")
    tk.Label(splash, text="MUGUI", bg="#323232",fg="white",font=("Arial", 24, "bold")).pack(expand=True)
    mostrar_frame(splash)
    root.after(1500, ir_pag_principal)
    
    #global logo_img 
    #logo_img= tk.PhotoImage(file="logo.png")
    #tk.Label(splash_screen, image=logo_img)

 # -----PAGINA PRINCIPAL-----
def ir_pag_principal():
    pagina_principal=tk.Frame(root, bg="#323232")
    tk.Label(pagina_principal, text="¡BIENVENIDO A MUGUI!",bg="#323232", fg="white",font=("Arial", 16, "bold")).pack(pady=20) # Crea una etiqueta
    tk.Button(pagina_principal, text="Iniciar Sesión",command=ir_login, bg="#fc6e20").pack(pady=20) # Crea un botón
    tk.Button(pagina_principal, text="Crear Cuenta",command=ir_crear_cuenta, bg="#fc6e20").pack(pady=10)
    tk.Button(pagina_principal, text="Ir al Menú Principal", command=ir_main_menu, bg="#fc6e20").pack(pady=20)
    mostrar_frame(pagina_principal)

def ir_login():
    pagina_login = tk.Frame(root, bg="#323232")
    tk.Label(pagina_login, text="INICIAR SESIÓN", bg="#323232", fg="white",font=("Arial", 16,"bold")).pack(pady=15)

    tk.Label(pagina_login, text="Usuario: ",bg="#323232", fg="white").pack(pady=5)
    tk.Entry(pagina_login, width=30).pack(pady=5)

    tk.Label(pagina_login, text="Contraseña: ",bg="#323232", fg="white").pack(pady=5)
    tk.Entry(pagina_login, width=30).pack(pady=5) # Crea una espacio de entrada tipo "Input"

    tk.Button(pagina_login, text="Iniciar Sesión", bg="#fc6e20", fg="White").pack(pady=20)
    tk.Label(pagina_login, text="¿Aún no tienes una cuenta? Crea una:",bg="#323232", fg="white").pack(pady=20)
    tk.Button(pagina_login, text="Crear Cuenta",bg="#323232", fg="white",command=ir_crear_cuenta).pack(pady=5)

    tk.Button(pagina_login, text="Volver", command=ir_pag_principal, bg="#323232", fg="white").pack(pady=10)  
    mostrar_frame(pagina_login)

def ir_crear_cuenta():
    pagina_crear_cuenta=tk.Frame(root, bg="#323232")
    tk.Label(pagina_crear_cuenta, text="CREAR CUENTA", bg="#323232", fg="white",font=("Arial", 16,"bold")).pack(pady=15)

    tk.Label(pagina_crear_cuenta, text="Correo: ", bg="#323232", fg="white").pack(pady=5)
    email_entry=tk.Entry(pagina_crear_cuenta, width=40).pack(pady=5)

    tk.Label(pagina_crear_cuenta, text="Usuario: ", bg="#323232", fg="white").pack(pady=5)
    user_entry=tk.Entry(pagina_crear_cuenta, width=30).pack(pady=5)

    tk.Label(pagina_crear_cuenta, text="Contraseña: ", bg="#323232", fg="white").pack(pady=5)
    password_entry=tk.Entry(pagina_crear_cuenta, width=30).pack(pady=5)

    tk.Label(pagina_crear_cuenta, text="Aceptar términos y condiciones",bg="#323232", fg="white").pack(pady=10)  
    tk.Checkbutton(pagina_crear_cuenta, bg="#323232").pack(pady=1) # Crea una casilla de verificación

    tk.Label(pagina_crear_cuenta, text="¿Todo listo para crear una cuenta?", bg="#323232", fg="white").pack(pady=5)
    tk.Button(pagina_crear_cuenta, text="Crear Cuenta", bg="#fc6e20").pack(pady=20)

    tk.Label(pagina_crear_cuenta, text="¿Ya tienes una cuenta creada?", bg="#323232", fg="white").pack(pady=20)
    tk.Button(pagina_crear_cuenta, text="Iniciar Sesión", bg="#323232", fg="white",command=ir_login).pack(pady=5)

    tk.Button(pagina_crear_cuenta, text="Volver", command=ir_pag_principal, bg="#323232", fg="white").pack(pady=10)
    mostrar_frame(pagina_crear_cuenta)

def ir_main_menu():
    panel = tk.Frame(root, bg="#323232")
    tk.Label(panel, text="MENÚ PRINCIPAL", bg="#323232", fg="white", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Button(panel, text="Volver al inicio", command=ir_pag_principal, bg="#323232", fg="White").pack(pady=10)
    mostrar_frame(panel)

    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu)

    menu_perfil = tk.Menu(barra_menu, tearoff=0)
    menu_perfil.add_command(label="Cuenta", command=ir_cuenta)
    menu_perfil.add_command(label="Configuración", command=ir_configuracion)
    menu_perfil.add_separator()
    menu_perfil.add_command(label="Salir", command=root.quit)
    barra_menu.add_cascade(label="Perfil", menu=menu_perfil)

    menu_biblioteca = tk.Menu(barra_menu, tearoff=0)
    menu_biblioteca.add_command(label="Importar Canción", command=ir_importar_cancion)
    menu_biblioteca.add_command(label="Canciones Guardadas", command=ir_canciones_guardadas)
    menu_biblioteca.add_command(label="Detector de Notas", command=ir_detector_notas)
    barra_menu.add_cascade(label="Biblioteca", menu=menu_biblioteca)

def ir_cuenta():
    cuenta_frame = tk.Frame(root, bg="#323232")
    cuenta_frame.pack(fill="both", expand=True)
    tk.Label(cuenta_frame, text="Información de la Cuenta", bg="#323232", fg="white", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Label(cuenta_frame, text="Usuario: ", bg="#323232", fg="white").pack(pady=10)
    tk.Label(cuenta_frame, text="Correo: ", bg="#323232", fg="white").pack(pady=10)
    tk.Button(cuenta_frame, text="Volver", command=ir_main_menu, bg="#323232", fg="white").pack(pady=20)
    mostrar_frame(cuenta_frame)

def ir_configuracion():
    configuracion_frame= tk.Frame(root, bg="#323232")
    tk.Label(configuracion_frame, text="CONFIGURACIÓN", bg="#323232", fg="white", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(configuracion_frame, text="Usuario:", bg="#323232", fg="white").pack(pady=10)
    tk.Button(configuracion_frame, text="EDITAR Usuario", command=ir_cambiar_usuario, bg="#fc6e20", fg="white").pack(pady=10)
    tk.Label(configuracion_frame, text="Contraseña:", bg="#323232", fg="white").pack(pady=10)
    tk.Button(configuracion_frame, text="EDITAR Contraseña", command=ir_cambiar_contraseña, bg="#fc6e20", fg="white").pack(pady=10)

    tk.Label(configuracion_frame, text="Correo:", bg="#323232", fg="white").pack(pady=10)
    tk.Button(configuracion_frame, text="EDITAR Correo", command=ir_cambiar_correo, bg="#fc6e20", fg="white").pack(pady=10)

    tk.Button(configuracion_frame, text="Volver", command=ir_pag_principal, bg="#323232", fg="white").pack(pady=20)
    mostrar_frame(configuracion_frame)

def ir_cambiar_usuario():
    global cambiar_usuario_frame
    cambiar_usuario_frame= tk.Frame(root, bg="#323232")
    tk.Label(cambiar_usuario_frame, text="CAMBIAR USUARIO", bg="#323232", fg="white", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Label(cambiar_usuario_frame, text="Usuario Actual: __________", bg="#323232", fg="white").pack(pady=10)
    tk.Label(cambiar_usuario_frame, text="Ingrese el nuevo usuario", bg="#323232", fg="white").pack(pady=10)
    tk.Entry(cambiar_usuario_frame, width=30).pack(pady=5)

    tk.Button(cambiar_usuario_frame, text="Guardar Cambios", bg="#fc6e20", fg="white").pack(pady=20)
    tk.Button(cambiar_usuario_frame, text="Volver", command=ir_configuracion, bg="#323232", fg="white").pack()
    mostrar_frame(cambiar_usuario_frame)

def ir_cambiar_contraseña():
    global cambiar_contraseña_frame
    cambiar_contraseña_frame= tk.Frame(root, bg="#323232")
    tk.Label(cambiar_contraseña_frame, text="CAMBIAR CONTRASEÑA", bg="#323232", fg="white", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Label(cambiar_contraseña_frame, text="Contraseña Actual: __________", bg="#323232", fg="white").pack(pady=10)
    new_password = tk.Entry(cambiar_contraseña_frame, width=30, show="*").pack(pady=10)

    tk.Button(cambiar_contraseña_frame, text="Guardar Cambios", bg="#fc6e20").pack(pady=20)
    tk.Button(cambiar_contraseña_frame, text="Volver",bg="#323232", fg="white", command=ir_configuracion).pack()

    mostrar_frame(cambiar_contraseña_frame)

def ir_cambiar_correo():
    global cambiar_correo_frame
    cambiar_correo_frame= tk.Frame(root, bg="#323232")
    tk.Label(cambiar_correo_frame, text="CAMBIAR CORREO", bg="#323232", fg="white", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Label(cambiar_correo_frame, text="Correo Actual: __________", bg="#323232", fg="white").pack(pady=10)
    tk.Label(cambiar_correo_frame, text="Ingrese el nuevo correo", bg="#323232", fg="white").pack(pady=10)
    new_email = tk.Entry(cambiar_correo_frame, width=40).pack(pady=5)

    tk.Button(cambiar_correo_frame, text="Guardar Cambios", bg="#fc6e20", fg="white").pack(pady=20)
    tk.Button(cambiar_correo_frame, text="Volver",bg="#323232",fg="white", command=ir_configuracion).pack(pady=20)

    mostrar_frame(cambiar_correo_frame)

def ir_importar_cancion():
    importar_cancion_frame= tk.Frame(root, bg="#323232")
    tk.Label(importar_cancion_frame, text="IMPORTAR CANCIÓN", bg="#323232", fg="white", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Button(importar_cancion_frame, text="Seleccionar Archivo", command=abrir_archivos_canciones).pack(pady=10)
    tk.Button(importar_cancion_frame, text="Volver", command=ir_main_menu, bg="#323232", fg="white").pack(pady=20)
    mostrar_frame(importar_cancion_frame)

def abrir_archivos_canciones():
    t = threading.Thread(target=MusicImporter.import_music, daemon=True)
    t.start()

def ir_canciones_guardadas():
    canciones_guardadas=tk.Frame(root, bg="#323232")
    tk.Label(canciones_guardadas, text="Canciones Guardadas", bg="#323232", fg="white", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Label(canciones_guardadas, text="Ups, al parecer no tienes canciones guardadas.", bg="#323232", fg="white").pack(pady=10)
    tk.Button(canciones_guardadas, text="Volver", command=ir_main_menu, bg="#323232", fg="white").pack(pady=20)
    mostrar_frame(canciones_guardadas)

def ir_detector_notas():
    detector_notas_frame=tk.Frame(root, bg="#323232")
    tk.Label(detector_notas_frame, text="Detector de Notas", bg="#323232", fg="white", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Button(detector_notas_frame, text="Empezar a detectar notas", bg="#fc6e20", fg="white").pack(pady=10)
    tk.Button(detector_notas_frame, text="Volver", command=ir_main_menu, bg="#323232", fg="white").pack(pady=20)
    mostrar_frame(detector_notas_frame)

def iniciar_detector_notas():
    t = threading.Thread(target=DetectorNotas.detector_notas, daemon=True)
    t.start()

if __name__ == "__main__":
    ir_splash_screen()
    root.mainloop() # Ejecuta el bucle principal de la ventana


