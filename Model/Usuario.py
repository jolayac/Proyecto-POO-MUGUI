class Usuario:
    def __init__(self, usuario, clave):
        self.usuario = usuario
        self.clave = clave

    # Convierte los datos del usuario a un diccionario para guardar en Firebase
    def to_dict(self):
        return {
            'usuario': self.usuario,
            'clave': self.clave
        }

    # Crea un usuario a partir de un diccionario (para cargar desde Firebase)
    def from_dict(self, data):
        return Usuario(
            usuario=data['usuario'],
            clave=data['clave']
        )