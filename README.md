# Proyecto-POO
# new
Registra un nuevo usuario después de pedir un nombre de usuario y una contraseña. El nombre de usuario se verifica para que no se repita en la base de datos y la contraseña debe ser de más de 8 dígitos y debe contener al menos un número para ser válida.

    Ingrese un comando:
    > new
    Ingrese nombre de usuario: Seba
    Ingrese clave: asfaf2
    Error: La clave debe tener al menos 8 caracteres

    Ingrese un comando:
    > new
    Ingrese nombre de usuario: Seba
    Ingrese clave: NAsdnk23
    Usuario creado en memoria. Usa 'save' para guardar en la base de datos.

# save
Guarda los datos del usuario en la base de datos en tiempo real de Firebase. Agrega el nombre de usuario y la contraseña.
## En la terminal
    Ingrese un comando:
    > save
## En DB de Firebase 
![alt text](<Screenshot 2025-10-16 at 23.54.34.png>)

# del
Elimina la cuenta ingresada de la base de datos.
## Antes
![alt text](<Screenshot 2025-10-16 at 23.57.26.png>)
## Despues de del
![alt text](<Screenshot 2025-10-16 at 23.57.59.png>)

# login
Sirve para verificar los datos de usuario y contraseña de un usuario. Verifica que la contraseña coincida con el usuario.
    Ingrese un comando:
    > login
    Ingrese nombre de usuario: Camilo
    Ingrese clave: Asdas213
    Error: clave incorrecta


    Ingrese un comando:
    > login
    Ingrese nombre de usuario: Camilo
    Ingrese clave: Portaaaa21
    Inicio de sesión exitoso

    Datos del perfil: usuario=Camilo, clave=Portaaaa21

# exit
cierra el programa.
    Ingrese un comando:
    > exit
    Gracias por usar el sistema
    Seba' Proyecto-POO-MUGUI % 