# Evaluación: Diagrama de clases del modelo de dominio

## Análisis
El documento presenta un modelo de dominio estructurado a través del **Glosario de Clases (Tabla 50)** y **Enumeraciones (Tabla 51)**, complementado con referencias a imágenes del diagrama UML. Se identifican conceptos centrales alineados con los requisitos: `Usuario`, `Administrador`, `Voluntario`, `Beneficiario`, `Donación`, `Inscripción`, `Voluntariado`, `Solicitud`, `Beca/Ayuda`, y una jerarquía con `Lugar` como clase base para `Refugio` y `Comedor`. 

Sin embargo, se detectan varias desviaciones respecto a un modelo de dominio conceptual puro y a la especificación de requisitos:
1. **Entidades faltantes:** Requisitos clave como `IRQ-008 (ONG)` y `CRQ-001/CRQ-002 (Reserva de recursos)` no tienen representación explícita en el glosario, a pesar de ser fundamentales para la gestión de donaciones y la disponibilidad de comedores/refugios.
2. **Inclusión de comportamiento:** El modelo lista métodos como `registrar()`, `iniciarSesion()`, `gestionarUsuarios()` o `asignarBeca()`. En un modelo de dominio conceptual, estos pertenecen a la capa de aplicación/servicios, no a las entidades del dominio, lo cual contamina la abstracción conceptual.
3. **Inconsistencia en la modelización de roles:** El registro de cambios indica que se añadió un atributo booleano `esAdministrador` en `Usuario`, pero el glosario mantiene `Administrador`, `Voluntario` y `Beneficiario` como clases independientes sin especificar claramente si heredan de `Usuario` o se relacionan por asociación. Esta ambigüedad dificulta la interpretación correcta de las multiplicidades y la integridad del modelo.
4. **Relaciones y multiplicidades:** Aunque se asume que están representadas en las imágenes referenciadas, el texto no documenta explícitamente los nombres de asociación, roles ni cardinalidades, lo que limita la trazabilidad directa con los casos de uso y requisitos de información.

A pesar de estos puntos, la estructura general es coherente, se utiliza herencia correctamente para `Lugar` → `Refugio`/`Comedor`, se incluyen enumeraciones relevantes (`Estado`, `MetodoDePago`) y el modelo cubre la mayoría de los flujos principales descritos en los casos de uso.

## Puntuación
**Puntuación:** 7/10

## Observaciones
- **Eliminar métodos del modelo de dominio:** Un modelo de dominio debe centrarse en entidades, atributos y relaciones conceptuales. Los métodos de negocio o de interfaz deben trasladarse a diagramas de secuencia o a la capa de servicios.
- **Incorporar clases faltantes:** Añadir `ONG` (para gestionar donaciones y voluntariados) y `Reserva` (para modelar la lógica de bloqueo temporal de plazas en comedores/refugios según CRQ-001/002).
- **Clarificar la jerarquía de roles:** Definir explícitamente si `Administrador`, `Voluntario` y `Beneficiario` heredan de `Usuario` o si se modelan mediante asociación/rol. Evitar mezclar herencia con atributos booleanos (`esAdministrador`) para mantener la pureza conceptual.
- **Documentar asociaciones:** Incluir en el glosario o en una tabla complementaria los nombres de las relaciones, roles y multiplicidades (ej. `Usuario 1..* → Solicitud`, `Voluntariado 0..* → Inscripción`, etc.) para facilitar la trazabilidad con los requisitos.
- **Revisar coherencia con casos de uso:** Asegurar que cada entidad crítica mencionada en los requisitos de información (IRQ) y restricciones (CRQ) tenga su contraparte conceptual en el diagrama.