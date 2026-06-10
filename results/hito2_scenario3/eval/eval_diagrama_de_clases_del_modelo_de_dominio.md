# Evaluación: Diagrama de clases del modelo de dominio

## Análisis
La evaluación se basa en el apartado 12 (referencia al diagrama) y, principalmente, en el **Glosario de clases (Sección 13, Tablas 43 a 53)**, ya que las imágenes no son accesibles. Un modelo de dominio debe representar exclusivamente **conceptos del mundo real** y sus relaciones, evitando detalles de implementación, elementos de interfaz o acciones del sistema.

**Aspectos positivos:**
- Se identifican entidades centrales alineadas con los requisitos: `Usuario`, `Ruta predeterminada`, `Ruta no predeterminada`, `Objetivos`, `Donaciones`, `Árbol`, `Empresa de plantación`, `Zona`, `Mantenimiento` y `Tipo de transporte`.
- Se reconoce la necesidad de una enumeración para `Tipo de transporte`, lo cual es correcto a nivel conceptual.
- El equipo reconoce explícitamente en la memoria (Sección 3.5) la dificultad para identificar clases y relaciones, lo que evidencia un proceso de reflexión.

**Deficiencias conceptuales y de notación:**
1. **Mezcla de conceptos de dominio con elementos de software/UI:** 
   - `Hacer ruta` (Tabla 44) se describe como una "opción" o acción, no como una entidad. En un modelo de dominio debería ser `Ruta` o `RegistroDeRuta`.
   - `Ruta no predeterminada` incluye atributos `Iniciar (Boolean)` y `Parar (Boolean)`, que son controles de interfaz o estados de ejecución, no propiedades conceptuales.
   - `Empresa de plantación` (Tabla 52) incluye `Contraseña`, un detalle de seguridad/implementación que no pertenece al dominio.
   - Las "Operaciones" listadas en el glosario (ej. `Ver objetivos`, `Realizar donación`, `Enviar donación`) son **operaciones del sistema o casos de uso**, no comportamiento inherente a las entidades del dominio.

2. **Notación y documentación de relaciones:**
   - Las relaciones entre clases no se modelan mediante asociaciones UML con multiplicidades, sino que se describen de forma textual en la columna "Operaciones" (ej. *"Usuario: el usuario puede hacer una ruta 0 o muchas veces..."*). Esto incumple la notación estándar de UML para modelos de dominio.
   - No se especifican cardinalidades claras (1..*, 0..1, etc.) ni roles en las asociaciones.

3. **Conceptos faltantes según los requisitos:**
   - Los requisitos IRQ-001 y CU-005 mencionan explícitamente la gestión de **amistades** y la **competencia**, pero no existe una clase `Amistad`, `Relación` o `RedSocial`.
   - Se menciona `Logro` (IRQ-005, IRQ-006) como concepto diferenciado de `Objetivo`, pero no aparece en el glosario.
   - La gestión de pagos/donaciones (CU-015, IRQ-007) carece de una entidad `Transacción` o `Pago` que registre el flujo monetario de forma conceptual.

En conjunto, el modelo presenta una estructura identificable, pero **no se mantiene en un nivel puramente conceptual** y **no utiliza correctamente la notación UML** para representar asociaciones y responsabilidades. Esto se alinea directamente con el nivel 2/10 de la rúbrica.

## Puntuación
**Puntuación:** 2/10

## Observaciones
- **Separar dominio de implementación:** Eliminar atributos como `Contraseña`, `Iniciar/Parar (Boolean)` y cualquier referencia a botones o flujos de UI. Un modelo de dominio solo debe contener datos estructurales y reglas de negocio.
- **Corregir la naturaleza de las clases:** Reemplazar `Hacer ruta` por `Ruta` o `Actividad`. Diferenciar claramente `Objetivo` (meta futura) de `Logro` (objetivo cumplido).
- **Modelar relaciones con notación UML:** Sustituir la columna "Operaciones" por asociaciones explícitas con multiplicidades (ej. `Usuario 1 ─── 0..* Ruta`, `Empresa 1 ─── 0..* Árbol`, `Árbol * ─── 1 Zona`).
- **Incluir conceptos faltantes:** Añadir clases como `Amistad` (o `RelaciónUsuario`), `Logro` y `Transacción` para cubrir los requisitos de competencia amistosa y gestión de donaciones.
- **Revisar el glosario:** Utilizar un formato estándar que liste: Nombre de la clase, Descripción conceptual, Atributos de dominio y Asociaciones (con multiplicidad y rol), evitando listar operaciones del sistema.