Restaurante_App_Sem12

BRYAN JAIR GREFA ALVARADO
Asignatura: Programación Orientada a Objetos
Semana 12 - Taller Práctico

Proyecto de la asignatura Programación Orientada a Objetos. Corresponde a la Semana 12: Utilización de colecciones para la mejora de rendimiento en restaurante_app.

### Estructura del proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
└── README.md

Se conserva la arquitectura modular trabajada en las semanas previas:
* modelos/ contiene las clases del dominio (Producto, Usuario, Venta).
* servicios/ contiene la lógica del negocio (Restaurante) y la persistencia JSON (ArchivoServicio).
* main.py es solo el punto de entrada con el menú, sin lógica de negocio.
* datos/ almacena los archivos JSON que permiten persistir la información.

Mejoras de rendimiento aplicadas en la Semana 12

Se conservan las listas principales (productos, usuarios, ventas) porque siguen siendo útiles para almacenar, recorrer, listar y persistir los objetos. Adicionalmente, dentro del servicio Restaurante se crearon las siguientes estructuras auxiliares en memoria:

| Estructura auxiliar | Tipo | Uso |
| :--- | :--- | :--- |
| `_index_productos` | dict | Índice por codigo de producto para búsquedas O(1). |
| `_index_usuarios` | dict | Índice por identificacion de usuario para búsquedas O(1). |
| `_index_ventas_usuario` | dict | Agrupa las ventas por identificación del usuario. Evita recorrer toda la lista de ventas al hacer una consulta. |
| `_codigos_unicos` | set | Validación rápida (in) de existencia/unicidad de códigos. |

Búsquedas y consultas mejoradas

* Búsqueda de producto por código (`buscar_producto`): antes se recorría toda la lista con un for; ahora se obtiene del diccionario `_index_productos` en un solo paso.
* Búsqueda de usuario por identificación (`buscar_usuario`): también pasa a ser directa gracias al diccionario `_index_usuarios`.
* Consulta de ventas por usuario (`consultar_ventas_por_usuario`): se apoya en el diccionario `_index_ventas_usuario`, evitando recorrer la colección completa de ventas cada vez que se consulta.
* Validaciones de existencia al registrar productos, usuarios o ventas se hacen con set, lo que hace la comprobación in en tiempo constante.

Sincronización de los índices

* Al iniciar el programa, después de cargar los JSON, se llama al método `_reconstruir_indices()` que arma nuevamente los dict y set desde los objetos recuperados.
* Al registrar un producto, usuario o venta, se actualizan tanto la lista principal como el diccionario y el set correspondientes.
* Los cambios se guardan en JSON para conservar la persistencia.

Ejecución del proyecto

Desde la raíz del proyecto ejecutar:
python restaurante_app/main.py

Se mostrará un menú con las opciones para registrar y consultar productos, usuarios y ventas.

Pruebas principales realizadas

1. Ejecutar `main.py`.
2. Cargar los usuarios, productos y ventas iniciales desde los JSON.
3. Buscar un producto por su código (opción 2).
4. Buscar un usuario por su identificación (opción 4).
5. Consultar las ventas de un usuario específico (opción 6).
6. Registrar una nueva venta y verificar que el stock se actualiza y que la venta queda enlazada al usuario correcto (opciones 5 y 6).
7. Verificar que los índices auxiliares permanecen coherentes después de registrar o modificar información.
8. Cerrar y volver a ejecutar el programa: los datos JSON se recuperan correctamente y los índices se reconstruyen automáticamente.