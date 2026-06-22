# Evaluaitor-Lamb

Assistent meta-agèntic interactiu per a l'avaluació de lliurables acadèmics, dissenyat per **complementar** el judici docent, **no substituir-lo**. 

Aquest projecte implementa un cicle de vida complet d'agent d'IA seguint la metodologia **"Agents All the Way Down"** del professor Marc Alier (UPC), empaquetat com a eina de línia de comandes (CLI) aplicant el patró Turtle.

> ⚠️ **Nota ètica i d'ús**  
> Aquest sistema s'ha d'emprar exclusivament com a eina de suport. La qualificació final i totes les decisions acadèmiques han de romandre sota responsabilitat de l'equip docent humà.

---

## 🎯 Arquitectura i Característiques Principals

- **Agent Loop Independent:** Bucle d'agent nadiu i segur que orquestra 18 *tools* especialitzades sense dependre de cap framework pesat de tercers.
- **Workflow Generator & Executor:** Generació automàtica de plans d'execució JSON a partir de rúbriques YAML. Un cop generat, un workflow es pot reutilitzar amb infinits documents per optimitzar costos i temps.
- **Visió Multimodal Local i Cloud:** Suport natiu per descriure diagrames UML inserits als documents mitjançant models de visió, traduint la imatge a text per l'avaluació.
- **Suport Multi-Proveïdor (Capa d'abstracció):** Transició transparent entre entorns Cloud i Local canviant només una variable d'entorn.
  - *Cloud:* DashScope (Qwen), OpenRouter (Llama, Gemma), Google Gemini.
  - *Local:* Suport natiu per Ollama (ex. `qwen2.5-coder:1.5b`, `llava`) per assegurar el compliment estricte del **RGPD**.
- **Càlcul Determinista:** El càlcul de les notes finals es fa sempre mitjançant codi Python determinista basat en els pesos de la rúbrica; l'IA només genera evidències texturals i sub-puntuacions per criteri.

---

## 📂 Estructura del Repositori

```text
Evaluaitor-Lamb/
├── configs/               # Rúbriques en format YAML (pesos, descriptors)
├── core/
│   ├── agent/             # Lògica core: agent.py, security.py, tools.py
│   ├── clients/           # Capa d'abstracció LLM: base.py, ollama_client.py, dashscope_client.py
│   ├── meta_agent/        # Workflow Generator
│   ├── analysis/          # Tools d'anàlisi: completitud, trazabilitat, orfes (determinístic)
│   ├── extraction/        # Tools per extracció de docs i processament multimodal
│   └── grading/           # Càlcul de qualificacions matemàticament assegurades
├── docs/                  # Memòria del TFG, annexos i imatges
├── evaluations/           # Informes generats per l'agent (ex. memoria_garcia)
├── workflows/             # Workflows JSON auto-generats
├── se-agent               # Punt d'entrada de la CLI interactiva
└── README.md
```

---

## 🚀 Requisits i Instal·lació

### 1. Entorn Virtual
Es recomana utilitzar un entorn virtual Python (versió recomanada: 3.10+):
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Variables d'Entorn (.env)
Crea un fitxer `.env` a l'arrel del projecte per configurar el teu proveïdor:

**Opció A: Ús en Local (Privacitat Total amb Ollama)**
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:1.5b
OLLAMA_VISION_MODEL=llava
```

**Opció B: Ús Cloud (Alta precisió)**
```env
LLM_PROVIDER=dashscope
DASHSCOPE_API_KEY=la_teva_clau_aqui
DASHSCOPE_MODEL=qwen-max
DASHSCOPE_VISION_MODEL=qwen-vl-max
```

### 3. Ollama (Només per a ús local)
Si optes per la via local, descarrega't Ollama (https://ollama.com) i baixa els models:
```bash
ollama pull qwen2.5-coder:1.5b
ollama pull llava
```

---

## 💻 Ús de la CLI (se-agent)

La interacció principal amb el sistema es fa a través de l'executable `se-agent`, el qual implementa el **Turtle Pattern** per mantenir sessions interactives.

### 1. Iniciar una nova avaluació (run)
Per demanar a l'agent que executi una tasca o avaluï un document nou:
```bash
./se-agent run "Avalua la memòria 'docs/memoria.pdf' utilitzant la rúbrica de l'hito 2"
```

### 2. Llistar sessions actives
El sistema guarda automàticament l'estat de les converses per poder-les reprendre més tard. Pots veure-les amb:
```bash
./se-agent list-sessions
```

### 3. Continuar una sessió existent (Multi-turn)
Si vols que l'agent continuï una avaluació prèvia, per exemple per demanar-li correccions manuals o que generi l'informe final després d'avaluar:
```bash
./se-agent run --session-id abc123def456 "Genera l'informe final Markdown basat en l'avaluació que acabem de fer"
```

### 4. Mode d'integració (JSON Output)
Si es vol integrar el CLI amb altres scripts o interfícies gràfiques, es pot forçar l'output estructurat:
```bash
./se-agent run --json "Resumeix els punts febles del document"
```

---

## 📜 Crèdits i Llicència

Desenvolupat com a Treball de Fi de Grau (TFG).

Aquest projecte integra conceptes estructurals i fragments clau de:
- **[SE-rubric-evaluAItor](https://github.com/Lamb-Project/SE-rubric-evaluAItor)** (Lamb-Project) – Lògica base de parsing de rúbriques.
- **[DiagramLens](https://github.com/Lamb-Project/DiagramLens)** (Lamb-Project) – Lògica d'anotació multimodal de diagrames tècnics.

Distribuït sota llicència **GNU GPL v3.0**.
