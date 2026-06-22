# Workflow d'Avaluació - Hito 1: MOVE&GROW

## Document Avaluat
- **Fitxer:** `tests/test-rubrica-hito1/A1.1 Memoria trabajo final.docx`
- **Rúbrica:** `tests/test-rubrica-hito1/rubrica-hito-1.md`
- **Resultat:** `tests/test-rubrica-hito1/output/evaluacion/evaluacion_final.md`

---

## Resum del Workflow Seguit

L'avaluació s'ha realitzat seguint el pipeline oficial definit a les skills del projecte `.opencode/skills/`, concretament aplicant les skills: `docx_extract_skill`, `evaluator_skill`, `analyze_skill`, `grade_skill` i `report_skill`.

---

## Fase 0: Conversió DOCX → Markdown (`docx_extract_skill`)

**Objectiu:** Convertir el document Word a Markdown estructurat amb extracció d'imatges.

**Eina utilitzada:** `python-docx` (pandoc no disponible)

**Procés:**
1. Verificació que el fitxer DOCX existeix
2. Creació del directori de sortida: `tests/test-rubrica-hito1/output/phase0_extract/`
3. Extracció de text amb `python-docx`, preservant l'estructura d'encapçalaments (Title → #, Heading 1 → ##, etc.)
4. Extracció de taules convertides a format Markdown
5. Extracció d'imatges com a fitxers independents amb referències al Markdown

**Resultat:**
- `contents.md`: 95.791 caràcters
- `img/`: 26 imatges extretes

**Comanda executada:**
```bash
python3 -c "import docx, os, re, base64; from pathlib import Path; ..." 
# (script python-docx segons docx_extract_skill.md Opció B)
```

---

## Fase 1: Importació de Rúbrica Externa (`evaluator_skill`)

**Objectiu:** Convertir la taula Markdown de la rúbrica a configuració YAML compatible amb el sistema.

**Eina utilitzada:** `core/config/rubric_importer.py`

**Procés:**
1. Lectura de `rubrica-hito-1.md` (12 criteris en format taula)
2. Generació automàtica de `configs/rubric_hito1.yaml` amb:
   - IDs de criteri normalitzats
   - Pesos normalitzats (suma = 1.00)
   - Descripcions i prompts associats
3. Generació de 12 prompts individuals a `prompts/hito1/`

**Correcció aplicada:** Els prompts es van generar a `prompts/hito1/` però el config els referenciava sense el prefix. Es va corregir amb:
```python
for criterion in cfg['rubric']['criteria']:
    criterion['prompt'] = 'hito1/' + criterion['prompt']
```

**Resultat:**
- `configs/rubric_hito1.yaml`: Configuració completa amb 12 criteris
- `prompts/hito1/`: 12 fitxers de prompt (un per criteri)

**Comanda executada:**
```bash
python core/config/rubric_importer.py \
  --input tests/test-rubrica-hito1/rubrica-hito-1.md \
  --output configs/rubric_hito1.yaml \
  --prompts-dir prompts/hito1/
```

---

## Fase 2: Avaluació de Criteris (`analyze_skill` / `evaluator_skill`)

**Objectiu:** Avaluar cada criteri de la rúbrica contra el document Markdown utilitzant LLM (qwen3.6-plus via DashScope).

**Eina utilitzada:** `core/evaluation/criterion_evaluator.py`

**Procés:**
1. Càrrega del document Markdown (`contents.md`)
2. Càrrega de la configuració YAML (`rubric_hito1.yaml`)
3. Per a cada criteri:
   - Càrrega del prompt template corresponent
   - Injecció del document al placeholder `--{DOCUMENTO}--`
   - Injecció del context d'anàlisi (no disponible → missatge per defecte)
   - Generació amb LLM (qwen3.6-plus, temperature=0.1, max_tokens=4096)
   - Extracció de la puntuació amb regex (`X/10`)
   - Guardat de `eval_<criterio>.md`

**Resultat:** 12 fitxers `eval_*.md` + `scores.json`

| Criteri | Puntuació |
|---|---|
| Portada | 7.0/10 |
| Tabla de contenidos | 0.0/10 |
| Estilo del documento | 7.0/10 |
| Objetivos | 7.0/10 |
| Requisitos de información | 4.0/10 |
| Requisitos no funcionales | 10.0/10 |
| Diagrama de casos de uso | 7.0/10 |
| Descripción de actores | 7.0/10 |
| Descripción de casos de uso | 10.0/10 |
| Matriz de rastreabilidad: obj-req | 10.0/10 |
| Matriz de rastreabilidad: req-req | 0.0/10 |
| Ética informática | 7.0/10 |

**Comanda executada:**
```bash
PYTHONPATH=/home/adrif/Evaluaitor-Lamb python3 core/evaluation/criterion_evaluator.py \
  --document tests/test-rubrica-hito1/output/phase0_extract/contents.md \
  --config configs/rubric_hito1.yaml \
  --output tests/test-rubrica-hito1/output/evaluacion/
```

---

## Fase 3: Càlcul de Nota Ponderada (`grade_skill`)

**Objectiu:** Calcular la nota final ponderada de forma determinística (sense al·lucinacions numèriques).

**Eina utilitzada:** `core/grading/grader.py`

**Procés:**
1. Lectura de `scores.json` amb les puntuacions per criteri
2. Lectura de `rubric_hito1.yaml` per obtenir els pesos
3. Creació de `criteria.json` amb el format `{criteria: [{name, score, weight}]}`
4. Càlcul de la mitjana ponderada amb `weighted_score()`

**Resultat:**
- **Nota ponderada:** 7.21/10
- **Mitjana aritmètica (x̄):** 6.33/10
- **Nivell de rendiment:** Bueno

**Comanda executada:**
```bash
PYTHONPATH=/home/adrif/Evaluaitor-Lamb python3 core/grading/grader.py \
  --criteria-json tests/test-rubrica-hito1/output/evaluacion/criteria.json
```

---

## Fase 4: Generació d'Informe Final (`report_skill`)

**Objectiu:** Sintetitzar totes les avaluacions en un informe consolidat amb recomanacions.

**Eina utilitzada:** `core/evaluation/evaluator.py`

**Procés:**
1. Càrrega de 12 fitxers `eval_*.md`
2. Càrrega de `scores.json`
3. Càrrega de `rubric_hito1.yaml` per a pesos i etiquetes
4. Generació de taula de rúbrica amb `RubricGrader`
5. Generació d'informe amb LLM (qwen3.6-plus) utilitzant el prompt `4_1_generacion_informe.md`
6. Guardat de `evaluacion_final.md`

**Resultat:** Informe complet amb:
- Resum executiu
- Anàlisi per criteris amb evidències
- Observacions transversals
- Recomanacions prioritzades
- Fortaleses del projecte
- Conclusions
- Peu de pàgina obligatori

**Comanda executada:**
```bash
PYTHONPATH=/home/adrif/Evaluaitor-Lamb python3 core/evaluation/evaluator.py \
  --document tests/test-rubrica-hito1/output/phase0_extract/contents.md \
  --eval-dir tests/test-rubrica-hito1/output/evaluacion/ \
  --config configs/rubric_hito1.yaml \
  --scores tests/test-rubrica-hito1/output/evaluacion/scores.json \
  --output tests/test-rubrica-hito1/output/evaluacion/
```

---

## Diagrama del Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE D'AVALUACIÓ                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │  FASE 0      │    │  FASE 1      │    │  FASE 2          │  │
│  │  DOCX→MD     │───▶│  Importar    │───▶│  Avaluar         │  │
│  │  (docx_ext)  │    │  Rúbrica     │    │  Criteris        │  │
│  └──────────────┘    └──────────────┘    └──────────────────┘  │
│         │                    │                     │            │
│         ▼                    ▼                     ▼            │
│   contents.md          rubric_hito1.yaml    eval_*.md +         │
│   img/ (26)            prompts/hito1/       scores.json         │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐                           │
│  │  FASE 3      │    │  FASE 4      │                           │
│  │  Calcular    │───▶│  Generar     │                           │
│  │  Nota        │    │  Informe     │                           │
│  └──────────────┘    └──────────────┘                           │
│         │                    │                                   │
│         ▼                    ▼                                   │
│   7.21/10 (Bueno)     evaluacion_final.md                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Skills Utilitzades

| Skill | Fase | Descripció |
|-------|------|------------|
| `docx_extract_skill.md` | Fase 0 | Conversió DOCX → Markdown + extracció d'imatges |
| `evaluator_skill.md` | Fase 1-2 | Importació de rúbrica i avaluació de criteris |
| `analyze_skill.md` | Fase 2 | Anàlisi amb context (huérfanos, SMART, ISO 25010) |
| `grade_skill.md` | Fase 3 | Càlcul determinístic de nota ponderada |
| `report_skill.md` | Fase 4 | Generació d'informe final consolidat |

---

## Regles Aplicades

- **R1 (Evidència obligatòria):** Cada judici evaluatiu inclou cites textuals, IDs d'elements o descripcions de diagrames.
- **R2 (Context abans de qualificar):** S'ha intentat construir context amb extracció i anàlisi. En aquest cas, els mòduls d'extracció requereixen Ollama amb models específics no disponibles.
- **R4 (Càlcul determinístic):** La nota final s'ha calculat exclusivament amb `core/grading/grader.py`, mai manualment.
- **R5 (Format de l'informe):** L'informe inclou taula de rúbrica, resum executiu, anàlisi per criteri, recomanacions i peu de pàgina obligatori.

---

## Limitacions

- **Ollama:** Els mòduls d'extracció (`extract_objectives`, `extract_requirements`, `extract_use_cases`) requereixen Ollama amb el model `qwen3`. Només estava disponible `qwen2.5-coder:1.5b`, insuficient per a aquestes tasques.
- **Anàlisi previ:** No s'han pogut executar les anàlisis de huérfanos, SMART i ISO 25010 per la dependència dels mòduls d'extracció.
- **Visió per a diagrames:** Els diagrames UML s'han avaluat sense visió directa de les imatges extretes, basant-se únicament en el text del document.

---

*Document generat automàticament com a part del procés d'avaluació del Hito 1 - Enginyeria del Software I*

*Nota: Aquest informe és una eina de suport. La qualificació final és responsabilitat exclusiva del professorat.*
