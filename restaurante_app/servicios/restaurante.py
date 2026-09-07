import os
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    # Rutas relativas para lectura y escritura JSON
    RUTA_PRODUCTOS = os.path.join("restaurante_app", "datos", "productos.json")
    RUTA_USUARIOS = os.path.join("restaurante_app", "datos", "usuarios.json")
    RUTA_VENTAS = os.path.join("restaurante_app", "datos", "ventas.json")

    def __init__(self):
        # Colecciones principales (Listas para persistencia y recorrido)
        self.productos = []
        self.usuarios = []
        self.ventas = []

        # Estructuras auxiliares (Índices en memoria para búsquedas O(1))
        self._index_productos = {}      # dict: codigo -> objeto Producto
        self._index_usuarios = {}       # dict: identificacion -> objeto Usuario
        self._index_ventas_usuario = {} # dict: usuario_id -> list[Venta]
        self._codigos_unicos = set()    # set: para validaciones de existencia rapidas

        self.cargar_datos()

    def _reconstruir_indices(self):
        """Reconstruye todos los índices auxiliares desde las listas principales."""
        self._index_productos = {p.codigo: p for p in self.productos}
        self._index_usuarios = {u.identificacion: u for u in self.usuarios}
        self._codigos_unicos = {p.codigo for p in self.productos}

        self._index_ventas_usuario = {}
        for v in self.ventas:
            if v.usuario_id not in self._index_ventas_usuario:
                self._index_ventas_usuario[v.usuario_id] = []
            self._index_ventas_usuario[v.usuario_id].append(v)

    def cargar_datos(self):
        datos_prod = ArchivoServicio.cargar_json(self.RUTA_PRODUCTOS)
        self.productos = [Producto.desde_diccionario(d) for d in datos_prod]

        datos_usr = ArchivoServicio.cargar_json(self.RUTA_USUARIOS)
        self.usuarios = [Usuario.desde_diccionario(d) for d in datos_usr]

        datos_ventas = ArchivoServicio.cargar_json(self.RUTA_VENTAS)
        self.ventas = [Venta.desde_diccionario(d) for d in datos_ventas]

        self._reconstruir_indices()

    def guardar_datos(self):
        ArchivoServicio.guardar_json(self.RUTA_PRODUCTOS, [p.a_diccionario() for p in self.productos])
        ArchivoServicio.guardar_json(self.RUTA_USUARIOS, [u.a_diccionario() for u in self.usuarios])
        ArchivoServicio.guardar_json(self.RUTA_VENTAS, [v.a_diccionario() for v in self.ventas])

    # --- PRODUCTOS ---
    def registrar_producto(self, codigo: str, nombre: str, precio: float, stock: int) -> bool:
        if codigo in self._codigos_unicos:
            return False

        nuevo = Producto(codigo, nombre, precio, stock)
        self.productos.append(nuevo)
        
        # Sincronización inmediata de índices
        self._index_productos[codigo] = nuevo
        self._codigos_unicos.add(codigo)
        
        self.guardar_datos()
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        # Búsqueda optimizada por clave O(1)
        return self._index_productos.get(codigo)

    # --- USUARIOS ---
    def registrar_usuario(self, identificacion: str, nombre: str, email: str) -> bool:
        if identificacion in self._index_usuarios:
            return False

        nuevo = Usuario(identificacion, nombre, email)
        self.usuarios.append(nuevo)
        
        # Sincronización del índice
        self._index_usuarios[identificacion] = nuevo
        self.guardar_datos()
        return True

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        # Búsqueda optimizada por clave O(1)
        return self._index_usuarios.get(identificacion)

    # --- VENTAS ---
    def registrar_venta(self, id_venta: str, usuario_id: str, producto_codigo: str, cantidad: int) -> tuple[bool, str]:
        usuario = self.buscar_usuario(usuario_id)
        if not usuario:
            return False, "Usuario no existe."

        producto = self.buscar_producto(producto_codigo)
        if not producto:
            return False, "Producto no existe."

        if producto.stock < cantidad:
            return False, f"Stock insuficiente. Disponible: {producto.stock}"

        producto.stock -= cantidad
        total = producto.precio * cantidad

        nueva_venta = Venta(id_venta, usuario_id, producto_codigo, cantidad, total)
        self.ventas.append(nueva_venta)

        # Sincronización del índice de ventas agrupadas
        if usuario_id not in self._index_ventas_usuario:
            self._index_ventas_usuario[usuario_id] = []
        self._index_ventas_usuario[usuario_id].append(nueva_venta)

        self.guardar_datos()
        return True, "Venta realizada con éxito."

    def consultar_ventas_por_usuario(self, usuario_id: str) -> list[Venta]:
        # Consulta optimizada O(1)
        return self._index_ventas_usuario.get(usuario_id, [])