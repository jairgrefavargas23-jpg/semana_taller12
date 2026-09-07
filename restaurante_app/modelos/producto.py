class Producto:
    def __init__(self, codigo: str, nombre: str, precio: float, stock: int):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def a_diccionario(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock
        }

    @staticmethod
    def desde_diccionario(data):
        return Producto(data["codigo"], data["nombre"], float(data["precio"]), int(data["stock"]))