# Evaluación: Glosario de clases

## Análisis
El documento incluye el **Glosario de clases** en las Tablas 43 a 53, correspondientes al apartado 13. Se han documentado un total de 11 clases (`Usuario`, `Hacer ruta`, `Ruta predeterminada`, `Ruta no predeterminada`, `Objetivos`, `Donaciones`, `Árbol`, `Tipo de transporte`, `Mantenimiento`, `Empresa de plantación` y `Zona`), las cuales coinciden con las entidades representadas en el diagrama de clases del modelo de dominio (Sección 12).

Cada tabla cumple con la estructura básica requerida:
- **Significado/Descripción:** Todas las clases cuentan con una descripción clara y contextualizada que explica su rol dentro del dominio del problema (ej. *"Representa a las personas que utilizan la aplicación"*, *"Lugares en los que están plantados los árboles..."*).
- **Atributos:** Se listan los atributos principales indicando su tipo de dato (`String`, `Boolean`, `Float`, `Integer`, `Tipo de transporte`), lo que aporta precisión técnica.
- **Métodos/Operaciones:** Se incluyen las operaciones principales. Sin embargo, en varios casos (ej. Tablas 44, 45, 51, 52) la descripción de las operaciones se mezcla con la definición de relaciones y multiplicidades (ej. *"el usuario puede hacer una ruta 0 o muchas veces"*), en lugar de presentar firmas de métodos o comportamientos puramente funcionales.

El trabajo cumple de forma sólida con el nivel de **7/10** de la rúbrica: se han descrito todas las clases, se ha explicado correctamente su significado y se han incluido sus atributos y métodos principales. No alcanza el nivel máximo debido a la falta de formalización en la definición de operaciones (se describen narrativamente y se confunden con asociaciones) y a pequeñas inconsistencias de formato (ej. celda vacía en la Tabla 47, atributos que en realidad son claves foráneas o asociaciones como `Usuario` en la clase `Árbol`).

## Puntuación
**Puntuación:** 7/10

## Observaciones
- **Formalización de operaciones:** Se recomienda describir los métodos con una notación más técnica (nombre, parámetros y tipo de retorno) y separar claramente las operaciones de las relaciones/multiplicidades, las cuales ya quedan reflejadas en el diagrama de clases.
- **Atributos vs. Asociaciones:** Revisar atributos como `Usuario (String)` en la clase `Árbol` o `Empresa de plantación` en `Mantenimiento`. En un modelo de dominio, estos suelen modelarse como asociaciones entre clases, no como atributos primitivos.
- **Consistencia de formato:** Unificar la estructura de las tablas (ej. la Tabla 47 tiene una fila vacía antes de los atributos) y evitar descripciones redundantes en el campo de operaciones.
- **Enumeraciones:** La clase `Tipo de transporte` se define correctamente como enumeración, pero podría listarse explícitamente sus valores literales en el glosario para mayor claridad.