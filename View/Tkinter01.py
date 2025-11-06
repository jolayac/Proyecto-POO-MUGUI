import tkinter as tk

root=tk.Tk()
root.title("MUGUI APP") #Configurar el título de la ventana
root.geometry("450x550") #Configurar el tamaño de la ventana
root.config(bg="#323232")  #Configurar el color de fondo de la ventana
root.config(cursor="circle") #Configurar el cursor de la ventana

 # -----PAGINA PRINCIPAL-----

pagina_principal = tk.Frame(root)
pagina_principal.config(bg="#323232")
pagina_principal.pack(fill="both", expand=True)

tk.Label(pagina_principal, text="¡Bienvenido a MUGUI!",bg="#323232", fg="white",font=("Arial", 16)).pack(pady=20) # Crea una etiqueta

def ir_login():
    pagina_principal.pack_forget()
    pagina_crear_cuenta.pack_forget()
    pagina_login.pack(fill="both", expand=True)

tk.Button(pagina_principal, text="Iniciar Sesión",command=ir_login).pack(pady=20) # Crea un botón
    
def ir_crear_cuenta():
    pagina_principal.pack_forget()
    pagina_login.pack_forget()
    pagina_crear_cuenta.pack(fill="both", expand=True)
    
tk.Button(pagina_principal, text="Crear Cuenta",command=ir_crear_cuenta).pack(pady=10)
    
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
correo=tk.Entry(pagina_crear_cuenta, width=40).pack(pady=5)

tk.Label(pagina_crear_cuenta, text="Usuario: ", bg="#323232", fg="white").pack(pady=5)
usuario=tk.Entry(pagina_crear_cuenta, width=30).pack(pady=5)

tk.Label(pagina_crear_cuenta, text="Contraseña: ", bg="#323232", fg="white").pack(pady=5)
contraseña=tk.Entry(pagina_crear_cuenta, width=30).pack(pady=5)

tk.Label(pagina_crear_cuenta, text="Aceptar términos y condiciones",bg="#323232", fg="white").pack(pady=10)  
tk.Checkbutton(pagina_crear_cuenta, bg="#323232").pack(pady=1) # Crea una casilla de verificación

tk.Label(pagina_crear_cuenta, text="¿Todo listo para crear una cuenta?", bg="#323232", fg="white")
tk.Button(pagina_crear_cuenta, text="Crear Cuenta", bg="#fc6e20").pack(pady=20)

tk.Label(pagina_crear_cuenta, text="¿Ya tienes una cuenta creada?", bg="#323232", fg="white").pack(pady=20)
tk.Button(pagina_crear_cuenta, text="Iniciar Sesión", bg="#323232", fg="white",command=ir_login).pack(pady=5)

root.mainloop() # Ejecuta el bucle principal de la ventana
