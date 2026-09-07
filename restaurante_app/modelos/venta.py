class Venta:
    def __init__(self, id_venta: str, usuario_id: str, producto_codigo: str, cantidad: int, total: float):
        self.id_venta = id_venta
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad
        self.total = total

    def a_diccionario(self):
        return {
            "id_venta": self.id_venta,
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad,
            "total": self.total
        }

    @staticmethod
    def desde_diccionario(data):
        return Venta(
            data["id_venta"],
            data["usuario_id"],
            data["producto_codigo"],
            int(data["cantidad"]),
            float(data["total"])
        )