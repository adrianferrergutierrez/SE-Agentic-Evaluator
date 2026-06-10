# Evaluación: Diagrama de clases del modelo de dominio

## Análisis
El diagrama de clases del modelo de dominio (Imagen 31) aplica correctamente la notación UML estándar: utiliza rectángulos con compartimentos para atributos, líneas de asociación con multiplicidades explícitas (`0..*`, `1`, etc.) y estereotipos adecuados (`<<enumeration>>`). Captura las entidades nucleares del dominio como `Usuario`, `Donación`, `Empresa de plantación`, `Árbol`, `Zona`, `Mantenimiento` y `Objetivos`, lo que evidencia una base conceptual sólida.

No obstante, el modelo presenta desviaciones conceptuales y omisiones respecto a la especificación de requisitos y casos de uso del documento:
- **Clases mal planteadas:** `Hacer ruta` se modela como una clase cuando, en el dominio, representa una acción o caso de uso. Debería ser una entidad conceptual como `Ruta` o `RegistroDeRuta`. Además, aparece una asociación con la clase `Computador` que no está definida en el diagrama.
- **Atributos conceptuales incorrectos:** `Zona` incluye `Habitantes: Float`, un dato irrelevante para la gestión de reforestación; `Árbol` incluye `Cantidad: Integer`, lo que confunde una instancia individual con un agregado o métrica.
- **Falta de cobertura de requisitos:** No se reflejan conceptos clave mencionados en los casos de uso y requisitos, como `Amigo`/`Competencia`, `Logro` (diferenciado explícitamente de `Objetivo` en los IRQ), `Empleado`/`Personal` (distinto de la entidad empresa) o `Transacción`/`Pago`.
- **Notación en asociaciones:** Las líneas de asociación utilizan verbos de acción (`Envía`, `Crear`, `Hacer ruta`) en lugar de nombres de roles o indicadores de navegabilidad estándar en UML.
- **Nivel de abstracción:** El glosario de clases (Tablas 43-53) añade operaciones detalladas, lo que acerca el modelo a un nivel de diseño técnico en lugar de mantenerlo estrictamente como un modelo de dominio conceptual (que debe centrarse en entidades, atributos y relaciones del mundo real).

En conjunto, la notación UML se ha utilizado bien, pero el diagrama no es del todo correcto conceptualmente y omite clases y relaciones derivadas directamente de la especificación de requisitos. Esto se ajusta al descriptor de 7/10 de la rúbrica.

## Puntuación
**Puntuación:** 7/10

## Observaciones
- Renombrar `Hacer ruta` a `Ruta` o `Trayecto` y eliminar la referencia a `Computador` o definirla si es estrictamente necesaria para el dominio.
- Corregir atributos conceptuales: `Zona` debería reflejar ubicación geográfica, coordenadas o hectáreas; `Árbol` debe representar una instancia única (eliminar `Cantidad` y moverlo a un agregado o métrica de usuario).
- Incorporar clases faltantes derivadas de los requisitos: `Amigo` (o relación de amistad), `Logro`, `Empleado` y `Transacción`/`Pago`.
- Sustituir los verbos en las asociaciones por nombres de roles estándar (ej. `donante`, `receptor`, `creador`) y añadir flechas de navegabilidad si corresponde.
- Mantener el diagrama estrictamente conceptual: reservar las operaciones y detalles de implementación para el modelo de diseño, no para el modelo de dominio.