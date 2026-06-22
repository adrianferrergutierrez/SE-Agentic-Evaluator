# Document de Definició del Projecte
## Evaluaitor-Lamb: Sistema Meta-Agèntic per a l'Avaluació Dinàmica d'Entregables d'Enginyeria del Software

---

## 1. Informació General

| Camp | Valor |
|------|-------|
| **Títol** | Evaluaitor-Lamb: Sistema Meta-Agèntic per a la Generació Dinàmica de Workflows d'Avaluació |
| **Tipus** | Treball de Fi de Grau (TFG) |
| **Àrea** | Enginyeria del Software, Intel·ligència Artificial Agèntica |
| **Versió del Document** | 1.0 |
| **Data** | Maig 2026 |

---

## 2. Resum Executiu

El projecte Evaluaitor-Lamb és un sistema d'avaluació automàtica d'entregables acadèmics d'Enginyeria del Software assistit per IA agèntica. El projecte s'ha desenvolupat de forma iterativa, evolucionant a mesura que s'han identificat millores i nous requisits.

Actualment, el sistema disposa d'un conjunt complet d'eines d'extracció, anàlisi i avaluació, així com un pipeline d'execució fix. La següent evolució del projecte consisteix a transformar-lo en un sistema **meta-agèntic**, capaç d'analitzar una rúbrica d'avaluació arbitrària i generar dinàmicament un workflow personalitzat. Això representa un salt qualitatiu: de ser un "executor de pipelines" a ser un "dissenyador d'avaluacions".

---

## 3. Evolució del Projecte

### 3.1 Fases Completades

El projecte s'ha desenvolupat de forma iterativa. A continuació es detallen les fases ja completades:

| Fase | Descripció | Deliverables | Estat |
|------|------------|--------------|-------|
| **F1** | Disseny inicial del sistema i arquitectura | Arquitectura base, estructura de mòduls | ✅ Completat |
| **F2** | Implementació de tools d'extracció | `objectives.py`, `requirements.py`, `use_cases.py` | ✅ Completat |
| **F3** | Implementació de tools d'anàlisi | `orphans.py`, `smart.py`, `iso25010.py` | ✅ Completat |
| **F4** | Implementació de tools d'avaluació | `criterion_evaluator.py`, `grader.py`, `evaluator.py` | ✅ Completat |
| **F5** | Integració amb LLMs | `dashscope_client.py`, suport Ollama | ✅ Completat |
| **F6** | Configuració i importació de rúbriques | `config_manager.py`, `rubric_importer.py` | ✅ Completat |
| **F7** | Creació de skills per a agents | 8 skills documentades a `.opencode/skills/` | ✅ Completat |
| **F8** | Pipeline orquestrador | `run_evaluation.py` | ✅ Completat |
| **F9** | Refactorització: DashScope per a extracció | Backend unificat, opció `--full` | ✅ Completat |
| **F10** | Validació amb rúbriques reals | 2 documents avaluats completament | ✅ Completat |

### 3.2 Components Actuals del Sistema

| Component | Mòdul | Descripció |
|-----------|-------|------------|
| **Extracció DOCX** | `docx_extract_skill` | Conversió DOCX → Markdown + imatges |
| **Extracció Objectius** | `core/extraction/objectives.py` | Extracció d'objectius (OBJ-X) via LLM |
| **Extracció Requisits** | `core/extraction/requirements.py` | Extracció IRQ/NFR via LLM |
| **Extracció Casos d'Ús** | `core/extraction/use_cases.py` | Extracció CU-XXX via LLM |
| **Anàlisi d'Orfes** | `core/analysis/orphans.py` | Detecció determinista de requisits/objectius sense vinculació |
| **Anàlisi SMART** | `core/analysis/smart.py` | Avaluació heurística d'objectius SMART |
| **Anàlisi ISO 25010** | `core/analysis/iso25010.py` | Classificació de NFR per qualitats ISO |
| **Avaluació de Criteris** | `core/evaluation/criterion_evaluator.py` | Avaluació de criteris de rúbrica amb LLM |
| **Càlcul de Notes** | `core/grading/grader.py` | Càlcul determinista de nota ponderada |
| **Generació d'Informes** | `core/evaluation/evaluator.py` | Síntesi d'avaluacions en informe final |
| **Client DashScope** | `core/clients/dashscope_client.py` | Integració amb API qwen3.6-plus |
| **Config Manager** | `core/config/config_manager.py` | Gestió de configuracions YAML |
| **Rubric Importer** | `core/config/rubric_importer.py` | Importació de rúbriques Markdown → YAML |
| **Pipeline Orquestrador** | `run_evaluation.py` | Script d'execució del pipeline complet |
| **Skills Definides** | `.opencode/skills/` | 8 skills documentades per a agents |

### 3.3 Limitació Actual

El pipeline actual és **fix i predeterminat**. No s'adapta a rúbriques diferents. Sempre executa les mateixes fases en el mateix ordre, independentment dels criteris de la rúbrica. Aquesta limitació és el motor de la següent evolució del projecte.

---

## 4. Objectius del Projecte

### 4.1 Objectiu General

Evolucionar el sistema Evaluaitor-Lamb cap a una arquitectura meta-agèntica capaç de generar dinàmicament workflows d'avaluació personalitzats a partir de rúbriques arbitràries, utilitzant el catàleg d'eines ja implementades.

### 4.2 Objectius Específics

| ID | Objectiu | Mètrica d'Èxit |
|----|----------|----------------|
| **OBJ-1** | Definir un esquema formal per a la representació de workflows dinàmics | Esquema JSON validat amb 3+ exemples |
| **OBJ-2** | Implementar un generador de workflows basat en LLM | Genera workflows vàlids en ≥80% dels casos |
| **OBJ-3** | Implementar un executor de workflows dinàmics | Executa correctament workflows generats |
| **OBJ-4** | Crear un registre centralitzat d'eines (tool registry) | Totes les 14+ tools existents registrades i invocables |
| **OBJ-5** | Validar el sistema amb rúbriques reals | 5+ rúbriques diferents avaluades correctament |
| **OBJ-6** | Documentar el sistema complet per al TFG | Memòria completa amb tots els capítols |

### 4.3 Criteris SMART

- **Specific**: El sistema ha de generar workflows JSON vàlids a partir de rúbriques Markdown/YAML, utilitzant les tools ja existents.
- **Measurable**: ≥80% de workflows generats correctament; puntuacions coherents amb avaluació del pipeline fix.
- **Achievable**: Es basa en un sistema existent completament funcional; només cal afegir la capa de generació dinàmica.
- **Relevant**: Respon a la necessitat real d'adaptabilitat en avaluació acadèmica automatitzada.
- **Time-bound**: Completat en 12 setmanes (veure planning).

---

## 5. Abast i Limitacions

### 5.1 Inclòs a l'Abast

- Esquema de workflow dinàmic (JSON Schema)
- Generador de workflows basat en LLM
- Executor de workflows amb gestió d'errors i condicions
- Tool Registry per registrar les 14+ tools existents
- Validació de workflows generats
- Documentació completa del sistema (mòduls existents + nous)

### 5.2 Fora de l'Abast

- Creació de noves eines d'anàlisi (es reutilitzen les existents)
- Suport per a formats d'entrada diferents de DOCX/PDF/Markdown
- Interfície gràfica d'usuari (només CLI)
- Integració amb plataformes externes (Moodle, GitHub, etc.)
- Refactorització de mòduls existents (es mantenen compatibles)

### 5.3 Limitacions

- Les eines disponibles estan limitades a les ja implementades
- La qualitat del workflow generat depèn de la qualitat del prompt i del model LLM
- El sistema requereix connexió a internet per a les crides a DashScope
- No es garanteix correcció absoluta en rúbriques ambigües o mal definides

---

## 6. Actors i Stakeholders

| Actor | Tipus | Descripció |
|-------|-------|------------|
| **Usuari (Estudiant/Docent)** | Principal | Proporciona el document i la rúbrica, rep l'informe d'avaluació |
| **Agent Meta-Avaluador** | Principal | Analitza la rúbrica, consulta el Tool Registry, genera el workflow, coordina l'execució |
| **Tool Registry** | Suport | Proporciona el catàleg d'eines disponibles amb les seves signatures |
| **LLM (DashScope)** | Suport | Genera el workflow i executa les avaluacions de criteris |
| **Workflow Executor** | Suport | Executa els passos del workflow generat |
| **Professor/Validador** | Passiu | Revisa i valida els resultats del sistema |

---

## 7. Requisits

### 7.1 Requisits Funcionals (IRQ)

| ID | Descripció | Prioritat |
|----|------------|-----------|
| **IRQ-1** | El sistema ha d'acceptar una rúbrica en format Markdown o YAML | Alta |
| **IRQ-2** | El sistema ha d'acceptar un document en format DOCX, PDF o Markdown | Alta |
| **IRQ-3** | El sistema ha de generar un workflow JSON vàlid segons l'esquema definit | Alta |
| **IRQ-4** | El sistema ha de validar el workflow generat abans de l'execució | Alta |
| **IRQ-5** | El sistema ha d'executar el workflow pas a pas, passant dades entre passos | Alta |
| **IRQ-6** | El sistema ha de gestionar errors en l'execució de passos (reintent, skip, abort) | Mitjana |
| **IRQ-7** | El sistema ha de generar un informe final d'avaluació en format Markdown | Alta |
| **IRQ-8** | El sistema ha de registrar un log detallat de l'execució del workflow | Mitjana |
| **IRQ-9** | El sistema ha de mantenir compatibilitat amb el pipeline fix existent | Alta |

### 7.2 Requisits No Funcionals (NFR)

| ID | Descripció | Categoria ISO 25010 |
|----|------------|---------------------|
| **NFR-1** | El workflow s'ha de generar en menys de 30 segons | Performance Efficiency |
| **NFR-2** | L'execució completa no ha de superar els 15 minuts per document | Performance Efficiency |
| **NFR-3** | El sistema ha de ser capaç d'avaluar documents de fins a 200 pàgines | Functional Suitability |
| **NFR-4** | L'esquema de workflow ha de ser extensible per afegir noves tools | Maintainability |
| **NFR-5** | El sistema ha de funcionar en entorns Linux i macOS | Portability |
| **NFR-6** | Les dades de l'usuari no s'han d'emmagatzemar permanentment | Security |
| **NFR-7** | El codi ha de seguir PEP 8 i incloure docstrings | Maintainability |
| **NFR-8** | El sistema ha de tenir tests unitaris amb ≥70% de cobertura | Reliability |

---

## 8. Arquitectura

### 8.1 Arquitectura Objectiu

```
┌─────────────────────────────────────────────────────────────────┐
│                        USUARI (CLI)                             │
│  Input: document.docx + rubrica.md                              │
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
│  - Catàleg 14+    │      │  - Prompt engineering               │
│    tools existents│      │  - JSON Schema validation           │
│  - Signatures     │      │  - Retry logic                      │
│  - Descripcions   │      │                                     │
└───────────────────┘      └─────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      WORKFLOW EXECUTOR                          │
│  - Step dispatcher                                              │
│  - Variable manager (passa dades entre steps)                   │
│  - Condition evaluator (if/else)                                │
│  - Error handler (retry/skip/abort)                             │
│  - Logger                                                       │
└───────┬──────────────────────────────┬──────────────────────────┘
        │                              │
        ▼                              ▼
┌───────────────────┐      ┌─────────────────────────────────────┐
│  TOOLS EXISTENTS  │      │           LLM CLIENT                │
│  ✅ docx_extract  │      │  ✅ DashScope API                   │
│  ✅ extract_*     │      │  ✅ qwen3.6-plus                    │
│  ✅ analyze_*     │      │  ✅ qwen-vl-max (visió)             │
│  ✅ evaluate_*    │      │                                     │
│  ✅ grade         │      │                                     │
│  ✅ report        │      │                                     │
└───────────────────┘      └─────────────────────────────────────┘
```

### 8.2 Components Nous vs Existents

| Component | Estat | Mòdul |
|-----------|-------|-------|
| Tool Registry | 🆕 Nou | `core/tool_registry.py` |
| Workflow Schema | 🆕 Nou | `schemas/workflow_schema.json` |
| Workflow Generator | 🆕 Nou | `core/workflow_generator.py` |
| Workflow Executor | 🆕 Nou | `core/workflow_executor.py` |
| Meta-Agent Controller | 🆕 Nou | `core/meta_agent/controller.py` |
| Tools existents (14+) | ✅ Existent | `core/extraction/`, `core/analysis/`, etc. |
| Client DashScope | ✅ Existent | `core/clients/dashscope_client.py` |
| Config Manager | ✅ Existent | `core/config/config_manager.py` |
| Rubric Importer | ✅ Existent | `core/config/rubric_importer.py` |
| Pipeline Orquestrador | ✅ Existent | `run_evaluation.py` |

### 8.3 Tecnologies

| Component | Tecnologia |
|-----------|------------|
| Llenguatge | Python 3.11+ |
| LLM Backend | DashScope API (qwen3.6-plus, qwen-vl-max) |
| Validació JSON | jsonschema |
| CLI | argparse |
| Logging | Python logging |
| Tests | pytest |
| Control de versions | Git |

---

## 9. Casos d'Ús

### 9.1 Diagrama de Casos d'Ús

```
                    ┌─────────────────────────────────┐
                    │     SE-AGENTIC-EVALUATOR        │
                    │                                 │
  ┌──────┐          │  ┌───────────────────────────┐  │
  │      │──────────│─▶│ Generar Workflow          │  │
  │      │          │  │ (analitza rúbrica + tools)│  │
  │      │          │  └───────────────────────────┘  │
  │      │          │  ┌───────────────────────────┐  │
  │      │──────────│─▶│ Validar Workflow          │  │
  │      │          │  │ (contra JSON Schema)      │  │
  │      │          │  └───────────────────────────┘  │
  │Usuari│          │  ┌───────────────────────────┐  │
  │      │──────────│─▶│ Executar Workflow         │  │
  │      │          │  │ (pas a pas amb condicions)│  │
  │      │          │  └───────────────────────────┘  │
  │      │          │  ┌───────────────────────────┐  │
  │      │──────────│─▶│ Consultar Resultats       │  │
  │      │          │  │ (informe + logs + workflow)│  │
  └──────┘          │  └───────────────────────────┘  │
                    │                                 │
                    │  <<include>>                    │
                    │  ┌───────────────────────────┐  │
                    │  │ Consultar Tool Registry   │  │
                    │  │ (catàleg d'eines)         │  │
                    │  └───────────────────────────┘  │
                    └─────────────────────────────────┘
```

### 9.2 Descripció de Casos d'Ús

| ID | Cas d'Ús | Actor | Descripció | Precondicions | Postcondicions |
|----|----------|-------|------------|---------------|----------------|
| **CU-1** | Generar Workflow | Usuari | L'usuari proporciona rúbrica + document. El sistema analitza la rúbrica, consulta les tools disponibles i genera un workflow JSON personalitzat. | Rúbrica i document vàlids | Workflow JSON generat |
| **CU-2** | Validar Workflow | Sistema | El sistema valida el workflow generat contra l'esquema JSON. Si és invàlid, sol·licita regeneració. | Workflow generat | Workflow vàlid o error |
| **CU-3** | Executar Workflow | Sistema | El sistema executa cada pas del workflow en ordre, passant variables entre passos, gestionant errors i generant logs. | Workflow validat | Resultats d'execució |
| **CU-4** | Consultar Resultats | Usuari | L'usuari rep l'informe final d'avaluació, el workflow executat i els logs detallats. | Workflow executat | Informe lliurat |

---

## 10. Esquema de Workflow (Proposta)

```json
{
  "$schema": "workflow_schema.json",
  "version": "1.0",
  "name": "workflow_hito1",
  "description": "Workflow per avaluar Hito 1",
  "variables": {},
  "steps": [
    {
      "id": "step_1",
      "tool": "docx_extract",
      "params": {
        "input": "${input_docx}",
        "output_dir": "${output_dir}/phase0"
      },
      "output": {
        "document_md": "${step_1.result.contents_md}",
        "images": "${step_1.result.images}"
      }
    },
    {
      "id": "step_2",
      "tool": "rubric_importer",
      "params": {
        "input": "${input_rubric}",
        "output": "${output_dir}/rubric.yaml"
      },
      "output": {
        "config": "${step_2.result.config_path}"
      }
    },
    {
      "id": "step_3",
      "tool": "criterion_evaluator",
      "params": {
        "document": "${step_1.output.document_md}",
        "config": "${step_2.output.config}",
        "full": true,
        "output_dir": "${output_dir}/evaluacion"
      },
      "output": {
        "scores": "${step_3.result.scores}"
      }
    },
    {
      "id": "step_4",
      "tool": "grader",
      "params": {
        "scores": "${step_3.output.scores}",
        "config": "${step_2.output.config}"
      },
      "output": {
        "final_grade": "${step_4.result.weighted_final}"
      }
    },
    {
      "id": "step_5",
      "tool": "report_generator",
      "params": {
        "document": "${step_1.output.document_md}",
        "eval_dir": "${step_3.output.eval_dir}",
        "config": "${step_2.output.config}",
        "output": "${output_dir}/informe.md"
      }
    }
  ]
}
```

---

## 11. Anàlisi de Riscos

| ID | Risc | Probabilitat | Impacte | Mitigació |
|----|------|--------------|---------|-----------|
| **R-1** | El LLM genera workflows invàlids | Alta | Alt | Validador estricte + reintent amb prompt millorat |
| **R-2** | Temps d'execució massa alt | Mitjana | Mitjà | Paral·lelitzar steps independents |
| **R-3** | API DashScope no disponible | Baixa | Alt | Sistema de reintents + fallback a Ollama |
| **R-4** | Tools existents incompatibles amb l'executor | Mitjana | Alt | Adapter pattern per uniformitzar interfícies |
| **R-5** | Rúbrica ambigua o mal definida | Mitjana | Mitjà | Feedback a l'usuari per millorar la rúbrica |
| **R-6** | Pèrdua de compatibilitat amb pipeline fix | Baixa | Alt | Tests de regressió + manteniment de run_evaluation.py |

---

## 12. Planning

### 12.1 Fases Completades

| Fase | Descripció | Durada | Deliverable |
|------|------------|--------|-------------|
| **F1** | Disseny inicial del sistema i arquitectura | - | Arquitectura base, estructura de mòduls |
| **F2** | Implementació de tools d'extracció | - | `objectives.py`, `requirements.py`, `use_cases.py` |
| **F3** | Implementació de tools d'anàlisi | - | `orphans.py`, `smart.py`, `iso25010.py` |
| **F4** | Implementació de tools d'avaluació | - | `criterion_evaluator.py`, `grader.py`, `evaluator.py` |
| **F5** | Integració amb LLMs | - | `dashscope_client.py`, suport Ollama |
| **F6** | Configuració i importació de rúbriques | - | `config_manager.py`, `rubric_importer.py` |
| **F7** | Creació de skills per a agents | - | 8 skills documentades |
| **F8** | Pipeline orquestrador | - | `run_evaluation.py` |
| **F9** | Refactorització: DashScope per a extracció | - | Backend unificat, opció `--full` |
| **F10** | Validació amb rúbriques reals | - | 2 documents avaluats completament |

### 12.2 Fases Pendents

| Fase | Descripció | Durada | Deliverable |
|------|------------|--------|-------------|
| **F11** | Disseny esquema workflow | Set 1-2 | `workflow_schema.json` + exemples |
| **F12** | Meta-agent generador | Set 3-4 | `workflow_generator.py` |
| **F13** | Executor de workflows | Set 5-6 | `workflow_executor.py` |
| **F14** | Tool Registry + adaptadors | Set 7-8 | `tool_registry.py` + integració |
| **F15** | Validació i proves comparatives | Set 9-10 | Informe validació + mètriques |
| **F16** | Documentació TFG completa | Set 11-12 | Memòria TFG + demo |

---

## 13. Deliverables

| ID | Deliverable | Format | Estat |
|----|-------------|--------|-------|
| **D-1** | Document de definició del projecte | Markdown | 📝 En curs |
| **D-2** | Tools d'extracció (3 mòduls) | Python | ✅ Completat |
| **D-3** | Tools d'anàlisi (3 mòduls) | Python | ✅ Completat |
| **D-4** | Tools d'avaluació (3 mòduls) | Python | ✅ Completat |
| **D-5** | Skills per a agents (8 skills) | Markdown | ✅ Completat |
| **D-6** | Pipeline orquestrador | Python | ✅ Completat |
| **D-7** | Esquema de workflow + exemples | JSON | ⏳ Pendent |
| **D-8** | Generador de workflows | Python | ⏳ Pendent |
| **D-9** | Executor de workflows | Python | ⏳ Pendent |
| **D-10** | Tool Registry + integració | Python | ⏳ Pendent |
| **D-11** | Informe de validació | Markdown | ⏳ Pendent |
| **D-12** | Memòria TFG completa | DOCX/PDF | ⏳ Pendent |

---

## 14. Criteris d'Acceptació

El projecte es considerarà completat quan:

1. El sistema generi workflows vàlids per a ≥5 rúbriques diferents
2. L'execució dels workflows generats produeixi resultats coherents amb el pipeline fix
3. El temps de generació + execució no superi els 20 minuts
4. La documentació inclogui tots els mòduls existents i nous
5. El codi nou tingui ≥70% de cobertura de tests
6. El professor validi els resultats com a satisfactoris
7. Es mantingui la compatibilitat amb el pipeline fix existent

---

*Document aprovat per: ___________________ Data: ___/___/______*
