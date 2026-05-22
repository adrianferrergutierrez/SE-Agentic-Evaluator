# Evaluación: Memoria técnica

## Análisis
**Estructura y extensión:** El documento cumple ampliamente con los requisitos mínimos de extensión (supera con holgura las 5 páginas) y contiene todos los apartados esperados en una memoria técnica de ingeniería del software: introducción, objetivos, técnicas y herramientas, descripción del equipo, aspectos relevantes, conclusiones, catálogo de requisitos (información, restricciones, funcionales, no funcionales, casos de uso, actores, matrices de trazabilidad, ética) y modelo de análisis (dominio, vistas de interacción, arquitectura, glosario). La organización es lógica y sigue un índice coherente.

**Redacción y ortografía:** Se detectan varios errores tipográficos, gramaticales y de estilo que afectan el rigor técnico esperado:
- Errores evidentes: `rastreabilidadbilidad` (debería ser *rastreabilidad*), `a el usuario` (debería ser *al usuario*), `que poder generar` (construcción sintáctica incorrecta).
- Inconsistencias en mayúsculas: `trello`, `telegram`, `google drive`, `visual paradigm` aparecen en minúscula cuando son nombres propios de herramientas.
- Tono informal en secciones que requieren objetividad técnica: `un trozo de pan`, `más o menos todos tuviéramos que trabajar`, `como nos gusta llamarla a nosotros`.
- Inconsistencias lógicas en casos de uso: CU-018 y CU-019 comparten exactamente la misma descripción; CU-020 se titula *Gestionar becas y ayudas* pero su descripción habla de *gestión de usuarios registrados*.

**Contenido técnico y coherencia:** El catálogo de requisitos está bien estructurado mediante tablas normalizadas (IRQ, CRQ, NFR, CU, ACT) y las matrices de trazabilidad (Objetivos-Requisitos y Requisitos-Requisitos) están correctamente referenciadas. El modelo de dominio y la propuesta de arquitectura en capas están descritos con claridad. No obstante, varias tablas de casos de uso presentan campos vacíos (`Rendimiento`, `Frecuencia`), y los diagramas se muestran únicamente como marcadores de imagen (`![Imagen X](img/...)`), lo cual es aceptable en un borrador pero debe resolverse en la versión final.

**Cumplimiento de la rúbrica:** El documento supera los criterios de extensión y estructura, pero la presencia de faltas ortográficas, expresiones informales y errores de coherencia en los casos de uso impiden alcanzar el nivel de "escrito correctamente" (7/10). Se sitúa en un nivel intermedio: cumple la base técnica y organizativa, pero requiere una revisión exhaustiva de forma y rigor.

## Puntuación
**Puntuación:** 5/10

## Observaciones
1. **Revisión ortotipográfica y de estilo:** Corregir errores como `rastreabilidadbilidad`, `a el`, y unificar la capitalización de herramientas (`Trello`, `Telegram`, `Google Drive`, `Visual Paradigm`). Eliminar coloquialismos y mantener un tono técnico y objetivo en toda la memoria.
2. **Corregir inconsistencias en casos de uso:** Revisar y diferenciar las descripciones de CU-018 y CU-019. Alinear el título y la descripción de CU-020. Completar los campos vacíos (`Rendimiento`, `Frecuencia`) o justificar su omisión.
3. **Integración de diagramas:** Asegurar que las imágenes de los diagramas (casos de uso, clases, arquitectura, vistas de interacción) se inserten correctamente en la versión final y no queden como placeholders.
4. **Validación de trazabilidad:** Verificar que todas las `X` en las matrices correspondan a relaciones reales y que no haya requisitos o casos de uso huérfanos.
5. **Formato de tablas:** Algunas tablas presentan columnas duplicadas o saltos de línea inconsistentes (probablemente por conversión a Markdown). Revisar el formato final para garantizar legibilidad y profesionalidad.