# Guía de Usuario: Evaluaitor-Lamb

## 1. Introducción

**Evaluaitor-Lamb** es un sistema de evaluación automática de entregables académicos basado en IA agéntica. El sistema utiliza un enfoque **meta-agéntico** para generar dinámicamente workflows de evaluación personalizados a partir de rúbricas arbitrarias.

Este documento explica cómo utilizar el sistema para generar workflows y ejecutar evaluaciones.

---

## 2. Instalación y Requisitos

### Requisitos
- **Python 3.11+**
- **DashScope API Key** (configurada en el archivo `.env` como `DASHSCOPE_API_KEY`)
- **Dependencias**: `python-docx`, `pandas`, `openpyxl`, `pydantic`, `jsonschema`, `requests`

### Instalación
```bash
pip install -r requirements.txt
```
*(O instala las dependencias manualmente según sea necesario)*

---

## 3. Uso del Sistema

El sistema se ejecuta mediante el script orquestador `run_evaluation.py`, que ofrece dos comandos principales: `generate` y `evaluate`.

### 3.1 Generar un Workflow

Este comando analiza una rúbrica y genera un archivo JSON que define los pasos necesarios para evaluar documentos según esa rúbrica. Este paso se realiza **una sola vez por rúbrica**.

```bash
python run_evaluation.py generate \
  --rubric configs/rubric_hito2.yaml \
  --sample-doc tests/test-1-hito-2/output/phase0_extract/contents.md \
  --output workflows/workflow_hito2.json
```

**Argumentos:**
- `--rubric`: Ruta al archivo YAML o Markdown de la rúbrica.
- `--sample-doc`: (Opcional) Ruta a un documento de ejemplo para dar contexto al generador.
- `--output`: Ruta donde se guardará el archivo `workflow.json` generado.
- `--model`: (Opcional) Modelo LLM a usar (por defecto: `qwen3.6-plus`).

**Salida:**
Genera un archivo JSON estructurado con metadatos, variables genéricas y pasos definidos.

### 3.2 Ejecutar una Evaluación

Este comando toma un workflow generado previamente y lo ejecuta contra un documento específico. Puedes reutilizar el **mismo workflow** para múltiples documentos.

```bash
python run_evaluation.py evaluate \
  --workflow workflows/workflow_hito2.json \
  --input entregas/alumno_01.docx \
  --output resultados/alumno_01/
```

**Argumentos:**
- `--workflow`: Ruta al archivo `workflow.json` generado.
- `--input`: Ruta al documento (DOCX) que deseas evaluar.
- `--output`: Directorio donde se guardarán los resultados (informe, logs, notas).
- `--dry-run`: (Opcional) Simula la ejecución sin llamar a las herramientas ni a la API.

**Salida:**
En el directorio de salida encontrarás:
- `evaluacion_final.md`: Informe completo de la evaluación.
- `scores.json`: Puntuaciones detalladas.
- `execution_log.json`: Log técnico de la ejecución del workflow.

---

## 4. Estructura de un Workflow

Un workflow generado tiene la siguiente estructura básica:

```json
{
  "version": "1.0",
  "name": "workflow_hito2",
  "description": "...",
  "metadata": {
    "rubric_id": "hito2",
    "created_at": "2026-05-22T...",
    "version": "1.0"
  },
  "variables": {
    "input_docx": "path/to/document.docx",
    "input_rubric": "path/to/rubric.yaml",
    "output_dir": "path/to/output"
  },
  "steps": [
    {
      "id": "step_extract_docx",
      "tool": "docx_extract",
      "params": { "input": "${variables.input_docx}", ... },
      "on_error": "abort"
    },
    ...
  ]
}
```

- **Variables**: El generador usa paths genéricos. Al ejecutar, el sistema inyecta los paths reales (`--input`, `--output`).
- **Steps**: Cada paso define qué herramienta usar, sus parámetros y cómo manejar errores.

---

## 5. Catálogo de Herramientas Disponibles

El sistema dispone de las siguientes herramientas que el agente puede incluir en un workflow:

| Categoría | Herramienta | Descripción |
|-----------|-------------|-------------|
| **Extract** | `docx_extract` | Convierte DOCX a Markdown + imágenes |
| | `xlsx_to_markdown` | Convierte rúbricas Excel a Markdown |
| | `extract_objectives` | Extrae objetivos (OBJ-X) |
| | `extract_requirements` | Extrae requisitos (IRQ/NFR) |
| | `extract_use_cases` | Extrae casos de uso (CU-XXX) |
| **Analyze** | `detect_orphans` | Detecta requisitos sin vincular |
| | `evaluate_smart` | Análisis SMART de objetivos |
| | `classify_iso25010` | Clasificación ISO 25010 de NFR |
| **Evaluate** | `criterion_evaluator` | Evalúa criterios de rúbrica (LLM) |
| **Grade** | `grader` | Calcula nota ponderada |
| **Report** | `report_generator` | Genera informe final |
| **Config** | `rubric_importer` | Importa rúbrica a YAML |

---

## 6. Solución de Problemas

- **Error "Missing variables"**: Asegúrate de que el workflow define las variables necesarias (`input_docx`, `output_dir`, etc.) o que no se han eliminado accidentalmente del JSON.
- **Error de API Key**: Verifica que el archivo `.env` existe en la raíz del proyecto y contiene `DASHSCOPE_API_KEY=sk-...`.
- **Workflow inválido**: Si el generador falla tras 3 intentos, revisa que la rúbrica tenga un formato de tabla Markdown correcto o un YAML válido.

---

*Para más detalles técnicos, consulta `docs/project-overview.md`.*
