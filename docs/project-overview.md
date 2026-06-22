# Evaluaitor-Lamb: Document de Presentació del Projecte
## Guia Completa

---

## 1. Resum del Projecte

**Evaluaitor-Lamb** és un sistema d'avaluació automàtica d'entregables acadèmics d'Enginyeria del Software assistit per IA agèntica. El sistema és capaç d'analitzar una rúbrica arbitrària i generar dinàmicament un workflow personalitzat per avaluar un document, utilitzant un catàleg d'eines disponibles.

### Evolució del Projecte

El projecte s'ha desenvolupat de forma iterativa en dues grans etapes:

| Etapa | Descripció | Estat |
|-------|------------|-------|
| **Etapa 1: Pipeline Fix** | Implementació de totes les eines d'extracció, anàlisi i avaluació amb un pipeline predeterminat | ✅ Completat |
| **Etapa 2: Meta-Agent** | Evolució cap a un sistema que genera workflows dinàmics segons la rúbrica | ✅ Completat |

---

## 2. Estructura del Projecte

```
Evaluaitor-Lamb/
├── core/                          # Lògica principal del sistema
│   ├── clients/                   # Clients per a APIs externes
│   │   └── dashscope_client.py    # Client per a DashScope (Qwen)
│   ├── config/                    # Gestió de configuració
│   │   ├── config_manager.py      # Gestor de configs YAML
│   │   └── rubric_importer.py     # Importació de rúbriques Markdown → YAML
│   ├── extraction/                # Eines d'extracció
│   │   ├── docx_extract.py        # DOCX → Markdown + imatges
│   │   ├── xlsx_to_markdown.py    # Excel → Markdown
│   │   ├── objectives.py          # Extracció d'objectius (OBJ-X)
│   │   ├── requirements.py        # Extracció de requisits (IRQ/NFR)
│   │   └── use_cases.py           # Extracció de casos d'ús (CU-XXX)
│   ├── analysis/                  # Eines d'anàlisi determinista
│   │   ├── orphans.py             # Detecció d'orfes (req/obj sense vincle)
│   │   ├── smart.py               # Anàlisi SMART d'objectius
│   │   └── iso25010.py            # Classificació ISO 25010 de NFR
│   ├── evaluation/                # Eines d'avaluació
│   │   ├── criterion_evaluator.py # Avaluació de criteris amb LLM
│   │   └── evaluator.py           # Generació d'informe final
│   ├── grading/                   # Càlcul de notes
│   │   └── grader.py              # Nota ponderada determinista
│   ├── meta_agent/                # Components meta-agèntics
│   │   ├── tool_catalog.py        # Catàleg de tools per al generador
│   │   └── workflow_generator.py  # Generador de workflows amb LLM
│   ├── tool_registry.py           # Registre centralitzat de 13 tools
│   └── workflow_executor.py       # Executor de workflows JSON
│
├── schemas/                       # Esquemes de validació
│   ├── workflow_schema.json       # JSON Schema per a workflows
│   └── examples/                  # Exemples de workflows
│       ├── workflow_hito1.json    # Workflow per Hito 1
│       ├── workflow_objectives_only.json
│       └── workflow_full_analysis.json
│
├── prompts/                       # Prompts per a LLM
│   ├── workflow_generator/        # Prompt per generar workflows
│   │   └── workflow_generation.md
│   └── hito*/                     # Prompts per criteris de rúbriques
│
├── configs/                       # Configuracions YAML
│   ├── rubric_hito1.yaml          # Config per Hito 1
│   └── rubric_hito2.yaml          # Config per Hito 2
│
├── .opencode/skills/              # Skills documentades per a agents
│   ├── docx_extract_skill.md
│   ├── evaluator_skill.md
│   ├── analyze_skill.md
│   ├── extract_skill.md
│   ├── grade_skill.md
│   ├── report_skill.md
│   └── ...
│
├── tests/                         # Tests amb dades reals
│   ├── test-rubrica-hito1/        # Test Hito 1
│   ├── test2/                     # Test Hito 1 (document 2)
│   └── test-1-hito-2/             # Test Hito 2
│
├── docs/                          # Documentació
│   ├── project-definition.md      # Definició del projecte TFG
│   └── evaluation-process.md      # Procés d'avaluació detallat
│
└── run_evaluation.py              # Script orquestrador (pipeline fix)
```

---

## 3. Eines Disponibles (Tool Registry)

El sistema disposa de **13 eines** registrades al `ToolRegistry`, cadascuna amb una interfície uniforme:

| # | Eina | Categoria | Descripció |
|---|------|-----------|------------|
| 1 | `docx_extract` | extract | Converteix DOCX a Markdown amb extracció d'imatges |
| 2 | `xlsx_to_markdown` | extract | Converteix rúbriques Excel a Markdown |
| 3 | `extract_objectives` | extract | Extreu objectius (OBJ-X) del document via LLM |
| 4 | `extract_requirements` | extract | Extreu requisits (IRQ/NFR) del document via LLM |
| 5 | `extract_use_cases` | extract | Extreu casos d'ús (CU-XXX) del document via LLM |
| 6 | `detect_orphans` | analyze | Detecta requisits/objectius sense vinculació (determinista) |
| 7 | `evaluate_smart` | analyze | Avalua objectius amb criteris SMART (heurístic) |
| 8 | `classify_iso25010` | analyze | Classifica NFR per qualitats ISO 25010 (determinista) |
| 9 | `build_context` | analyze | Construeix context consolidat d'anàlisi |
| 10 | `criterion_evaluator` | evaluate | Avalua criteris de rúbrica contra document via LLM |
| 11 | `grader` | grade | Calcula nota ponderada final (determinista) |
| 12 | `report_generator` | report | Genera informe final consolidat via LLM |
| 13 | `rubric_importer` | config | Importa rúbrica Markdown a YAML + prompts |

### Patró de Disseny: Adapter Pattern

Cada eina al `ToolRegistry` és un **adaptador** que:
1. Defineix una interfície uniforme (`name`, `description`, `params`, `output`, `execute()`)
2. Crida a la lògica original existent a `core/extraction/`, `core/analysis/`, etc.
3. Retorna el resultat en un format estàndard

Això permet que el `WorkflowExecutor` sigui **genèric**: no sap què fa cada eina, només sap executar-les.

---

## 4. Procés d'Avaluació

### 4.1 Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                        USUARI (CLI)                             │
│  Input: document.docx + rubrica.xlsx                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    META-AGENT CONTROLLER                        │
│  - Analitza rúbrica                                             │
│  - Consulta Tool Registry                                       │
│  - Genera Workflow JSON                                         │
│  - Coordina execució                                            │
└───────┬──────────────────────────────┬──────────────────────────┘
        │                              │
        ▼                              ▼
┌───────────────────┐      ┌─────────────────────────────────────┐
│  TOOL REGISTRY    │      │         WORKFLOW GENERATOR          │
│  - Catàleg 13     │      │  - Prompt engineering               │
│    tools          │      │  - JSON Schema validation           │
│  - Signatures     │      │  - Retry logic                      │
│  - Descripcions   │      │                                     │
└───────────────────┘      └─────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      WORKFLOW EXECUTOR                          │
│  - Step dispatcher                                              │
│  - Variable manager (${step_id.result.key})                     │
│  - Condition evaluator (if/else)                                │
│  - Error handler (retry/skip/abort)                             │
│  - Logger                                                       │
└───────┬──────────────────────────────┬──────────────────────────┘
        │                              │
        ▼                              ▼
┌───────────────────┐      ┌─────────────────────────────────────┐
│  TOOLS (13)       │      │           LLM CLIENT                │
│  ✅ extract_*     │      │  ✅ DashScope API                   │
│  ✅ analyze_*     │      │  ✅ qwen3.6-plus                    │
│  ✅ evaluate_*    │      │  ✅ qwen-vl-max (visió)             │
│  ✅ grade/report  │      │                                     │
└───────────────────┘      └─────────────────────────────────────┘
```

### 4.2 Fases del Procés

El sistema opera en dos modes clarament diferenciats: **Generació** i **Avaluació**.

#### Mode 1: Generació del Workflow
- **Input:** `rubrica.md` (o `.yaml`) + `document.md` (opcional, per context).
- **Eina:** `run_evaluation.py generate`.
- **Procés:**
  1. El `workflow_generator` analitza la rúbrica i el catàleg de tools.
  2. Genera un JSON amb variables genèriques (`path/to/document.docx`).
  3. Afegeix metadades (`rubric_id`, `created_at`).
  4. Valida contra `workflow_schema.json`.
- **Output:** `workflow_<rubric>.json` reutilitzable.

#### Mode 2: Execució de l'Avaluació
- **Input:** `workflow.json` + `document.docx`.
- **Eina:** `run_evaluation.py evaluate`.
- **Procés:**
  1. El `workflow_executor` injecta variables reals (`input_docx`, `output_dir`).
  2. Valida que totes les variables referenciades existeixen.
  3. Executa cada step resolent referències (`${step_id.result.key}`).
  4. Gestiona errors i guarda logs.
- **Output:** `evaluacion_final.md`, `scores.json`, `execution_log.json`.

### 4.3 Exemple de Workflow Generat

Per a una rúbrica de Hito 2 (Memòria tècnica, Diagrama de classes, Glosario):

```json
{
  "name": "workflow_eval_hito2",
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
      "id": "step_extract_doc",
      "tool": "docx_extract",
      "params": {"input": "${variables.input_docx}", "output_dir": "${variables.output_dir}"},
      "output": {"document_md": "${step_extract_doc.result.contents_md}"},
      "on_error": "abort"
    },
    {
      "id": "step_evaluate",
      "tool": "criterion_evaluator",
      "params": {
        "document": "${step_extract_doc.output.document_md}",
        "config": "${variables.input_rubric}",
        "full": false,
        "output_dir": "${variables.output_dir}/eval"
      },
      "on_error": "abort"
    },
    ...
  ]
}
```

**Nota clau:** El generador decideix NO usar `full: true` per a aquesta rúbrica, evitant extraccions innecessàries. Les variables són genèriques per permetre la reutilització.

---

## 5. Esquema de Workflow (JSON Schema)

L'esquema defineix el format vàlid per a qualsevol workflow generat:

```json
{
  "version": "1.0",
  "name": "string",
  "description": "string",
  "variables": {"key": "value"},
  "steps": [
    {
      "id": "step_[a-zA-Z0-9_]+",
      "tool": "string (must be in registry)",
      "description": "string",
      "params": {"key": "value or ${ref}"},
      "output": {"key": "${step_id.result.key}"},
      "condition": {"if": "expression"},
      "on_error": "abort|skip|retry",
      "max_retries": 0-5
    }
  ]
}
```

### Característiques Clau

- **Variables:** Es poden definir variables inicials i referenciar-les amb `${variable_name}`
- **Outputs de steps:** Es referencien amb `${step_id.result.key}`
- **Condicions:** Suport per a execució condicional (`if/else`)
- **Gestió d'errors:** Tres estratègies (`abort`, `skip`, `retry`)
- **Reintents:** Fins a 5 reintents per step

---

## 6. Resultats de Validació

### Test End-to-End Realitzat

| Mètrica | Valor |
|---------|-------|
| **Document** | `A1.1 Memoria trabajo final (2).docx` |
| **Rúbrica** | `2025 Rúbrica trabajo final - Hito 2.xlsx` |
| **Criteris** | 3 (Memòria tècnica, Diagrama, Glosario) |
| **Workflow Generat** | ✅ Vàlid, 4 steps |
| **Execució** | ✅ Completada (4/4 steps) |
| **Durada** | 323.1s |
| **Nota Ponderada** | 3.75/10 (Insuficiente) |

### Puntuacions per Criteri

| Criteri | Pes | Puntuació | Nota Ponderada |
|---------|-----|-----------|----------------|
| Memòria tècnica | 25% | 7.0/10 | 1.75 |
| Diagrama de classes | 65% | 2.0/10 | 1.30 |
| Glosario de classes | 10% | 7.0/10 | 0.70 |
| **TOTAL** | **100%** | | **3.75/10** |

---

## 7. Comparativa: Pipeline Fix vs Meta-Agent

| Aspecte | Pipeline Fix | Meta-Agent |
|---------|--------------|------------|
| **Flexibilitat** | Fija, sempre igual | Dinàmica, adaptada a rúbrica |
| **Extraccions** | Sempre totes (`--full`) | Només les necessàries |
| **Temps** | ~600s (amb full) | ~323s (sense full) |
| **Tokens** | ~250,000+ | ~180,000 |
| **Adaptabilitat** | Cap | Alta |
| **Manteniment** | Modificar codi | Actualitzar prompt/schema |
| **Reproductibilitat** | Alta | Alta (workflow JSON) |

---

## 8. Tecnologies Utilitzades

| Component | Tecnologia |
|-----------|------------|
| Llenguatge | Python 3.11+ |
| LLM Backend | DashScope API (qwen3.6-plus, qwen-vl-max) |
| Validació JSON | jsonschema |
| CLI | argparse |
| Logging | Python logging |
| Tests | pytest (pendent) |
| Control de versions | Git |
| Dependències | python-docx, pandas, openpyxl, pydantic, requests |

---

## 9. Estat Actual i Treball Futur

### Completat ✅

- [x] Totes les eines d'extracció, anàlisi i avaluació
- [x] Tool Registry amb 13 tools
- [x] Workflow Generator amb LLM
- [x] Workflow Executor amb resolució de variables
- [x] JSON Schema per a workflows
- [x] Conversió XLSX → Markdown
- [x] Test End-to-End amb Hito 2
- [x] Documentació completa

### Pendent ⏳

- [ ] Validació amb 4 rúbriques més (Fase 15)
- [ ] Tests unitaris i d'integració
- [ ] Documentació TFG completa (Fase 16)
- [ ] Optimització de rendiment (paral·lelització)
- [ ] Suport per a visió de diagrames automàtica
- [ ] Bucle de retroalimentació per a re-avaluació automàtica

---

## 10. Punts Forts del Projecte

1. **Agenticitat real:** El sistema no executa un script fix, sinó que *raona* sobre la rúbrica i decideix com avaluar.
2. **Reproductibilitat:** Cada workflow generat és un JSON que es pot guardar, revisar i re-executar.
3. **Extensibilitat:** Per afegir una nova eina, només cal registrar-la al `ToolRegistry`. El generador la podrà usar automàticament.
4. **Eficiència:** El generador aprèn a ser minimalista, evitant extraccions innecessàries.
5. **Traçabilitat:** Cada pas del workflow queda registrat al log d'execució.

---

