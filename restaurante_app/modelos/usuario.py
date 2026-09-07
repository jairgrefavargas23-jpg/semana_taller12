class Usuario:
    def __init__(self, identificacion: str, nombre: str, email: str):
        self.identificacion = identificacion
        self.nombre = nombre
        self.email = email

    def a_diccionario(self):
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "email": self.email
        }

    @staticmethod
    def desde_diccionario(data):
        return Usuario(data["identificacion"], data["nombre"], data["email"])