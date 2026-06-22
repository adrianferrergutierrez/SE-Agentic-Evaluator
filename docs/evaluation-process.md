# Proceso de Evaluación Meta-Agéntica - Documentación Detallada

## 1. Visión General del Sistema

El sistema Evaluaitor-Lamb ha evolucionado de un pipeline fijo a un sistema **meta-agéntico** capaz de generar y ejecutar workflows dinámicos personalizados para cualquier rúbrica.

### Arquitectura del Proceso

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USUARIO (CLI)                                 │
│  Input: documento.docx + rubrica.xlsx                                   │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    PIPELINE DE EVALUACIÓN                               │
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────────┐  │
│  │ FASE 0      │─▶│ FASE 1      │─▶│ FASE 2      │─▶│ FASE 3        │  │
│  │ Extracción  │  │ Importación │  │ Generación  │  │ Ejecución     │  │
│  │ DOCX/XLSX   │  │ Rúbrica     │  │ Workflow    │  │ Workflow      │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └───────────────┘  │
│         │                │                │                  │          │
│         ▼                ▼                ▼                  ▼          │
│   contents.md       rubric.yaml    workflow.json    evaluacion_final.md │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Fase 0: Extracción de Documentos

### Objetivo
Convertir los archivos binarios de entrada (DOCX, XLSX) a formatos procesables (Markdown).

### Herramientas Utilizadas

| Herramienta | Archivo | Descripción |
|-------------|---------|-------------|
| `docx_extract` | `core/extraction/docx_extract.py` | Extrae texto, tablas e imágenes del DOCX |
| `xlsx_to_markdown` | `core/extraction/xlsx_to_markdown.py` | Convierte la rúbrica Excel a Markdown |

### Proceso Detallado

#### 2.1 Conversión DOCX → Markdown

```python
# core/extraction/docx_extract.py
def extract_docx(input: str, output_dir: str) -> Dict[str, Any]:
    # 1. Leer documento con python-docx
    doc = docx.Document(input_path)
    
    # 2. Procesar párrafos preservando estilos
    for para in doc.paragraphs:
        style = para.style.name
        if 'Title' in style: lines.append(f'# {text}')
        elif 'Heading 1' in style: lines.append(f'## {text}')
        # ... etc
    
    # 3. Extraer tablas como Markdown
    for table in doc.tables:
        # Convertir a formato | col1 | col2 |
    
    # 4. Extraer imágenes como archivos independientes
    for rel in doc.part.rels.values():
        if 'image' in rel.reltype:
            # Guardar blob a img/img_X.ext
            # Añadir referencia ![Imagen X](img/img_X.ext)
    
    # 5. Guardar contents.md
    return {"contents_md": str(md_path), "images": img_count}
```

**Output:** `tests/test-1-hito-2/output/phase0_extract/contents.md` (95,791 chars, 26 imágenes)

#### 2.2 Conversión XLSX → Markdown

```python
# core/extraction/xlsx_to_markdown.py
def xlsx_to_markdown(input: str, output: str) -> Dict[str, Any]:
    # 1. Leer Excel con pandas
    df = pd.read_excel(input_path, header=None)
    
    # 2. Detectar fila de encabezado (busca "(0)", "(10)", etc.)
    for i, row in df.iterrows():
        if re.search(r"\(\d+\)", str(row)):
            header_idx = i
            break
    
    # 3. Convertir a Markdown
    md_content = table_df.to_markdown(index=False)
    
    return {"markdown_path": str(output_path)}
```

**Output:** `tests/test-1-hito-2/rubrica_hito2.md`

---

## 3. Fase 1: Importación de Rúbrica

### Objetivo
Convertir la rúbrica Markdown a configuración YAML y prompts individuales.

### Herramientas Utilizadas

| Herramienta | Archivo | Descripción |
|-------------|---------|-------------|
| `rubric_importer` | `core/config/rubric_importer.py` | Parsea tabla Markdown y genera YAML + prompts |

### Proceso Detallado

```python
# core/config/rubric_importer.py
def import_rubric(input_path, output_yaml, prompts_dir):
    # 1. Parsear tabla Markdown
    criteria = parse_markdown_rubric(md_content)
    # Detecta columnas: Criterio | Nivel 0 | Nivel 2 | ... | Peso
    
    # 2. Generar prompts individuales
    for criterion in criteria:
        prompt = generate_prompt(criterion)
        # Crea prompts/hito2/hito2_memoria_tecnica.md
        # Crea prompts/hito2/hito2_diagrama_de_clases...
    
    # 3. Generar YAML config
    yaml_content = generate_yaml(criteria, rubric_id)
    # Crea configs/rubric_hito2.yaml
    
    return config_path
```

**Output:**
- `configs/rubric_hito2.yaml` (configuración con 3 criterios)
- `prompts/hito2/` (3 prompts individuales)

---

## 4. Fase 2: Generación del Workflow (Meta-Agent)

### Objetivo
Analizar la rúbrica y generar dinámicamente un workflow JSON personalizado.

### Herramientas Utilizadas

| Herramienta | Archivo | Descripción |
|-------------|---------|-------------|
| `workflow_generator` | `core/meta_agent/workflow_generator.py` | Genera workflow JSON usando LLM |
| `tool_catalog` | `core/meta_agent/tool_catalog.py` | Proporciona catálogo de tools al LLM |
| `workflow_schema` | `schemas/workflow_schema.json` | Valida el workflow generado |
| `workflow_generation.md` | `prompts/workflow_generator/workflow_generation.md` | Prompt para el generador |

### Proceso Detallado

#### 4.1 Construcción del Prompt

```python
# core/meta_agent/workflow_generator.py
def build_prompt(rubric_text, document_text, catalog_text):
    template = _load_prompt(PROMPT_PATH)  # workflow_generation.md
    return (
        template
        .replace("--{CATALOGO}--", catalog_text)
        .replace("--{RUBRICA}--", rubric_text)
        .replace("--{DOCUMENTO}--", document_text[:5000])
    )
```

El prompt incluye:
1. **Catálogo de Tools**: Lista de 13 tools disponibles con sus parámetros y outputs
2. **Rúbrica**: Los 3 criterios de Hito 2 (Memoria técnica, Diagrama, Glosario)
3. **Documento**: Primeros 5000 chars del contenido para contexto
4. **Instrucciones**: Reglas estrictas para minimalismo (NO usar `full: true` innecesariamente)

#### 4.2 Generación y Validación

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW GENERATOR                           │
│                                                                 │
│  Input:                                                         │
│  - Catálogo de 13 tools                                         │
│  - Rúbrica Hito 2 (3 criterios)                                 │
│  - Documento (95k chars)                                        │
│                                                                 │
│  LLM (qwen3.6-plus):                                            │
│  1. Analiza criterios de rúbrica                                │
│  2. Selecciona tools necesarias                                 │
│  3. Define orden y conexiones                                   │
│  4. Genera JSON                                                 │
│                                                                 │
│  Validación:                                                    │
│  - jsonschema.validate(workflow, workflow_schema.json)          │
│  - Si falla: reintentar con feedback de errores (max 3)         │
│                                                                 │
│  Output: workflow_eval_hito2.json                               │
└─────────────────────────────────────────────────────────────────┘
```

**Workflow Generado:**

```json
{
  "name": "workflow_eval_hito2",
  "steps": [
    {"id": "step_extract_doc", "tool": "docx_extract"},
    {"id": "step_evaluate", "tool": "criterion_evaluator", "full": false},
    {"id": "step_grade", "tool": "grader"},
    {"id": "step_report", "tool": "report_generator"}
  ]
}
```

**Nota clave:** El generador decidió NO usar `full: true`, evitando extracciones innecesarias de objetivos/requisitos para esta rúbrica.

---

## 5. Fase 3: Ejecución del Workflow

### Objetivo
Ejecutar el workflow generado paso a paso, conectando herramientas y pasando datos.

### Herramientas Utilizadas

| Herramienta | Archivo | Descripción |
|-------------|---------|-------------|
| `workflow_executor` | `core/workflow_executor.py` | Ejecuta workflows JSON |
| `tool_registry` | `core/tool_registry.py` | Registro centralizado de 13 tools |

### Proceso Detallado

#### 5.1 Tool Registry

El `ToolRegistry` es el corazón de la ejecución. Proporciona una interfaz uniforme para todas las tools:

```python
# core/tool_registry.py
class Tool(ABC):
    @property
    @abstractmethod
    def name(self) -> str: pass
    
    @property
    @abstractmethod
    def description(self) -> str: pass
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]: pass

# 13 tools registradas:
# - DocxExtractTool, XlsxToMarkdownTool, RubricImporterTool
# - ExtractObjectivesTool, ExtractRequirementsTool, ExtractUseCasesTool
# - DetectOrphansTool, EvaluateSmartTool, ClassifyIso25010Tool
# - BuildContextTool, CriterionEvaluatorTool, GraderTool, ReportGeneratorTool
```

#### 5.2 Ejecución Paso a Paso

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW EXECUTOR                            │
│                                                                 │
│  Variables iniciales:                                           │
│  - input_docx: tests/test-1-hito-2/A1.1 Memoria...docx         │
│  - input_rubric: configs/rubric_hito2.yaml                      │
│  - output_dir: tests/test-1-hito-2/output                       │
│                                                                 │
│  Step 1: step_extract_doc (docx_extract)                        │
│  ├── Params: input=${input_docx}, output_dir=${output_dir}      │
│  ├── Ejecuta: registry.execute("docx_extract", ...)             │
│  └── Result: contents_md=".../contents.md", images=26           │
│                                                                 │
│  Step 2: step_evaluate (criterion_evaluator)                    │
│  ├── Params: document=${step_extract_doc.result.contents_md}    │
│  │         config=${input_rubric}, full=false                   │
│  ├── Ejecuta: run_criterion_evaluation(...)                     │
│  │   ├── Carga config: hito2 (3 criterios)                      │
│  │   ├── Evalúa: Memoria técnica → 7.0/10                       │
│  │   ├── Evalúa: Diagrama de clases → 2.0/10                    │
│  │   └── Evalúa: Glosario de clases → 7.0/10                    │
│  └── Result: scores={...}, output_dir=".../eval"                │
│                                                                 │
│  Step 3: step_grade (grader)                                    │
│  ├── Params: scores=${step_evaluate.result.scores}              │
│  │         config=${input_rubric}                               │
│  ├── Ejecuta: RubricGrader.grade(...)                           │
│  └── Result: weighted_final=3.75, mean_xbar=5.33                │
│                                                                 │
│  Step 4: step_report (report_generator)                         │
│  ├── Params: document=..., eval_dir=..., config=..., scores=... │
│  ├── Ejecuta: run_report_generation(...)                        │
│  └── Result: report_path=".../evaluacion_final.md"              │
│                                                                 │
│  Estado: completed (4/4 steps)                                  │
│  Duración: 323.1s                                               │
└─────────────────────────────────────────────────────────────────┘
```

#### 5.3 Resolución de Variables

El executor resuelve referencias como `${step_id.result.key}`:

```python
def _resolve_variables(self, value):
    # ${input_docx} → "tests/test-1-hito-2/A1.1 Memoria...docx"
    # ${step_extract_doc.result.contents_md} → "tests/.../contents.md"
    # ${step_evaluate.result.scores} → {"memoria_tecnica": 7.0, ...}
```

---

## 6. Fase 4: Generación del Informe Final

### Objetivo
Sintetizar todas las evaluaciones en un informe consolidado.

### Herramientas Utilizadas

| Herramienta | Archivo | Descripción |
|-------------|---------|-------------|
| `report_generator` | `core/evaluation/evaluator.py` | Genera informe final con LLM |
| `4_1_generacion_informe.md` | `prompts/4_1_generacion_informe.md` | Prompt para generación de informe |

### Proceso Detallado

```python
# core/evaluation/evaluator.py
def run_report_generation(document_path, eval_dir, config_path, scores_path, output_dir):
    # 1. Cargar evaluaciones individuales (eval_*.md)
    evaluations = load_evaluations_from_dir(eval_dir)
    
    # 2. Calcular nota ponderada con RubricGrader
    grader = RubricGrader.from_config(config_path)
    grading_result = grader.grade({}, scores=scores)
    
    # 3. Generar informe con LLM
    prompt = load_prompt("4_1_generacion_informe.md")
    prompt = prompt.replace("--{DOCUMENTO}--", document)
    prompt = prompt.replace("--{EVALUACIONES}--", evals_summary)
    prompt = prompt.replace("--{NOTA_FINAL}--", f"{grading_result.weighted_final}/10")
    
    final_report = client.generate(model="qwen3.6-plus", prompt=prompt)
    
    # 4. Guardar informe
    report_file.write_text(final_report)
```

**Output:** `tests/test-1-hito-2/output/evaluacion_final.md`

---

## 7. Resumen de Archivos Utilizados

### Tools (core/)

| Archivo | Función |
|---------|---------|
| `core/extraction/docx_extract.py` | Extracción DOCX → Markdown |
| `core/extraction/xlsx_to_markdown.py` | Conversión Excel → Markdown |
| `core/config/rubric_importer.py` | Importación de rúbrica |
| `core/meta_agent/workflow_generator.py` | Generación de workflow |
| `core/meta_agent/tool_catalog.py` | Catálogo de tools |
| `core/workflow_executor.py` | Ejecución de workflow |
| `core/tool_registry.py` | Registro de tools |
| `core/evaluation/criterion_evaluator.py` | Evaluación de criterios |
| `core/evaluation/evaluator.py` | Generación de informe |
| `core/grading/grader.py` | Cálculo de nota |
| `core/clients/dashscope_client.py` | Cliente API DashScope |

### Prompts (prompts/)

| Archivo | Función |
|---------|---------|
| `prompts/workflow_generator/workflow_generation.md` | Prompt para generar workflow |
| `prompts/hito2/hito2_memoria_tecnica.md` | Prompt criterio Memoria técnica |
| `prompts/hito2/hito2_diagrama_de_clases_del_modelo_de_dominio.md` | Prompt criterio Diagrama |
| `prompts/hito2/hito2_glosario_de_clases.md` | Prompt criterio Glosario |

### Esquemas (schemas/)

| Archivo | Función |
|---------|---------|
| `schemas/workflow_schema.json` | JSON Schema para validar workflows |

### Configuración (configs/)

| Archivo | Función |
|---------|---------|
| `configs/rubric_hito2.yaml` | Configuración de rúbrica Hito 2 |

### Skills (.opencode/skills/)

| Archivo | Función |
|---------|---------|
| `docx_extract_skill.md` | Skill para extracción DOCX |
| `evaluator_skill.md` | Skill para evaluación |
| `analyze_skill.md` | Skill para análisis |
| `grade_skill.md` | Skill para cálculo de notas |
| `report_skill.md` | Skill para generación de informes |
| `extract_skill.md` | Skill para extracción semántica |

---

## 8. Resultados Finales

| Métrica | Valor |
|---------|-------|
| **Nota Ponderada** | 3.75/10 |
| **Media Aritmética** | 5.33/10 |
| **Nivel** | Insuficiente |
| **Steps Ejecutados** | 4/4 |
| **Duración Total** | 323.1s |
| **Tokens Consumidos** | ~180,000 input + ~20,000 output |

### Puntuaciones por Criterio

| Criterio | Peso | Puntuación | Nota Ponderada |
|----------|------|------------|----------------|
| Memoria técnica | 25% | 7.0/10 | 1.75 |
| Diagrama de clases del modelo de dominio | 65% | 2.0/10 | 1.30 |
| Glosario de clases | 10% | 7.0/10 | 0.70 |
| **TOTAL** | **100%** | | **3.75/10** |

---

## 9. Comparativa con Pipeline Fijo

| Aspecto | Pipeline Fijo | Meta-Agent |
|---------|---------------|------------|
| **Flexibilidad** | Fijo, siempre igual | Dinámico, adaptado a rúbrica |
| **Extracciones** | Siempre todas (`--full`) | Solo las necesarias |
| **Tiempo** | ~600s (con full) | ~323s (sin full) |
| **Tokens** | ~250,000+ | ~180,000 |
| **Adaptabilidad** | Ninguna | Alta |
| **Mantenimiento** | Modificar código | Actualizar prompt/schema |

---

*Documento generado como parte del proceso de evaluación del Hito 2 - Evaluaitor-Lamb*
