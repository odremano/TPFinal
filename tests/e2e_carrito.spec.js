/**
 * ================================================================================
 *  TRABAJO PRÁCTICO FINAL — Sprint 4: Pruebas End-to-End (E2E)
 *  Materia: Control de Calidad de Software — Universidad de Belgrano
 *  Sistema bajo prueba: carrito.py (ejecutado como proceso real)
 *  Framework: Playwright Test (Node.js)
 * ================================================================================
 *
 *  Estrategia E2E:
 *    Cada test lanza `python3 carrito.py` como proceso real usando Node.js
 *    child_process.spawn. Se envían inputs por stdin y se captura la salida
 *    completa de stdout. No se accede a ningún objeto interno Python —
 *    la prueba observa únicamente lo que vería un usuario real en la terminal.
 *
 *  Flujos E2E cubiertos:
 *    E2E-01  Usuario consulta carrito vacío y sale
 *    E2E-02  Compra simple: un producto, ver total, salir
 *    E2E-03  Compra múltiple: tres productos distintos, verificar total acumulado
 *    E2E-04  Compra con duplicados: mismo producto dos veces
 *    E2E-05  Flujo completo de sesión: agregar, revisar, agregar más, revisar final
 *    E2E-06  Salida inmediata sin ninguna operación
 *    E2E-07  Navegación: volver al menú múltiples veces antes de comprar
 *    E2E-08  Verificación de formato de precios en catálogo y resumen
 * ================================================================================
 */

const { test, expect } = require('@playwright/test');
const { spawn }        = require('child_process');
const path             = require('path');

// ── Utilidad: lanza carrito.py con las entradas dadas y resuelve con stdout ──
function runCarrito(inputs) {
  return new Promise((resolve, reject) => {
    const proc = spawn('python3', [path.join(__dirname, '..', 'carrito.py')], {
      stdio: ['pipe', 'pipe', 'pipe'],
    });

    let output = '';
    let error  = '';

    proc.stdout.on('data', d => { output += d.toString(); });
    proc.stderr.on('data', d => { error  += d.toString(); });

    proc.on('close', code => {
      resolve({ output, error, code });
    });

    proc.on('error', reject);

    // Enviar cada input seguido de Enter, con pequeño delay para que el
    // proceso tenga tiempo de mostrar el prompt antes del siguiente input
    let i = 0;
    function sendNext() {
      if (i < inputs.length) {
        proc.stdin.write(inputs[i] + '\n');
        i++;
        setTimeout(sendNext, 20);
      } else {
        proc.stdin.end();
      }
    }
    sendNext();
  });
}

// ════════════════════════════════════════════════════════════════════════════
//  E2E-01 — Usuario consulta carrito vacío y sale
//  Flujo: Inicio → Ver Carrito (opción 2) → Salir (opción 3)
// ════════════════════════════════════════════════════════════════════════════
test('E2E-01 | Consultar carrito vacío y salir', async () => {
  const { output, code } = await runCarrito(['2', '3']);

  expect(code).toBe(0);
  expect(output).toContain('vacío');
  expect(output).not.toContain('TOTAL');
});

// ════════════════════════════════════════════════════════════════════════════
//  E2E-02 — Compra simple: agregar Notebook y ver total
//  Flujo: Inicio → Catálogo (1) → Notebook (1) → Ver Carrito (2) → Salir (3)
// ════════════════════════════════════════════════════════════════════════════
test('E2E-02 | Compra simple: Notebook → ver total', async () => {
  const { output, code } = await runCarrito(['1', '1', '2', '3']);

  expect(code).toBe(0);
  expect(output).toContain('Notebook');
  expect(output).toContain('$1500.00');
  expect(output).toContain('TOTAL: $1500.00');
});

// ════════════════════════════════════════════════════════════════════════════
//  E2E-03 — Compra múltiple: los tres productos del catálogo
//  Flujo: +Notebook → +Mouse → +Teclado → Ver Carrito → Salir
//  Total esperado: $1500.00 + $25.50 + $45.00 = $1570.50
// ════════════════════════════════════════════════════════════════════════════
test('E2E-03 | Compra múltiple: los tres productos, total $1570.50', async () => {
  const { output, code } = await runCarrito([
    '1', '1',   // agregar Notebook
    '1', '2',   // agregar Mouse
    '1', '3',   // agregar Teclado
    '2',        // ver carrito
    '3',        // salir
  ]);

  expect(code).toBe(0);
  expect(output).toContain('Notebook');
  expect(output).toContain('Mouse');
  expect(output).toContain('Teclado');
  expect(output).toContain('TOTAL: $1570.50');
});

// ════════════════════════════════════════════════════════════════════════════
//  E2E-04 — Compra con duplicados: Notebook dos veces
//  Flujo: +Notebook → +Notebook → Ver Carrito → Salir
//  Total esperado: $3000.00
// ════════════════════════════════════════════════════════════════════════════
test('E2E-04 | Duplicados: Notebook × 2 = $3000.00', async () => {
  const { output, code } = await runCarrito([
    '1', '1',
    '1', '1',
    '2',
    '3',
  ]);

  expect(code).toBe(0);
  // Deben aparecer dos líneas con Notebook en el resumen
  const notebookOccurrences = (output.match(/Notebook/g) || []).length;
  expect(notebookOccurrences).toBeGreaterThanOrEqual(2);
  expect(output).toContain('TOTAL: $3000.00');
});

// ════════════════════════════════════════════════════════════════════════════
//  E2E-05 — Sesión completa: agregar, revisar parcial, agregar más, revisar final
//  Flujo: +Mouse → Ver (parcial) → +Teclado → Ver (final) → Salir
//  Total parcial: $25.50  |  Total final: $70.50
// ════════════════════════════════════════════════════════════════════════════
test('E2E-05 | Sesión completa con revisión parcial y final', async () => {
  const { output, code } = await runCarrito([
    '1', '2',   // agregar Mouse
    '2',        // ver carrito parcial
    '1', '3',   // agregar Teclado
    '2',        // ver carrito final
    '3',        // salir
  ]);

  expect(code).toBe(0);
  // Revisión parcial: solo Mouse
  expect(output).toContain('$25.50');
  // Revisión final: Mouse + Teclado
  expect(output).toContain('$45.00');
  expect(output).toContain('TOTAL: $70.50');
});

// ════════════════════════════════════════════════════════════════════════════
//  E2E-06 — Salida inmediata sin ninguna operación
//  Flujo: Inicio → Salir (3)
// ════════════════════════════════════════════════════════════════════════════
test('E2E-06 | Salida inmediata sin operar', async () => {
  const { output, code, error } = await runCarrito(['3']);

  expect(code).toBe(0);
  expect(error).toBe('');
  expect(output).not.toContain('TOTAL');
  expect(output).not.toContain('Error');
});

// ════════════════════════════════════════════════════════════════════════════
//  E2E-07 — Navegación repetida al menú antes de comprar
//  Flujo: Ver Carrito → Ver Carrito → +Notebook → Ver Carrito → Salir
// ════════════════════════════════════════════════════════════════════════════
test('E2E-07 | Navegación repetida al menú principal', async () => {
  const { output, code } = await runCarrito([
    '2',        // ver carrito vacío (1ra vez)
    '2',        // ver carrito vacío (2da vez)
    '1', '1',   // agregar Notebook
    '2',        // ver carrito con Notebook
    '3',        // salir
  ]);

  expect(code).toBe(0);
  // Debe haber aparecido el mensaje de vacío dos veces
  const emptyCount = (output.match(/vacío/g) || []).length;
  expect(emptyCount).toBeGreaterThanOrEqual(2);
  expect(output).toContain('TOTAL: $1500.00');
});

// ════════════════════════════════════════════════════════════════════════════
//  E2E-08 — Verificación de formato de salida en catálogo y resumen
//  Flujo: Ver catálogo → agregar Mouse → ver resumen → salir
// ════════════════════════════════════════════════════════════════════════════
test('E2E-08 | Formato correcto en catálogo y resumen', async () => {
  const { output, code } = await runCarrito(['1', '2', '2', '3']);

  expect(code).toBe(0);

  // Catálogo: los tres productos deben mostrarse con sus nombres
  expect(output).toContain('Notebook');
  expect(output).toContain('Mouse');
  expect(output).toContain('Teclado');

  // Resumen: precio con símbolo $ y dos decimales
  expect(output).toMatch(/\$25\.50/);
  expect(output).toContain('TOTAL: $25.50');

  // El menú debe haberse mostrado (opción 1, 2, 3 presentes)
  expect(output).toContain('1. Ver Catálogo');
  expect(output).toContain('2. Ver Carrito');
  expect(output).toContain('3. Salir');
});
