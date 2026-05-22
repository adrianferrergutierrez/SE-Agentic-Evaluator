# Evaluación: Memoria técnica

## Análisis
El documento cumple con los requisitos estructurales y de extensión establecidos en la rúbrica:
- **Apartados requeridos:** La sección `3. Memoria técnica` contiene exactamente los 6 apartados solicitados (3.1 Introducción, 3.2 Objetivos, 3.3 Técnicas y herramientas, 3.4 Descripción del grupo, 3.5 Aspectos relevantes, 3.6 Conclusiones).
- **Extensión:** El documento supera ampliamente el mínimo de 5 páginas, incluyendo tablas, glosarios y referencias a diagramas.

Sin embargo, presenta deficiencias significativas en **redacción, formalidad y completitud** que impiden alcanzar una calificación superior:
1. **Tono excesivamente informal:** Se utilizan expresiones coloquiales impropias de una memoria técnica universitaria (ej. `"Nuestro principal método de trabajo ha sido llamarnos y repartirnos el trabajo"`, `"no hemos dado demasiada importancia a los roles"`, `"esta plataforma la han sugerido los profesores"`).
2. **Errores gramaticales y de expresión:** Frases incompletas o mal construidas como `"se introduce de forma general que aborda nuestra aplicación"` (falta un conector o pronombre), `"Se hace cuenta del tiempo total"` (debería ser `"Se lleva cuenta"` o `"Se contabiliza"`), y `"utilizaran"` sin tilde en futuro.
3. **Campos sin rellenar (marcadores de posición):** Múltiples tablas de requisitos de información (IRQ) y no funcionales (NFR) conservan texto genérico sin completar: `<tiempo medio de vida>`, `<importancia del requisito>`, `<urgencia del requisito>`, `<estado del requisito>`, `<estabilidad del requisito>`, `<comentarios adicionales sobre el requisito>`. Esto evidencia falta de revisión final y resta rigor técnico.
4. **Errores de copia-pega y coherencia interna:** 
   - Las Tablas 26 y 27 repiten el identificador `ACT-004 ADMINISTRADOR DE GESTIÓN` para describir actores completamente distintos (GPS y Cuenta Bancaria).
   - El caso de uso `CU-011` se duplica con diferentes nombres (`Gestionar usuarios`, `Activar usuarios`, `Desactivar usuarios`) sin actualizar la numeración, generando inconsistencia con el índice y el diagrama.
   - Algunas tablas de casos de uso presentan columnas duplicadas o desalineadas.

En conjunto, el documento cumple la estructura y longitud, pero la presencia de marcadores sin rellenar, el tono informal y los errores de coherencia lo sitúan en el nivel de **"no está expresado correctamente"** según la rúbrica.

## Puntuación
**Puntuación:** 3/10

## Observaciones
- **Completar todos los campos marcadores:** Rellenar sistemáticamente los campos `<...>` en las tablas de IRQ y NFR con valores reales o justificaciones técnicas. Si no aplica, eliminar la fila o indicar `"N/A"` con una breve explicación.
- **Corregir errores de copia-pega:** Revisar la numeración y descripción de actores (ACT-004) y casos de uso (CU-011, CU-012, CU-013, CU-014) para garantizar unicidad y coherencia con el diagrama de casos de uso.
- **Elevar el registro lingüístico:** Sustituir expresiones coloquiales por un lenguaje técnico y objetivo. Ejemplo: cambiar `"llamarnos y repartirnos el trabajo"` por `"se establecieron reuniones sincrónicas para la distribución y seguimiento de tareas"`.
- **Revisión ortográfica y gramatical:** Corregir acentuación (`utilizarán` → `utilizarán`), concordancia y estructuras sintácticas incompletas. Se recomienda el uso de correctores automáticos y una lectura en voz alta para detectar frases truncadas.
- **Unificar formato de tablas:** Asegurar que todas las tablas sigan la misma estructura, sin columnas duplicadas ni celdas vacías innecesarias. Verificar que la numeración de casos de uso sea secuencial y única.
- **Validación cruzada:** Contrastar el contenido de la memoria técnica con los diagramas y matrices adjuntas para garantizar que no existan contradicciones ni elementos huérfanos.