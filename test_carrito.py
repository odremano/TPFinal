"""
================================================================================
  TRABAJO PRÁCTICO FINAL — Punto 2: Diseño del Conjunto de Pruebas
  Materia: Control de Calidad de Software
  Sistema bajo prueba: Carrito de Compras (POO) — carrito.py
================================================================================

Tipos de prueba implementados:
  2.1  Prueba de Componentes   (TestProducto, TestCarrito)
  2.2  Prueba de Integración   (TestIntegracion)
  2.3  Prueba de Caja Negra    (TestCajaNegra)
  2.4  Prueba de Rendimiento   (TestRendimiento)
  2.5  Prueba de Interfaz      (TestInterfazConsola)
  2.6  Prueba de Camino        (TestCamino)
"""

import unittest
import time
import io
import sys
from unittest.mock import patch
from carrito import Producto, Carrito, menu


# ══════════════════════════════════════════════════════════════════════════════
# 2.1  PRUEBA DE COMPONENTES
#      Verifica cada clase/método de forma aislada, sin dependencias externas.
# ══════════════════════════════════════════════════════════════════════════════

class TestProducto(unittest.TestCase):
    """Pruebas de componente para la clase Producto."""

    def test_creacion_con_valores_validos(self):
        """CP-01: Un Producto se crea correctamente con nombre y precio."""
        p = Producto("Notebook", 1500.00)
        self.assertEqual(p.nombre, "Notebook")
        self.assertEqual(p.precio, 1500.00)

    def test_precio_puede_ser_entero(self):
        """CP-02: El precio acepta valores enteros (Python los trata como float)."""
        p = Producto("Mouse", 25)
        self.assertEqual(p.precio, 25)

    def test_precio_puede_ser_cero(self):
        """CP-03: El precio puede ser 0 (producto gratuito/promocional)."""
        p = Producto("Folleto", 0)
        self.assertEqual(p.precio, 0)

    def test_nombre_puede_ser_cadena_vacia(self):
        """CP-04: El atributo nombre no impone restricciones de contenido."""
        p = Producto("", 10.0)
        self.assertEqual(p.nombre, "")


class TestCarrito(unittest.TestCase):
    """Pruebas de componente para la clase Carrito."""

    def setUp(self):
        self.carrito = Carrito()
        self.p1 = Producto("Notebook", 1500.00)
        self.p2 = Producto("Mouse", 25.50)

    def test_carrito_inicia_vacio(self):
        """CC-01: Un Carrito recién creado tiene total igual a 0."""
        self.assertEqual(self.carrito.calcular_total(), 0)

    def test_agregar_un_producto(self):
        """CC-02: Tras agregar un producto, el total refleja su precio."""
        self.carrito.agregar_producto(self.p1)
        self.assertEqual(self.carrito.calcular_total(), 1500.00)

    def test_agregar_multiples_productos(self):
        """CC-03: El total es la suma correcta de todos los productos agregados."""
        self.carrito.agregar_producto(self.p1)
        self.carrito.agregar_producto(self.p2)
        self.assertAlmostEqual(self.carrito.calcular_total(), 1525.50, places=2)

    def test_agregar_mismo_producto_dos_veces(self):
        """CC-04: Agregar el mismo objeto dos veces duplica su precio en el total."""
        self.carrito.agregar_producto(self.p2)
        self.carrito.agregar_producto(self.p2)
        self.assertAlmostEqual(self.carrito.calcular_total(), 51.00, places=2)

    def test_encapsulamiento_lista_interna(self):
        """CC-05: El atributo __productos no es accesible directamente (name mangling)."""
        with self.assertRaises(AttributeError):
            _ = self.carrito.__productos

    def test_mostrar_resumen_carrito_vacio(self):
        """CC-06: mostrar_resumen imprime un mensaje cuando el carrito está vacío."""
        captured = io.StringIO()
        sys.stdout = captured
        self.carrito.mostrar_resumen()
        sys.stdout = sys.__stdout__
        self.assertIn("vacío", captured.getvalue())

    def test_mostrar_resumen_con_productos(self):
        """CC-07: mostrar_resumen incluye el nombre del producto y el total."""
        self.carrito.agregar_producto(self.p1)
        captured = io.StringIO()
        sys.stdout = captured
        self.carrito.mostrar_resumen()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("Notebook", output)
        self.assertIn("TOTAL", output)


# ══════════════════════════════════════════════════════════════════════════════
# 2.2  PRUEBA DE INTEGRACIÓN
#      Verifica la colaboración entre Producto y Carrito como un flujo completo.
# ══════════════════════════════════════════════════════════════════════════════

class TestIntegracion(unittest.TestCase):
    """Pruebas de integración: Producto ↔ Carrito."""

    def test_flujo_agregar_y_calcular(self):
        """INT-01: Flujo completo — crear productos, agregarlos y verificar total."""
        carrito = Carrito()
        carrito.agregar_producto(Producto("Notebook", 1500.00))
        carrito.agregar_producto(Producto("Mouse", 25.50))
        carrito.agregar_producto(Producto("Teclado", 45.00))
        self.assertAlmostEqual(carrito.calcular_total(), 1570.50, places=2)

    def test_resumen_refleja_todos_los_productos_agregados(self):
        """INT-02: mostrar_resumen lista todos los productos previamente agregados."""
        carrito = Carrito()
        carrito.agregar_producto(Producto("Notebook", 1500.00))
        carrito.agregar_producto(Producto("Teclado", 45.00))
        captured = io.StringIO()
        sys.stdout = captured
        carrito.mostrar_resumen()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("Notebook", output)
        self.assertIn("Teclado", output)
        self.assertIn("1545.00", output)

    def test_multiples_carritos_son_independientes(self):
        """INT-03: Dos instancias de Carrito no comparten estado."""
        c1 = Carrito()
        c2 = Carrito()
        c1.agregar_producto(Producto("Notebook", 1500.00))
        self.assertEqual(c2.calcular_total(), 0)


# ══════════════════════════════════════════════════════════════════════════════
# 2.3  PRUEBA DE CAJA NEGRA
#      Prueba el sistema desde la perspectiva del usuario final (entradas/salidas),
#      sin conocer la implementación interna.
# ══════════════════════════════════════════════════════════════════════════════

class TestCajaNegra(unittest.TestCase):
    """
    Pruebas de caja negra sobre la función menu().
    Se simulan las entradas del usuario y se verifica la salida en consola.
    """

    @patch("builtins.input", side_effect=["2", "3"])
    def test_cb_carrito_vacio_al_iniciar(self, mock_input):
        """CB-01: Al arrancar y consultar el carrito sin agregar nada, aparece mensaje de vacío."""
        captured = io.StringIO()
        sys.stdout = captured
        menu()
        sys.stdout = sys.__stdout__
        self.assertIn("vacío", captured.getvalue())

    @patch("builtins.input", side_effect=["1", "1", "2", "3"])
    def test_cb_agregar_notebook_y_ver_total(self, mock_input):
        """CB-02: Agregar el producto 1 (Notebook $1500) y verificar el total."""
        captured = io.StringIO()
        sys.stdout = captured
        menu()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("Notebook", output)
        self.assertIn("1500.00", output)

    @patch("builtins.input", side_effect=["1", "2", "1", "3", "2", "3"])
    def test_cb_agregar_dos_productos_distintos(self, mock_input):
        """CB-03: Agregar Mouse ($25.50) y Teclado ($45.00); total esperado $70.50."""
        captured = io.StringIO()
        sys.stdout = captured
        menu()
        sys.stdout = sys.__stdout__
        self.assertIn("70.50", captured.getvalue())

    @patch("builtins.input", side_effect=["1", "1", "1", "1", "2", "3"])
    def test_cb_agregar_mismo_producto_dos_veces(self, mock_input):
        """CB-04: Agregar Notebook dos veces; total esperado $3000.00."""
        captured = io.StringIO()
        sys.stdout = captured
        menu()
        sys.stdout = sys.__stdout__
        self.assertIn("3000.00", captured.getvalue())

    @patch("builtins.input", side_effect=["3"])
    def test_cb_salir_sin_operar(self, mock_input):
        """CB-05: Seleccionar "Salir" de inmediato no produce error."""
        try:
            menu()
        except Exception as e:
            self.fail(f"menu() lanzó una excepción inesperada: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 2.4  PRUEBA DE RENDIMIENTO
#      Verifica que las operaciones críticas respondan dentro de umbrales aceptables.
# ══════════════════════════════════════════════════════════════════════════════

class TestRendimiento(unittest.TestCase):
    """Pruebas de rendimiento sobre Carrito con volúmenes de datos altos."""

    def test_agregar_10000_productos_bajo_1_segundo(self):
        """RD-01: Agregar 10.000 productos debe completarse en menos de 1 segundo."""
        carrito = Carrito()
        productos = [Producto(f"Prod-{i}", float(i)) for i in range(10000)]
        inicio = time.time()
        for p in productos:
            carrito.agregar_producto(p)
        duracion = time.time() - inicio
        self.assertLess(duracion, 1.0,
            f"agregar_producto tardó {duracion:.3f}s para 10.000 items (límite: 1s)")

    def test_calcular_total_10000_productos_bajo_100ms(self):
        """RD-02: calcular_total() con 10.000 productos debe responder en < 100ms."""
        carrito = Carrito()
        for i in range(10000):
            carrito.agregar_producto(Producto(f"Prod-{i}", 1.0))
        inicio = time.time()
        total = carrito.calcular_total()
        duracion = time.time() - inicio
        self.assertEqual(total, 10000.0)
        self.assertLess(duracion, 0.1,
            f"calcular_total tardó {duracion:.4f}s para 10.000 items (límite: 0.1s)")

    def test_precision_numerica_con_muchos_decimales(self):
        """RD-03: La suma de 1000 productos con precio $0.10 debe dar exactamente $100.00."""
        carrito = Carrito()
        for _ in range(1000):
            carrito.agregar_producto(Producto("Centavo", 0.10))
        self.assertAlmostEqual(carrito.calcular_total(), 100.00, places=2)


# ══════════════════════════════════════════════════════════════════════════════
# 2.5  PRUEBA DE INTERFAZ (CLI)
#      Verifica que los mensajes mostrados al usuario sean correctos y completos.
# ══════════════════════════════════════════════════════════════════════════════

class TestInterfazConsola(unittest.TestCase):
    """
    Pruebas de interfaz sobre la salida de texto de la CLI.
    Se valida que el menú, el catálogo y el resumen tengan el formato correcto.
    """

    @patch("builtins.input", side_effect=["3"])
    def test_menu_muestra_tres_opciones(self, mock_input):
        """IF-01: El menú principal debe mostrar las opciones 1, 2 y 3."""
        captured = io.StringIO()
        sys.stdout = captured
        menu()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("1.", output)
        self.assertIn("2.", output)
        self.assertIn("3.", output)

    @patch("builtins.input", side_effect=["1", "1", "3"])
    def test_catalogo_muestra_precios_con_formato(self, mock_input):
        """IF-02: Al ver el catálogo, los precios deben aparecer en formato numérico."""
        captured = io.StringIO()
        sys.stdout = captured
        menu()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("1500", output)
        self.assertIn("25.5", output)

    @patch("builtins.input", side_effect=["1", "1", "2", "3"])
    def test_resumen_muestra_precio_con_dos_decimales(self, mock_input):
        """IF-03: El resumen de compra debe mostrar precios con exactamente 2 decimales."""
        captured = io.StringIO()
        sys.stdout = captured
        menu()
        sys.stdout = sys.__stdout__
        # $1500.00 debe aparecer en el resumen
        self.assertIn("$1500.00", captured.getvalue())

    @patch("builtins.input", side_effect=["1", "1", "2", "3"])
    def test_confirmacion_al_agregar_producto(self, mock_input):
        """IF-04: Al agregar un producto, el sistema debe confirmar con un mensaje."""
        captured = io.StringIO()
        sys.stdout = captured
        menu()
        sys.stdout = sys.__stdout__
        # El mensaje de confirmación contiene "agregado"
        self.assertIn("agregado", captured.getvalue())

    def test_resumen_incluye_cabecera_y_total(self):
        """IF-05: mostrar_resumen debe incluir una cabecera y la etiqueta TOTAL."""
        carrito = Carrito()
        carrito.agregar_producto(Producto("Mouse", 25.50))
        captured = io.StringIO()
        sys.stdout = captured
        carrito.mostrar_resumen()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("Resumen", output)
        self.assertIn("TOTAL", output)


# ══════════════════════════════════════════════════════════════════════════════
# 2.6  PRUEBA DE CAMINO (Prueba de Camino Básico / Cobertura de Ramas)
#      Cubre todos los caminos de ejecución posibles en el flujo de control.
# ══════════════════════════════════════════════════════════════════════════════

class TestCamino(unittest.TestCase):
    """
    Pruebas de camino basadas en el grafo de flujo de menu() y mostrar_resumen().

    Caminos identificados en menu():
      C1: opción inválida → continúa el bucle (no hay handler definido)
      C2: opción "1" → ver catálogo → agregar producto
      C3: opción "2" con carrito vacío → mensaje vacío
      C4: opción "2" con productos → mostrar resumen
      C5: opción "3" → salir (break)

    Caminos en mostrar_resumen():
      M1: lista vacía → rama "vacío"
      M2: lista con items → rama "resumen completo"
    """

    @patch("builtins.input", side_effect=["3"])
    def test_camino_c5_salir_directo(self, mock_input):
        """CAM-01 (C5): Seleccionar salir en el primer ciclo termina el programa."""
        try:
            menu()
        except StopIteration:
            self.fail("menu() no manejó correctamente la opción de salir.")

    @patch("builtins.input", side_effect=["2", "3"])
    def test_camino_c3_ver_carrito_vacio(self, mock_input):
        """CAM-02 (C3): Opción 2 con carrito vacío toma la rama 'vacío'."""
        captured = io.StringIO()
        sys.stdout = captured
        menu()
        sys.stdout = sys.__stdout__
        self.assertIn("vacío", captured.getvalue())

    @patch("builtins.input", side_effect=["1", "1", "2", "3"])
    def test_camino_c2_c4_agregar_y_ver_resumen(self, mock_input):
        """CAM-03 (C2→C4): Agregar producto y luego ver resumen toma ambas ramas."""
        captured = io.StringIO()
        sys.stdout = captured
        menu()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("Notebook", output)
        self.assertIn("TOTAL", output)

    def test_camino_m1_resumen_lista_vacia(self):
        """CAM-04 (M1): mostrar_resumen con lista vacía toma la rama de retorno temprano."""
        carrito = Carrito()
        captured = io.StringIO()
        sys.stdout = captured
        carrito.mostrar_resumen()
        sys.stdout = sys.__stdout__
        self.assertIn("vacío", captured.getvalue())

    def test_camino_m2_resumen_lista_con_items(self):
        """CAM-05 (M2): mostrar_resumen con items toma la rama de iteración completa."""
        carrito = Carrito()
        carrito.agregar_producto(Producto("Teclado", 45.00))
        captured = io.StringIO()
        sys.stdout = captured
        carrito.mostrar_resumen()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("45.00", output)
        self.assertNotIn("vacío", output)

    @patch("builtins.input", side_effect=["1", "1", "1", "2", "1", "3", "2", "3"])
    def test_camino_ciclo_multiple_iteraciones(self, mock_input):
        """CAM-06: El bucle ejecuta múltiples iteraciones correctamente (3 ciclos antes de salir)."""
        captured = io.StringIO()
        sys.stdout = captured
        menu()
        sys.stdout = sys.__stdout__
        # Notebook ($1500) + Teclado ($45) en el resumen
        output = captured.getvalue()
        self.assertIn("TOTAL", output)


# ══════════════════════════════════════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    unittest.main(verbosity=2)