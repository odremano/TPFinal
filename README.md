# Trabajo Práctico Final - Testeo de Software (Sprint 1)

**Institución:** Universidad de Belgrano  
**Proyecto:** Sistema de Gestión de Carrito de Compras (POO)

---

## 1. Descriptivo del Software

### 1.1 Objetivo del Software

El objetivo de esta aplicación es proporcionar un motor de lógica de negocio orientado a objetos para la gestión de un carrito de compras en una tienda minorista. El software permite la selección de productos, la acumulación en memoria y el cálculo automático de totales, sirviendo como base para la ejecución de pruebas unitarias, de integración y de caja negra.

### 1.2 Requerimientos Implementados

#### Requerimientos Funcionales (RF)

- **RF-01: Gestión de Catálogo:** El sistema debe permitir visualizar una lista predefinida de productos con sus respectivos precios.
- **RF-02: Adición al Carrito:** El usuario debe poder seleccionar productos del catálogo e integrarlos a su carrito actual.
- **RF-03: Cálculo de Total:** El sistema debe calcular dinámicamente la suma de los precios de todos los productos agregados.
- **RF-04: Resumen de Compra:** El sistema debe listar los ítems seleccionados y mostrar el monto final a pagar.

#### Requerimientos No Funcionales (RNF)

- **RNF-01: Paradigma POO:** El software debe estar desarrollado bajo el paradigma de Programación Orientada a Objetos para facilitar el testeo de componentes.
- **RNF-02: Portabilidad:** La aplicación debe ser ejecutable en cualquier sistema con el intérprete de Python 3.x instalado.
- **RNF-03: Interfaz Consola:** La interacción debe realizarse mediante una interfaz de línea de comandos (CLI) simple y determinista.

---

## 2. Artefactos UML (Diagrama de Clases)

El diseño se basa en la interacción de dos entidades principales:

1. **Clase `Producto`:**
   - **Atributos:** `nombre` (String), `precio` (Float).
   - **Responsabilidad:** Representar la unidad básica de venta.
2. **Clase `Carrito`:**
   - **Atributos:** `__productos` (List - Encapsulado).
   - **Métodos:**
     - `agregar_producto(producto)`: Añade una instancia de Producto a la lista.
     - `calcular_total()`: Itera y suma los precios (Lógica de negocio).
     - `mostrar_resumen()`: Genera la salida de datos para el usuario.

Además, la función `menu()` concentra el catálogo precargado y el bucle de la CLI (opciones 1–3).

---

## 3. Código Fuente e Instrucciones

### Requisitos previos

- Python 3.8 o superior (solo biblioteca estándar).

### Ejecución

Para ejecutar el software y proceder con las pruebas, utilice el siguiente comando en la terminal (desde la carpeta del proyecto):

```bash
python carrito.py
```

En Linux o macOS, si preferís explícitamente el intérprete `python3`:

```bash
python3 carrito.py
```

### Uso del menú

1. **Ver catálogo y agregar:** muestra Notebook, Mouse y Teclado con precios; se ingresa el número del producto para agregarlo al carrito.
2. **Ver carrito y total:** lista los ítems agregados y el total (formato `$X.XX`).
3. **Salir:** termina el programa.

Se puede agregar el mismo producto varias veces; cada aparición figura como una línea distinta en el resumen.

### Notas

- El catálogo está definido en código para facilitar pruebas; no hay persistencia en archivo ni base de datos.
- Si en la opción 1 se ingresa un número fuera del rango del catálogo, el programa puede lanzar un error (comportamiento no validado en esta versión).