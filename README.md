# SE-Agentic-Evaluator

Asistente agéntico para evaluación asistida por IA generativa, diseñado para
**complementar** el juicio docente, **no sustituirlo**.

> ⚠️ **Nota ética y de uso**  
> Este sistema debe emplearse exclusivamente como herramienta de apoyo.
> La calificación final y todas las decisiones académicas deben permanecer
> bajo responsabilidad del profesorado.

---

## Propósito

Transforma el pipeline rígido de investigación del proyecto
[SE-rubric-evaluAItor](https://github.com/Lamb-Project/SE-rubric-evaluAItor)
en una **Skill agéntica** para la plataforma **opencode.ai**, permitiendo:

- **Selección dinámica de herramientas** según el contenido (texto, PDFs, diagramas UML).
- **Visión multimodal local**: integra la lógica de
  [DiagramLens](https://github.com/Lamb-Project/DiagramLens) para categorizar
  y describir diagramas técnicos sin enviar datos a servicios externos.
- **Privacidad RGPD**: todos los modelos de IA se ejecutan localmente vía
  [Ollama](https://ollama.com).
- **Trazabilidad**: cada afirmación evaluativa debe poder vincularse a
  evidencia textual o visual del documento.
- **Cálculo determinístico**: la nota final se calcula mediante un script
  Python, nunca por el propio LLM, evitando errores de alucinación.

---

## Estructura del repositorio

```
SE-Agentic-Evaluator/
├── .opencode/
│   └── skills/
│       └── evaluator_skill.md      # Definición de la Skill para opencode.ai
├── core/
│   ├── extraction/
│   │   ├── objectives.py            # Tool: extraer OBJ-X
│   │   ├── requirements.py          # Tool: extraer IRQ/NFR
│   │   ├── use_cases.py             # Tool: extraer CU-XXX
│   │   └── diagramlens/             # Módulo de visión (de DiagramLens)
│   │       ├── annotate.py          # Lógica importable de descripción de diagramas
│   │       └── image_categories_enhanced.json
│   ├── analysis/
│   │   ├── traceability.py          # Tool: análisis de trazabilidad OBJ<->IRQ
│   │   ├── completeness.py          # Tool: análisis de completitud de requisitos
│   │   ├── orphans.py               # Tool determinística: detección de huérfanos
│   │   ├── smart.py                 # Helper: evaluación SMART de objetivos
│   │   └── iso25010.py              # Helper: clasificación ISO/IEC 25010 de NFR
│   └── grading/
│       └── grader.py                # Script determinístico de calificación final
├── prompts/                          # Prompts reales de SE-rubric-evaluAItor (GPL-3.0)
│   ├── 1_1_extraccion_objetivos.md
│   ├── 1_2_extraccion_requisitos.md
│   ├── 1_3_extraccion_casos_de_uso.md
│   ├── 2_1_analisis_trazabilidad.md
│   ├── 2_2_analisis_completitud.md
│   ├── 3_1_evaluacion_objetivos.md
│   ├── 3_2_evaluacion_requisitos_info.md
│   ├── 3_3_evaluacion_requisitos_nf.md
│   ├── 3_4_evaluacion_caso_uso.md
│   ├── 3_5_evaluacion_matrices.md
│   └── 4_1_generacion_informe.md
├── docs/
│   └── TECHNICAL_NOTES.md
├── requirements.txt
└── README.md
```

---

## Dependencias

```bash
pip install -r requirements.txt
```

Requiere **Ollama** ejecutándose localmente con los modelos necesarios:

```bash
# Modelo de texto (extracción y análisis)
ollama pull qwen3

# Modelo de visión (descripción de diagramas)
ollama pull qwen3-vl
```

---

## Uso rápido

### 1. Extracción

```python
from core.extraction.objectives import extract_objectives
from core.extraction.requirements import extract_requirements, parse_objective_associations

doc = open("entregable.md").read()
objectives_md = extract_objectives(doc)
requirements_md = extract_requirements(doc)
```

### 2. Detección de huérfanos (determinístico)

```python
from core.analysis.orphans import detect_orphans

report = detect_orphans(objectives_md, requirements_md)
print(report.as_markdown())
```

### 3. Evaluación SMART e ISO 25010 (determinística)

```python
from core.analysis.smart import evaluate_objectives_smart, smart_summary_markdown
from core.analysis.iso25010 import classify_requirements_iso25010

smart_scores = evaluate_objectives_smart(objectives_md)
print(smart_summary_markdown(smart_scores))

iso_report = classify_requirements_iso25010(requirements_md)
print(iso_report.as_markdown())
```

### 4. Descripción de diagramas (requiere Ollama + modelo de visión)

```python
from core.extraction.diagramlens import process_markdown_document
from pathlib import Path

results = process_markdown_document(
    input_md=Path("entregable.md"),
    output_annotated=Path("entregable_anotado.md"),
    output_summary=Path("resumen_diagramas.md"),
)
```

### 5. Calificación final (determinístico)

```bash
python core/grading/grader.py \
  --scores 7.5 8.0 6.0 7.0 8.5
# Output: {"mean_xbar": 7.4}

python core/grading/grader.py \
  --criteria-json criteria.json
# Output: {"weighted_final": 7.43}
```

---

## Créditos y licencias

Este proyecto integra código de:

- **[SE-rubric-evaluAItor](https://github.com/Lamb-Project/SE-rubric-evaluAItor)**
  (Lamb-Project) – prompts, lógica de parsing y generación de reportes.
  Licencia: GNU GPL v3.0.

- **[DiagramLens](https://github.com/Lamb-Project/DiagramLens)**
  (Lamb-Project) – lógica de descripción de diagramas vía modelos de visión.
  Licencia: GNU GPL v3.0.

El código de SE-Agentic-Evaluator que integra estos recursos también se
distribuye bajo **GNU GPL v3.0** (ver `LICENSE`).
