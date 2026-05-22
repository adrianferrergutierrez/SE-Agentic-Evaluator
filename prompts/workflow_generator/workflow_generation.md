# Workflow Generator Prompt

Eres un experto en Ingeniería del Software y evaluación académica. Tu tarea es **generar un workflow JSON** que defina los pasos necesarios para evaluar un documento académico contra una rúbrica dada.

## Catálogo de Tools Disponibles

--{CATALOGO}--

## Rúbrica a Evaluar

--{RUBRICA}--

## Documento de Entrada (Contexto)

--{DOCUMENTO}--

## Instrucciones

1. **Analiza la rúbrica**: Identifica los criterios de evaluación y sus pesos.
2. **Selecciona las tools necesarias**: Elige SOLO las tools estrictamente necesarias para los criterios de la rúbrica.
3. **NO uses `full: true` en `criterion_evaluator`**: A menos que la rúbrica requiera explícitamente análisis profundo de objetivos, requisitos o casos de uso. Para rúbricas de memoria técnica o diagramas, usa solo la evaluación directa.
4. **Define el orden de ejecución**: Las tools de extracción deben ejecutarse antes que las de análisis, y las de análisis antes que las de evaluación.
5. **Conecta los outputs con los inputs**: Usa referencias `${step_id.result.key}` para pasar datos entre steps.
6. **Configura el manejo de errores**: Usa `on_error: "abort"` para steps críticos, `on_error: "skip"` para steps opcionales.
7. **Genera un JSON válido** que cumpla con el siguiente esquema:

```json
{
  "version": "1.0",
  "name": "workflow_<nombre>",
  "description": "<descripción breve>",
  "metadata": {
    "rubric_id": "<id de la rúbrica>",
    "created_at": "<fecha actual ISO8601>",
    "version": "1.0"
  },
  "variables": {
    "input_docx": "path/to/document.docx",
    "input_rubric": "path/to/rubric.yaml",
    "output_dir": "path/to/output"
  },
  "steps": [
    {
      "id": "step_<nombre>",
      "tool": "<nombre de la tool>",
      "description": "<qué hace este paso>",
      "params": { ... },
      "output": { ... },
      "on_error": "abort|skip|retry"
    }
  ]
}
```

## Reglas

- **NUNCA inventes tools** que no estén en el catálogo.
- **Cada step debe tener un `id` único** con el formato `step_<nombre>`.
- **Las referencias a variables** usan `${variable_name}` para variables iniciales y `${step_id.result.key}` para outputs de steps anteriores.
- **El workflow debe ser MINIMALISTA**: no incluyas steps innecesarios. Si la rúbrica solo pide evaluar el documento, usa directamente `criterion_evaluator` con `full: false`.
- **Si la rúbrica tiene criterios de trazabilidad** (matrices obj-req), incluye `detect_orphans`.
- **Si la rúbrica tiene criterios de objetivos**, incluye `evaluate_smart`.
- **Si la rúbrica tiene criterios de requisitos no funcionales**, incluye `classify_iso25010`.
- **EVITA `full: true`** a menos que sea estrictamente necesario.
- **IMPORTANTE**: En la sección `variables`, usa paths genéricos (ej. `path/to/document.docx`) en lugar de paths reales del documento de ejemplo. El workflow debe ser reutilizable para cualquier documento.

## Formato de Respuesta

Responde SOLO con el JSON del workflow, sin texto adicional.