# Trabajo Práctico Final - Testeo de Software

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

<img width="2816" height="1536" alt="Gemini_Generated_Image_ilq30ilq30ilq30i" src="https://github.com/user-attachments/assets/f02b1dce-2671-4df6-8690-8eecb9c1343d" />

---

## 3. Código Fuente e Instrucciones

### Requisitos previos

- Python 3.8 o superior (solo biblioteca estándar).

### Ejecución de la aplicación

```bash
python carrito.py
```

En Linux o macOS:

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

---

## 4. Pruebas (Sprints 2, 3 y 4)

### Sprint 2 — Diseño del conjunto de pruebas (`test_carrito.py`)

Suite de 33 pruebas unitarias con `unittest` que cubre seis tipos de prueba:

| Tipo | Clase | Tests |
|------|-------|-------|
| Componentes | `TestProducto`, `TestCarrito` | 11 |
| Integración | `TestIntegracion` | 3 |
| Caja Negra | `TestCajaNegra` | 5 |
| Rendimiento | `TestRendimiento` | 3 |
| Interfaz CLI | `TestInterfazConsola` | 5 |
| Camino | `TestCamino` | 6 |

**Ejecución:**

```bash
python3 test_carrito.py
```

**Resultado:** 33/33 ✅

---

### Sprint 3 — Planificación y ejecución de pruebas

Documentación del plan de pruebas y evidencia de ejecución de los 33 casos. Ver `Sprint3_Plan_Ejecucion_Pruebas.docx`.

---

### Sprint 4 — Pruebas End-to-End (`tests/e2e_carrito.spec.js`)

Suite de 8 pruebas E2E con [Playwright Test](https://playwright.dev/) que lanza `carrito.py` como proceso real del sistema operativo. No se importa ningún objeto Python: los tests envían inputs por `stdin` y verifican `stdout`, exactamente como lo haría un usuario en la terminal.

| ID | Flujo |
|----|-------|
| E2E-01 | Consultar carrito vacío y salir |
| E2E-02 | Compra simple: Notebook → ver total |
| E2E-03 | Compra múltiple: los tres productos ($1570.50) |
| E2E-04 | Duplicados: Notebook × 2 ($3000.00) |
| E2E-05 | Sesión completa con revisión parcial y final |
| E2E-06 | Salida inmediata sin operar |
| E2E-07 | Navegación repetida al menú antes de comprar |
| E2E-08 | Verificación de formato en catálogo y resumen |

**Requisitos previos:**

- Node.js 18 o superior
- `npm install`

**Ejecución:**

```bash
npx playwright test --reporter=list
```

**Resultado:** 8/8 ✅ en 2.4s

---

## 5. Estructura del repositorio
# Trabajo Práctico Final - Testeo de Software (Sprint 1 y 2)

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

<img width="2816" height="1536" alt="Gemini_Generated_Image_ilq30ilq30ilq30i" src="https://github.com/user-attachments/assets/f02b1dce-2671-4df6-8690-8eecb9c1343d" />


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
### Ejecución de los tests

Para ejecutar las pruebas unitarias, ejecutar el siguiente comando:

```bash
python3 test_carrito.py 
```

### Uso del menú

1. **Ver catálogo y agregar:** muestra Notebook, Mouse y Teclado con precios; se ingresa el número del producto para agregarlo al carrito.
2. **Ver carrito y total:** lista los ítems agregados y el total (formato `$X.XX`).
3. **Salir:** termina el programa.

Se puede agregar el mismo producto varias veces; cada aparición figura como una línea distinta en el resumen.

### Notas

- El catálogo está definido en código para facilitar pruebas; no hay persistencia en archivo ni base de datos.
- Si en la opción 1 se ingresa un número fuera del rango del catálogo, el programa puede lanzar un error (comportamiento no validado en esta versión).

```
├── carrito.py                        # Sistema bajo prueba
├── test_carrito.py                   # Sprint 2: 33 pruebas unittest
├── tests/
│   └── e2e_carrito.spec.js           # Sprint 4: 8 pruebas E2E (Playwright)
├── playwright.config.js              # Configuración Playwright
├── package.json                      # Dependencias Node.js
└── README.md
```
### Defectos intencionales y pruebas diseñadas para detectarlos

Con fines pedagógicos, `carrito.py` incluye **tres defectos deliberados** que permiten validar la efectividad del conjunto de pruebas. Al ejecutar las suites con el código defectuoso, los tests listados a continuación **deben fallar**; al corregir cada defecto, las pruebas asociadas vuelven a pasar.

| ID | Tipo de defecto | Ubicación | Descripción | Corrección |
|----|-----------------|-----------|-------------|------------|
| D-01 | Lógica | `calcular_total()` | El total queda **$1 por debajo** del valor correcto (`sum(...) - 1`). | Eliminar el `- 1`. |
| D-02 | Funcionalidad | `mostrar_resumen()` | No se informa al usuario cuando el carrito está **vacío** (línea comentada). | Descomentar `print("El carrito está vacío.")`. |
| D-03 | Formato / parámetro | `mostrar_resumen()` | Los precios de ítems se muestran **sin dos decimales** (`.0f` en lugar de `.2f`). | Usar `:.2f` en el formato de cada producto. |

#### Pruebas unitarias que fallan (`test_carrito.py`)

| Defecto | ID test | Clase | Qué verifica |
|---------|---------|-------|--------------|
| **D-01** | CC-01 | `TestCarrito` | Carrito vacío: total esperado `0`, obtenido `-1`. |
| **D-01** | CC-02 | `TestCarrito` | Un producto: total esperado `1500.00`, obtenido `1499.00`. |
| **D-01** | CC-03 | `TestCarrito` | Varios productos: suma incorrecta (`1524.50` vs `1525.50`). |
| **D-01** | CC-04 | `TestCarrito` | Mismo producto ×2: total incorrecto (`50.00` vs `51.00`). |
| **D-01** | INT-01 | `TestIntegracion` | Flujo completo: total `$1570.50` incorrecto. |
| **D-01** | RD-02 | `TestRendimiento` | `calcular_total()` con 10.000 ítems: espera `10000.0`, obtiene `9999.0`. |
| **D-01** | RD-03 | `TestRendimiento` | Suma de 1000 × `$0.10`: espera `100.00`, obtiene `99.00`. |
| **D-02** | CC-06 | `TestCarrito` | `mostrar_resumen()` con carrito vacío debe contener `"vacío"`. |
| **D-02** | CB-01 | `TestCajaNegra` | Al consultar carrito vacío desde `menu()`, debe aparecer `"vacío"`. |
| **D-02** | CAM-02 | `TestCamino` | Opción 2 con carrito vacío: rama `"vacío"`. |
| **D-02** | CAM-04 | `TestCamino` | `mostrar_resumen()` con lista vacía (rama M1). |
| **D-03** | IF-03 | `TestInterfazConsola` | Resumen debe mostrar `$1500.00` (con dos decimales). |
| **D-03** | CAM-05 | `TestCamino` | Resumen con Teclado debe incluir `"45.00"`. |
| **D-01 + D-03** | INT-02 | `TestIntegracion` | Resumen debe incluir total `"1545.00"` (formato y cálculo). |
| **D-01 + D-02 + D-03** | CB-02 | `TestCajaNegra` | Notebook agregado: espera `"1500.00"` en salida. |
| **D-01 + D-03** | CB-03 | `TestCajaNegra` | Mouse + Teclado: espera `"70.50"` en total. |
| **D-01 + D-03** | CB-04 | `TestCajaNegra` | Notebook ×2: espera `"3000.00"`. |

**Resumen unitario con defectos activos:** aproximadamente **17 de 33** pruebas fallan.  
**Pruebas que siguen pasando** (no cubren esos defectos): p. ej. CP-01 a CP-04, CC-05, CC-07, INT-03, CB-05, RD-01, IF-01, IF-02, IF-04, IF-05, CAM-01, CAM-03, CAM-06.

#### Pruebas E2E que fallan (`tests/e2e_carrito.spec.js`)

| Defecto | ID | Qué verifica |
|---------|-----|--------------|
| **D-02** | E2E-01 | Consultar carrito vacío: debe contener `"vacío"`. |
| **D-01 + D-03** | E2E-02 | Compra simple: `$1500.00` en ítem y `TOTAL: $1500.00`. |
| **D-01 + D-03** | E2E-03 | Tres productos: `TOTAL: $1570.50`. |
| **D-01 + D-03** | E2E-04 | Notebook ×2: `TOTAL: $3000.00`. |
| **D-01 + D-03** | E2E-05 | Totales parcial (`$25.50`) y final (`$70.50`). |
| **D-02 + D-01** | E2E-07 | Mensaje `"vacío"` al menos 2 veces + `TOTAL: $1500.00`. |
| **D-01 + D-03** | E2E-08 | Formato `$25.50` y `TOTAL: $25.50` en resumen. |

**Resumen E2E con defectos activos:** **7 de 8** pruebas fallan.  
**E2E-06** (salida inmediata sin operar) sigue pasando porque no valida totales ni carrito vacío.

#### Ejecución con defectos activos (resultado esperado)

```bash
python3 test_carrito.py
# Esperado: 18 FAIL, 15 OK

npx playwright test --reporter=list
# Esperado: 7 FAIL, 1 OK (E2E-06)