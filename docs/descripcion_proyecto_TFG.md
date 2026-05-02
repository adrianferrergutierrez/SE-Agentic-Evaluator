# SE-Agentic-Evaluator: Sistema de Evaluación Asistida por IA Agéntica para Ingeniería de Software

## Descripción del Proyecto

**SE-Agentic-Evaluator** es un asistente agéntico diseñado para la evaluación asistida por inteligencia artificial generativa de entregables académicos de Ingeniería de Software. El sistema ha sido concebido como una **herramienta de apoyo al juicio docente**, nunca como un sustituto, manteniendo la responsabilidad final de la calificación exclusivamente en el profesorado.

El proyecto representa la evolución del pipeline de investigación [SE-rubric-evaluAItor](https://github.com/Lamb-Project/SE-rubric-evaluAItor), transformando su arquitectura rígida en una **Skill agéntica** para la plataforma **opencode.ai**, lo que permite una ejecución dinámica, contextual y adaptativa del proceso de evaluación.

---

## Objetivos Principales

1. **Automatización asistida del proceso de evaluación**: Implementar un pipeline de evaluación que combina modelos de lenguaje grandes (LLMs) con lógica determinística para analizar documentos de requisitos, especificaciones técnicas y diagramas UML.

2. **Privacidad por diseño**: Garantizar el cumplimiento del Reglamento General de Protección de Datos (RGPD) mediante la ejecución local de todos los modelos de IA a través de [Ollama](https://ollama.com), evitando la exfiltración de documentos académicos a servicios externos.

3. **Visión multimodal local**: Integrar la lógica de [DiagramLens](https://github.com/Lamb-Project/DiagramLens) para la categorización y descripción técnica automática de diagramas mediante modelos de visión locales (`qwen3-vl`), sin dependencia de APIs externas.

4. **Trazabilidad completa**: Vincular cada afirmación evaluativa a evidencia textual o visual explícita del documento analizado, garantizando transparencia y auditabilidad del proceso.

5. **Cálculo determinístico de calificaciones**: Delegar toda agregación numérica en scripts Python dedicados, eliminando el riesgo de alucinaciones numéricas inherentes a los LLMs.

---

## Arquitectura del Sistema

El sistema se organiza en tres módulos principales:

### Módulo de Extracción (`core/extraction/`)

| Módulo | Descripción |
|--------|-------------|
| `objectives.py` | Extracción estructurada de objetivos del proyecto (OBJ-X) mediante prompts especializados. |
| `requirements.py` | Identificación y clasificación de requisitos funcionales (IRQ) y no funcionales (NFR). |
| `use_cases.py` | Extracción de casos de uso (CU-XXX) con sus componentes (actor, precondiciones, flujo). |
| `diagramlens/` | Módulo de visión multimodal que categoriza y describe técnicamente diagramas UML y figuras técnicas embebidas en documentos Markdown. |

### Módulo de Análisis (`core/analysis/`)

| Módulo | Descripción |
|--------|-------------|
| `traceability.py` | Generación de matrices de trazabilidad entre objetivos y requisitos (OBJ ↔ IRQ/NFR). |
| `completeness.py` | Evaluación de la completitud de los requisitos identificados. |
| `orphans.py` | Detección determinística de requisitos huérfanos (sin objetivo asociado) y objetivos sin cobertura de requisitos. |
| `smart.py` | Evaluación heurística de objetivos contra los criterios SMART (Specific, Measurable, Achievable, Relevant, Time-bound) mediante análisis de patrones regex, sin dependencia de LLM. |
| `iso25010.py` | Clasificación automática de requisitos no funcionales según las 8 características de calidad del estándar ISO/IEC 25010. |

### Módulo de Calificación (`core/grading/`)

| Módulo | Descripción |
|--------|-------------|
| `grader.py` | Script determinístico que calcula la nota final ponderada y la media aritmética (x̄) a partir de las puntuaciones parciales por criterio, con pesos configurables. |

**Pesos por defecto de la rúbrica:**

| Criterio | Peso |
|----------|------|
| Objetivos | 20% |
| Requisitos de Información | 15% |
| Requisitos No Funcionales | 10% |
| Casos de Uso | 35% |
| Matrices de Trazabilidad | 20% |

---

## Flujo de Ejecución

El sistema opera mediante una **Skill agéntica** (`evaluator_skill`) que define el rol, las herramientas disponibles y las reglas de proceso:

1. **Extracción**: Identificación estructurada de objetivos, requisitos, casos de uso y diagramas del documento entregable.

2. **Análisis**: Evaluación de trazabilidad, completitud, detección de huérfanos, criterios SMART e ISO 25010.

3. **Evaluación por criterio**: Aplicación de prompts de evaluación específicos (`prompts/3_1` a `3_5`) con evidencia obligatoria.

4. **Calificación determinística**: Cálculo de la nota final mediante `grader.py`, evitando alucinaciones numéricas.

5. **Generación de informe**: Producción de un informe Markdown con tabla de rúbrica, resumen ejecutivo, análisis por criterio, detección de huérfanos, evaluación SMART/ISO 25010 y recomendaciones accionables priorizadas.

---

## Principios de Diseño

- **Complementariedad**: El sistema complementa el juicio docente; la calificación final permanece bajo responsabilidad exclusiva del profesorado.

- **Evidencia obligatoria**: Todo juicio evaluativo debe acompañarse de cita textual, descripción de diagrama o ID de elemento referenciado.

- **Minimización de alucinaciones**: Los cálculos numéricos se delegan exclusivamente en código determinístico.

- **Selección dinámica de herramientas**: El agente decide qué herramientas invocar según el contenido detectado, sin un orden fijo predefinido.

- **Visión multimodal obligatoria**: Ante la detección de diagramas, se invoca automáticamente el módulo de visión antes de evaluar consistencia arquitectónica.

---

## Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| Plataforma agéntica | opencode.ai |
| Modelos de IA locales | Ollama (qwen3, qwen3-vl) |
| Lenguaje principal | Python 3 |
| Procesamiento de imágenes | Pillow |
| Procesamiento de PDFs | PyMuPDF |
| OCR (fallback) | pytesseract |
| Validación de datos | Pydantic |
| Cálculo numérico | NumPy |
| Salida en terminal | Rich |

---

## Estructura del Repositorio

```
SE-Agentic-Evaluator/
├── .opencode/
│   └── skills/
│       ├── evaluator_skill.md          # Definición de la Skill para opencode.ai
│       └── tfg_documentation_skill.md  # Skill de documentación del TFG
├── core/
│   ├── extraction/
│   │   ├── objectives.py               # Tool: extraer OBJ-X
│   │   ├── requirements.py             # Tool: extraer IRQ/NFR
│   │   ├── use_cases.py                # Tool: extraer CU-XXX
│   │   └── diagramlens/                # Módulo de visión (de DiagramLens)
│   │       ├── annotate.py             # Lógica importable de descripción de diagramas
│   │       └── image_categories_enhanced.json
│   ├── analysis/
│   │   ├── traceability.py             # Tool: análisis de trazabilidad OBJ ↔ IRQ
│   │   ├── completeness.py             # Tool: análisis de completitud de requisitos
│   │   ├── orphans.py                  # Tool determinística: detección de huérfanos
│   │   ├── smart.py                    # Helper: evaluación SMART de objetivos
│   │   └── iso25010.py                 # Helper: clasificación ISO/IEC 25010 de NFR
│   └── grading/
│       └── grader.py                   # Script determinístico de calificación final
├── prompts/                            # Prompts de SE-rubric-evaluAItor (GPL-3.0)
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
├── tests/                              # Casos de prueba y evaluaciones de ejemplo
├── docs/
│   ├── TFG_diario_desarrollo.md        # Diario de desarrollo del TFG
│   └── TECHNICAL_NOTES.md              # Notas técnicas del proyecto
├── requirements.txt
└── README.md
```

---

## Herramientas del Sistema Agéntico

| # | Nombre | Módulo | Descripción |
|---|--------|--------|-------------|
| 1 | **ExtractObjectives** | `core/extraction/objectives.py` | Extrae objetivos (OBJ-X) usando el prompt `1_1_extraccion_objetivos.md` |
| 2 | **ExtractRequirements** | `core/extraction/requirements.py` | Extrae IRQ y NFR usando el prompt `1_2_extraccion_requisitos.md` |
| 3 | **ExtractUseCases** | `core/extraction/use_cases.py` | Extrae casos de uso (CU-XXX) usando el prompt `1_3_extraccion_casos_de_uso.md` |
| 4 | **VisionDescriber** | `core/extraction/diagramlens/` | Categoriza y describe técnicamente cada diagrama usando un modelo de visión local (`qwen3-vl`) vía Ollama |
| 5 | **AnalyzeTraceability** | `core/analysis/traceability.py` | Genera la matriz de trazabilidad OBJ ↔ IRQ/NFR usando `2_1_analisis_trazabilidad.md` |
| 6 | **AnalyzeCompleteness** | `core/analysis/completeness.py` | Evalúa completitud de requisitos usando `2_2_analisis_completitud.md` |
| 7 | **DetectOrphans** | `core/analysis/orphans.py` | **Determinístico.** Detecta requisitos huérfanos (sin objetivo) y objetivos sin requisitos |
| 8 | **CheckSMART** | `core/analysis/smart.py` | Evalúa objetivos contra los 5 criterios SMART (heurístico, sin LLM) |
| 9 | **ClassifyISO25010** | `core/analysis/iso25010.py` | Clasifica NFR según las 8 características de ISO/IEC 25010 (heurístico) |
| 10 | **DeterministicGrader** | `core/grading/grader.py` | **Determinístico.** Recibe puntuaciones parciales y pesos; devuelve nota ponderada y media x̄ en JSON |

---

## Reglas de Proceso del Agente

### R1 — No orden fijo
El agente decide dinámicamente qué herramienta invocar según el contenido detectado. El flujo típico es: Extracción → Análisis → Evaluación → Grading → Síntesis, pero cualquier orden es válido si el contenido lo requiere.

### R2 — Visión multimodal obligatoria ante diagramas
Si **ExtractUseCases** reporta diagramas detectados, o si el texto de extracción cita figuras, se invoca **VisionDescriber** antes de evaluar la consistencia arquitectónica. La descripción técnica del diagrama debe incluirse como evidencia en el informe.

### R3 — Detección de huérfanos antes de calificar
Antes de emitir cualquier puntuación se ejecuta **DetectOrphans**. Si existen requisitos huérfanos, se mencionan con sus IDs. Si existen objetivos sin requisitos, se indica el riesgo de falta de cobertura. Solo después continúa con las evaluaciones por criterio.

### R4 — SMART e ISO/IEC 25010 siempre
Se invoca **CheckSMART** sobre los objetivos extraídos y **ClassifyISO25010** sobre los NFR extraídos. Los hallazgos se incluyen en las evaluaciones correspondientes.

### R5 — Cálculo determinístico de la nota final
Nunca se calcula la nota final directamente. Una vez obtenidas todas las puntuaciones parciales (0–10), se llama a **DeterministicGrader**, que devuelve `{"weighted_final": X.XX, "mean_xbar": Y.YYYY}`.

### R6 — Evidencia obligatoria
Todo juicio evaluativo debe ir acompañado de al menos una de:
- **Cita textual**: extracto del documento con página/sección de origen.
- **Descripción de diagrama**: texto generado por **VisionDescriber**.
- **ID de elemento**: referencia explícita a OBJ-X, IRQ-Y, CU-ZZZ.

### R7 — Formato del informe final
El informe generado incluye:
1. Tabla de rúbrica con puntuaciones y nota ponderada.
2. Resumen ejecutivo con nivel de desempeño.
3. Análisis por criterio con evidencias.
4. Detección de requisitos huérfanos y evaluación SMART/ISO 25010.
5. Recomendaciones accionables priorizadas.
6. Pie de página: *"Este informe es una herramienta de apoyo. La calificación final es responsabilidad exclusiva del profesorado."*

---

## Criterios SMART de Evaluación de Objetivos

El módulo `smart.py` evalúa cada objetivo contra los cinco criterios SMART mediante análisis heurístico de patrones regex:

| Criterio | Descripción | Señales detectadas |
|----------|-------------|-------------------|
| **S**pecific | ¿El objetivo está bien definido y enfocado? | Palabras como "específico", "concreto", "definido", "focused" |
| **M**easurable | ¿Se puede medir el logro? | KPIs, porcentajes, métricas, indicadores, números con unidades |
| **A**chievable | ¿Es realista dado el contexto? | "viable", "factible", "alcanzable", "realistic", "feasible" |
| **R**elevant | ¿Se alinea con el alcance del proyecto? | "relevante", "alineado", "contexto", "relevant", "aligned" |
| **T**ime-bound | ¿Existe un plazo o hito temporal? | "plazo", "fecha", "deadline", "semanal", "mensual", "tiempo real" |

Cada objetivo recibe una puntuación de 0 a 5 según cuántas dimensiones SMART satisface, clasificándose como:
- **Fully SMART** (5/5)
- **Partially SMART** (1–4/5)
- **Not SMART** (0/5)

---

## Clasificación ISO/IEC 25010 de Requisitos No Funcionales

El módulo `iso25010.py` clasifica los NFR según las 8 características de calidad del estándar internacional ISO/IEC 25010:

1. **Adecacidad funcional** (Functional suitability)
2. **Eficiencia de rendimiento** (Performance efficiency)
3. **Compatibilidad** (Compatibility)
4. **Usabilidad** (Usability)
5. **Fiabilidad** (Reliability)
6. **Seguridad** (Security)
7. **Mantenibilidad** (Maintainability)
8. **Portabilidad** (Portability)

---

## Ejemplo de Evaluación

El sistema ha sido probado con documentos de ejemplo como un Sistema de Gestión de Biblioteca, obteniendo los siguientes resultados:

| Elemento | Cantidad |
|----------|----------|
| Objetivos (OBJ) | 3 |
| Requisitos funcionales (IRQ) | 3 |
| Requisitos no funcionales (NFR) | 2 |
| Casos de uso (CU) | 2 |

**Resultado de la evaluación:** 5.52/10 (Nivel: Aceptable con mejoras)

**Hallazgos principales:**
- Objetivos cumplen estructura pero no son SMART
- NFR no categorizados según ISO/IEC 25010
- Casos de uso incompletos (faltan postcondiciones y flujos alternativos)
- Trazabilidad: 80% de cobertura

---

## Créditos y Licencias

Este proyecto integra código de:

- **[SE-rubric-evaluAItor](https://github.com/Lamb-Project/SE-rubric-evaluAItor)** (Lamb-Project) – prompts, lógica de parsing y generación de reportes. Licencia: GNU GPL v3.0.

- **[DiagramLens](https://github.com/Lamb-Project/DiagramLens)** (Lamb-Project) – lógica de descripción de diagramas vía modelos de visión. Licencia: GNU GPL v3.0.

El código de SE-Agentic-Evaluator que integra estos recursos también se distribuye bajo **GNU GPL v3.0**.

---

*Documento generado para el Trabajo de Fin de Grado (TFG)*
*Proyecto: SE-Agentic-Evaluator*
