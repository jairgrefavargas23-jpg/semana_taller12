import sys
import os

# Ajuste para importar los módulos correctamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from servicios.restaurante import RestauranteServicio

def menu():
    servicio = RestauranteServicio()

    while True:
        print("\n=== RESTAURANTE APP (SEMANA 12) ===")
        print("1. Registrar Producto")
        print("2. Buscar Producto (Optimizado - Dict)")
        print("3. Registrar Usuario")
        print("4. Buscar Usuario (Optimizado - Dict)")
        print("5. Registrar Venta (Control Stock)")
        print("6. Consultar Ventas por Usuario (Optimizado - Dict)")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cod = input("Código: ")
            nom = input("Nombre: ")
            pre = float(input("Precio: "))
            stk = int(input("Stock: "))
            if servicio.registrar_producto(cod, nom, pre, stk):
                print("¡Producto registrado con éxito!")
            else:
                print("Error: El código ya existe.")

        elif opcion == "2":
            cod = input("Código a buscar: ")
            p = servicio.buscar_producto(cod)
            if p:
                print(f"Encontrado: {p.nombre} | Precio: ${p.precio} | Stock: {p.stock}")
            else:
                print("Producto no encontrado.")

        elif opcion == "3":
            ced = input("Identificación: ")
            nom = input("Nombre: ")
            em = input("Email: ")
            if servicio.registrar_usuario(ced, nom, em):
                print("¡Usuario registrado con éxito!")
            else:
                print("Error: La identificación ya existe.")

        elif opcion == "4":
            ced = input("Identificación a buscar: ")
            u = servicio.buscar_usuario(ced)
            if u:
                print(f"Encontrado: {u.nombre} | Email: {u.email}")
            else:
                print("Usuario no encontrado.")

        elif opcion == "5":
            id_v = input("ID de Venta: ")
            u_id = input("ID Usuario: ")
            p_cod = input("Código Producto: ")
            cant = int(input("Cantidad: "))
            exito, msg = servicio.registrar_venta(id_v, u_id, p_cod, cant)
            print(f"Resultado: {msg}")

        elif opcion == "6":
            u_id = input("ID Usuario: ")
            ventas = servicio.consultar_ventas_por_usuario(u_id)
            if ventas:
                print(f"\n--- Ventas del Usuario {u_id} ---")
                for v in ventas:
                    print(f"Venta ID: {v.id_venta} | Producto: {v.producto_codigo} | Cantidad: {v.cantidad} | Total: ${v.total}")
            else:
                print("No se encontraron ventas para este usuario.")

        elif opcion == "7":
            print("Saliendo de la aplicación...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()