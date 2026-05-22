# Evaluación: Glosario de clases

## Análisis
El glosario de clases se encuentra documentado en la **Tabla 50** del documento, aunque el apartado `3.2 Modelo de dominio` contiene el encabezado `GLOSARIO DE CLASES` sin contenido inmediato, lo que dificulta ligeramente su localización. 

La tabla incluye **11 clases** identificadas en el modelo de dominio: `Usuario`, `Administrador`, `Voluntario`, `Beneficiario`, `Donación`, `Inscripción`, `Voluntariado`, `Solicitud`, `Beca/Ayuda`, `Lugar`, `Refugio` y `Comedor`. Para cada una de ellas se proporciona:
- **Descripción:** Explicación clara del significado y rol de la clase dentro del sistema (ej. *"Usuario: Representa a cualquier persona que interactúa con el sistema"*).
- **Atributos:** Listado de los datos principales que almacena cada clase (ej. `idUsuario, nombre, apellido, dni, correo, telefono, direccion, fechaNacimiento`).
- **Métodos:** Operaciones o comportamientos clave asociados a la clase (ej. `registrar(), iniciarSesion(), realizarDonacion(), inscribirseVoluntariado()`).

El contenido es coherente con los casos de uso, actores y requisitos funcionales descritos en secciones anteriores, y cumple con la estructura esperada para un glosario de clases en ingeniería del software. Sin embargo, no alcanza el nivel máximo debido a detalles de rigor técnico: algunas clases como `Refugio` y `Comedor` carecen de métodos (se indica `-`), la clase `Beca/Ayuda` agrupa dos entidades conceptuales distintas sin justificación, y no se especifican tipos de datos, visibilidad ni relaciones entre clases, aspectos que suelen esperarse en una documentación de nivel avanzado.

## Puntuación
**Puntuación:** 7/10

## Observaciones
- **Localización y estructura:** Vincular explícitamente la Tabla 50 en el apartado `3.2 GLOSARIO DE CLASES` o mover la tabla a esa sección mejoraría la navegación y coherencia del documento.
- **Completitud de métodos:** Añadir al menos un método de consulta o gestión a `Refugio` y `Comedor` (ej. `consultarDisponibilidad()`, `actualizarCapacidad()`) evitaría el uso de `-` y reflejaría mejor su comportamiento en el sistema.
- **Precisión conceptual:** Separar `Beca` y `Ayuda` en dos clases distintas o justificar su agrupación mejoraría la fidelidad al modelo de dominio y a los requisitos de información.
- **Rigor técnico:** Incluir tipos de datos para los atributos (ej. `String`, `Date`, `Double`) y visibilidad (`+`, `-`, `#`) elevaría la calidad del glosario y facilitaría su transición directa a código o diagramas UML detallados.