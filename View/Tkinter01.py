import tkinter as tk

root=tk.Tk()
root.title("MUGUI APP") #Configurar el título de la ventana
root.geometry("450x550") #Configurar el tamaño de la ventana
root.config(bg="#323232")  #Configurar el color de fondo de la ventana

 # -----SPLASH SCREEN-----
def ir_splash_screen():
    splash_screen = tk.Frame(root, bg="#323232")
    splash_screen.pack(fill="both", expand=True)

    global logo_img 
    logo_img= tk.PhotoImage(file="logo.png")

    tk.Label(splash_screen, image=logo_img, bg="#323232").pack(pady=20)
    tk.Label(splash_screen, text="MUGUI", bg="#323232",fg="white",font=("Arial", 24, "bold")).pack(expand=True)

    root.after(4000, lambda: ir_pag_principal(splash_screen))

 # -----PAGINA PRINCIPAL-----
def ir_pag_principal(splash_frame):
    splash_frame.destroy()

    global pagina_principal
    pagina_principal=tk.Frame(root, bg="#323232")
    pagina_principal.pack(fill="both", expand=True)

    tk.Label(pagina_principal, text="¡Bienvenido a MUGUI!",bg="#323232", fg="white",font=("Arial", 16)).pack(pady=20) # Crea una etiqueta
    tk.Button(pagina_principal, text="Iniciar Sesión",command=ir_login).pack(pady=20) # Crea un botón
    tk.Button(pagina_principal, text="Crear Cuenta",command=ir_crear_cuenta).pack(pady=10)

def ir_login():
    pagina_principal.pack_forget()
    pagina_crear_cuenta.pack_forget()
    pagina_login.pack(fill="both", expand=True)
    
def ir_crear_cuenta():
    pagina_principal.pack_forget()
    pagina_login.pack_forget()
    pagina_crear_cuenta.pack(fill="both", expand=True)
    
 # -----PAGINA DE INICIO DE SESIÓN-----

pagina_login = tk.Frame(root)
pagina_login.config(bg="#323232")
tk.Label(pagina_login, text="INICIAR SESIÓN", bg="#323232", fg="white",font=("Arial", 16,"bold")).pack(pady=15)

tk.Label(pagina_login, text="Usuario: ",bg="#323232", fg="white").pack(pady=5)
tk.Entry(pagina_login, width=30).pack(pady=5)

tk.Label(pagina_login, text="Contraseña: ",bg="#323232", fg="white").pack(pady=5)
tk.Entry(pagina_login, width=30).pack(pady=5)

tk.Button(pagina_login, text="Iniciar Sesión", bg="#fc6e20", fg="White").pack(pady=20)
tk.Label(pagina_login, text="¿Aún no tienes una cuenta? Crea una:",bg="#323232", fg="white").pack(pady=20)
tk.Button(pagina_login, text="Crear Cuenta",bg="#323232", fg="white",command=ir_crear_cuenta).pack(pady=5)

# -----PAGINA DE CREAR CUENTA-----

pagina_crear_cuenta=tk.Frame(root)
pagina_crear_cuenta.config(bg="#323232")
tk.Label(pagina_crear_cuenta, text="CREAR CUENTA", bg="#323232", fg="white",font=("Arial", 16,"bold")).pack(pady=15)

tk.Label(pagina_crear_cuenta, text="Correo: ", bg="#323232", fg="white").pack(pady=5)
email=tk.Entry(pagina_crear_cuenta, width=40).pack(pady=5)

tk.Label(pagina_crear_cuenta, text="Usuario: ", bg="#323232", fg="white").pack(pady=5)
user=tk.Entry(pagina_crear_cuenta, width=30).pack(pady=5)

tk.Label(pagina_crear_cuenta, text="Contraseña: ", bg="#323232", fg="white").pack(pady=5)
password=tk.Entry(pagina_crear_cuenta, width=30).pack(pady=5)

tk.Label(pagina_crear_cuenta, text="Aceptar términos y condiciones",bg="#323232", fg="white").pack(pady=10)  
tk.Checkbutton(pagina_crear_cuenta, bg="#323232").pack(pady=1) # Crea una casilla de verificación

tk.Label(pagina_crear_cuenta, text="¿Todo listo para crear una cuenta?", bg="#323232", fg="white").pack(pady=5)
tk.Button(pagina_crear_cuenta, text="Crear Cuenta", bg="#fc6e20").pack(pady=20)

tk.Label(pagina_crear_cuenta, text="¿Ya tienes una cuenta creada?", bg="#323232", fg="white").pack(pady=20)
tk.Button(pagina_crear_cuenta, text="Iniciar Sesión", bg="#323232", fg="white",command=ir_login).pack(pady=5)

ir_splash_screen()
root.mainloop() # Ejecuta el bucle principal de la ventana
