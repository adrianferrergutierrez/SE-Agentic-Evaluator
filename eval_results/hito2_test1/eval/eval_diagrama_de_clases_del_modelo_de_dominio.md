# Evaluación: Diagrama de clases del modelo de dominio

## Análisis
El documento presenta un apartado específico para el diagrama de clases del modelo de dominio (sección 12) y lo complementa con un glosario de clases detallado (sección 13, tablas 43-53). Aunque se identifica un conjunto de entidades alineadas con los objetivos y requisitos del sistema, el modelo presenta deficiencias estructurales y de notación que limitan su validez como modelo conceptual.

**Evidencias y aciertos:**
- Se han identificado las entidades nucleares del dominio: `Usuario`, `Ruta predeterminada`, `Ruta no predeterminada`, `Objetivos`, `Donaciones`, `Árbol`, `Empresa de plantación`, `Zona` y `Tipo de transporte`.
- Se reconoce la necesidad de una clase `Zona` (mencionada en el registro de cambios) y se utiliza correctamente una enumeración para `Tipo de transporte`.
- El glosario intenta documentar atributos y relaciones, mostrando un esfuerzo por cubrir la especificación de requisitos.

**Errores y desviaciones del modelo de dominio:**
1. **Confusión grave en la notación UML:** En el glosario, las asociaciones estructurales se listan bajo el epígrafe `"Operaciones"` (ej. en `Empresa de plantación`: `"Árbol: planta uno o varios árboles"`, `"Mantenimiento: se encarga del..."`; en `Usuario`: `"Enviar donación"`, `"Competir"`). En UML, las operaciones son comportamientos/métodos con firma, no relaciones de asociación. Esto indica un mal uso de la notación.
2. **Clases orientadas a acciones, no a conceptos:** La clase `Hacer ruta` representa un caso de uso o flujo de interacción, no una entidad del dominio. Un modelo conceptual debe abstraer `Ruta` (con un atributo `tipo` o una generalización) en lugar de nominalizar verbos.
3. **Inclusión de detalles de implementación/UI:** Atributos como `Contraseña` en `Empresa de plantación`, `Iniciar/Parar (Boolean)` en `Ruta no predeterminada` o `Número de cuenta` en `Donaciones` pertenecen al nivel de diseño técnico o interfaz, no al modelo de dominio conceptual.
4. **Atributos mal tipados o redundantes:** En `Árbol`, el atributo `Usuario (String)` debería modelarse como una asociación con multiplicidad. En `Mantenimiento`, el atributo `Mantenimiento a realizar(Boolean)` es ambiguo y no representa un concepto de negocio claro.
5. **Conceptos clave omitidos:** Los requisitos IRQ-005 (`Historial de objetivos`), IRQ-006 (`Compartir logros`), IRQ-007 (`Donación` con trazabilidad) y el CU-005 (`Competir con amigos`) implican la existencia de clases como `Logro`, `Historial`, `Amistad` (o asociación reflexiva en `Usuario`) y `Transacción/Pago`, las cuales no aparecen en el glosario ni se infieren en el diagrama.
6. **Multiplicidades no formalizadas:** Aunque se mencionan textualmente (`"0 o varias"`, `"uno o varios"`), no se representan con la notación UML estándar en el diagrama gráfico, lo que dificulta la validación de la integridad estructural.

En conjunto, el modelo parte de una base conceptual adecuada y cubre parcialmente la especificación, pero contiene demasiados errores de notación, mezcla de niveles de abstracción y omisiones de clases derivadas directamente de los requisitos. Esto se alinea con el nivel intermedio-bajo de la rúbrica.

## Puntuación
**Puntuación:** 3/10

## Observaciones
- **Corregir la notación UML:** Separar estrictamente `Atributos`, `Operaciones` (métodos con firma, ej. `registrarPlantacion(fecha: Date)`) y `Asociaciones` (con nombre, rol y multiplicidad UML, ej. `1..*`). Las relaciones nunca deben listarse como operaciones.
- **Eliminar clases de acción y nominalizaciones verbales:** Sustituir `Hacer ruta` por una clase `Ruta` con un atributo `tipo: TipoRuta` o una jerarquía de herencia (`RutaPredeterminada`, `RutaEspontanea`).
- **Abstraer detalles técnicos:** Eliminar atributos como `Contraseña`, `Iniciar/Parar (Boolean)` o `Número de cuenta`. El modelo de dominio debe centrarse exclusivamente en conceptos del negocio y sus reglas.
- **Incluir clases faltantes:** Añadir `Logro`, `Historial`, `Amistad` (o asociación reflexiva `amigos` en `Usuario` con multiplicidad `0..*`) y `Transacción` para cubrir IRQ-005, IRQ-006, IRQ-007 y CU-005.
- **Formalizar multiplicidades y roles:** Utilizar la notación estándar en el diagrama gráfico (ej. `Usuario "1" --- "0..*" Ruta : "realiza"`) y evitar descripciones textuales en las operaciones.
- **Validar coherencia con la matriz de requisitos:** Realizar un cruce sistemático entre cada IRQ/CU y las clases del modelo para garantizar que no queden conceptos del dominio sin representar, manteniendo siempre un nivel estrictamente conceptual (sin lógica de aplicación ni persistencia).