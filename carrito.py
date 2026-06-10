class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class Carrito:
    def __init__(self):
        self.__productos = []

    def agregar_producto(self, producto):
        self.__productos.append(producto)
        print(f"✅ {producto.nombre} agregado.")
# Error de lógica - El total siempre está 1$ por debajo del valor correcto
    def calcular_total(self):
        #return sum(p.precio for p in self.__productos) # -- Original
        return sum(p.precio for p in self.__productos) - 1 # -- Con error
# Error de funcionalidad - El sistema no informa al usuario cuando el carrito está vacío. 
    def mostrar_resumen(self):
        if not self.__productos:
            #print("El carrito está vacío.") # -- Error. (Si comentas esta linea :) ) 
            return
        print("\n--- Resumen de Compra ---")
# Error de parámetro / formato - Rompe test que verifican formato con dos decimales.
        for p in self.__productos:
            #print(f"- {p.nombre}: ${p.precio:.2f}") # -- Original
            print(f"- {p.nombre}: ${p.precio:.0f}") # -- Con error
        print(f"TOTAL: ${self.calcular_total():.2f}\n")

def menu():
    carrito = Carrito()
    # Productos precargados para facilitar el testing
    catalogo = [
        Producto("Notebook", 1500.00),
        Producto("Mouse", 25.50),
        Producto("Teclado", 45.00)
    ]

    while True:
        print("1. Ver Catálogo y Agregar")
        print("2. Ver Carrito y Total")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            for i, p in enumerate(catalogo):
                print(f"{i+1}. {p.nombre} (${p.precio})")
            idx = int(input("Número de producto: ")) - 1
            carrito.agregar_producto(catalogo[idx])
        elif opcion == "2":
            carrito.mostrar_resumen()
        elif opcion == "3":
            break

if __name__ == "__main__":
    menu()