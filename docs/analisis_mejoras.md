# Análisis de Problemas y Mejoras Propuestas — SE-Agentic-Evaluator

> **Fecha:** 2026-05-02
> **Contexto:** Trabajo de Fin de Grado (TFG)
> **Referencia:** Comparativa con EVALUAITOR-WORKFLOW (LAMB Project)

---

## 1. Configuración Rígida de la Rúbrica

### Problema
Los pesos de la rúbrica están *hardcodeados* en `core/grading/grader.py`:

```python
DEFAULT_WEIGHTS: Dict[str, float] = {
    "objetivos": 0.20,
    "requisitos_info": 0.15,
    "requisitos_nf": 0.10,
    "casos_uso": 0.35,
    "matrices": 0.20,
}
```

Cambiar la rúbrica (añadir un criterio, modificar pesos, adaptar a otro entregable) requiere modificar código fuente y redeployar. Esto limita la reutilización del sistema para otros cursos o asignaturas.

### Mejora Propuesta
Externalizar la configuración a un archivo **YAML o JSON** externo.

**Estructura sugerida:**
```
configs/
├── entregable-1-uso.yaml
├── entregable-2-clases.yaml
└── rubric-custom.yaml
```

**Ejemplo de config YAML:**
```yaml
version: "1.0"
id: "entregable-1-uso"
description: "Evaluación Entregable 1 - Casos de Uso"

models:
  text: "qwen3:32b"
  vision: "qwen3-vl:30b"

rubric:
  criteria:
    - id: "objetivos"
      name: "Objetivos del Sistema"
      weight: 0.20
      prompt: "3_1_evaluacion_objetivos.md"
    - id: "requisitos_info"
      name: "Requisitos de Información"
      weight: 0.15
      prompt: "3_2_evaluacion_requisitos_info.md"
    - id: "requisitos_nf"
      name: "Requisitos No Funcionales"
      weight: 0.10
      prompt: "3_3_evaluacion_requisitos_nf.md"
    - id: "casos_uso"
      name: "Casos de Uso"
      weight: 0.35
      prompt: "3_4_evaluacion_caso_uso.md"
    - id: "matrices"
      name: "Matrices de Trazabilidad"
      weight: 0.20
      prompt: "3_5_evaluacion_matrices.md"

options:
  multimodal: true
  skip_existing: false
```

**Implementación:**
- Crear `core/config/config_manager.py` con validación de esquema (Pydantic).
- Modificar `grader.py` para cargar pesos desde config en lugar de hardcodear.
- Añadir parámetro `--config configs/entregable-1-uso.yaml` al CLI.

**Esfuerzo:** Bajo | **Impacto:** Muy Alto

---

## 2. Falta de Procesamiento por Lotes (Batch)

### Problema
El sistema solo evalúa un documento a la vez. Un profesor con 30-50 alumnos por curso no podrá usarlo de forma eficiente sin ejecutar manualmente cada evaluación.

### Mejora Propuesta
Implementar un modo batch que:
1. Recorra un directorio de PDFs/Markdowns.
2. Ejecute la evaluación completa para cada documento.
3. Genere un **CSV resumen** con las notas finales y métricas por criterio.

**Estructura de salida sugerida:**
```
output/batch-2026-05-02/
├── alumno-1/
│   ├── phase1/
│   ├── phase2/
│   ├── phase3/
│   └── evaluacion_final.md
├── alumno-2/
│   └── ...
└── resumen_batch.csv
```

**Ejemplo de `resumen_batch.csv`:**
```csv
Documento,Objetivos,Req_Info,Req_NF,Casos_Uso,Matrices,Nota_Final,Nivel
alumno-1.pdf,7.5,8.0,6.0,7.0,8.5,7.43,Bueno
alumno-2.pdf,5.0,6.0,4.0,5.5,6.0,5.25,Aceptable
alumno-3.pdf,9.0,9.5,8.5,9.0,9.5,9.10,Excelente
```

**Implementación:**
- Crear `core/batch/batch_processor.py`.
- Añadir skill `/batch-evaluate` o parámetro CLI `--batch-dir submissions/`.
- Generar CSV al finalizar con estadísticas (media, desviación, min, max).

**Esfuerzo:** Medio | **Impacto:** Muy Alto

---

## 3. Especificación de Modelos Insuficiente

### Problema
El README indica `ollama pull qwen3` y `ollama pull qwen3-vl` sin especificar tamaño. Modelos pequeños (<14B) suelen fallar en:
- Extracción estructurada de objetivos/requisitos.
- Razonamiento para evaluación SMART e ISO 25010.
- Descripción técnica de diagramas complejos.

### Mejora Propuesta
Definir **tamaños mínimos recomendados** y añadir validación al inicio:

| Propósito | Modelo Recomendado | Mínimo Aceptable |
|-----------|-------------------|------------------|
| Texto (extracción + evaluación) | `qwen3:32b` | `qwen3:14b` |
| Visión (diagramas) | `qwen3-vl:30b` | `qwen3-vl:7b` |

**Implementación:**
- Crear `core/utils/model_checker.py` con función `validate_models()`.
- Al iniciar, verificar que los modelos existen y tienen el tamaño adecuado.
- Emitir warning si se detecta un modelo por debajo del mínimo.

**Esfuerzo:** Bajo | **Impacto:** Alto

---

## 4. Abstracción de la API de Ollama

### Problema
Las llamadas a Ollama están dispersas o son directas en los módulos. Esto dificulta:
- Añadir soporte para **streaming** (feedback en tiempo real).
- Cambiar de proveedor de LLM en el futuro.
- Manejar errores de red, reintentos y timeouts de forma consistente.

### Mejora Propuesta
Crear una clase `OllamaClient` que centralice todas las interacciones con Ollama.

**Implementación:**
```python
# core/clients/ollama_client.py

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.session = requests.Session()

    def generate(self, model: str, prompt: str, **kwargs) -> str:
        """Generación síncrona sin streaming."""

    def generate_stream(self, model: str, prompt: str, callback=None) -> str:
        """Generación con streaming y callback para progreso."""

    def vision(self, model: str, prompt: str, image_path: Path) -> str:
        """Análisis de imagen con modelo de visión."""

    def check_connection(self) -> bool:
        """Verifica que Ollama está corriendo."""

    def list_models(self) -> List[str]:
        """Lista modelos disponibles localmente."""
```

**Esfuerzo:** Medio | **Impacto:** Alto

---

## 5. Modularización de Skills

### Problema
`evaluator_skill.md` es un monolito con 10 herramientas y 7 reglas. Esto dificulta:
- Reutilizar parcialmente (ej. solo extracción sin evaluación).
- Mantener y actualizar reglas específicas.
- Añadir nuevas habilidades sin afectar las existentes.

### Mejora Propuesta
Dividir en skills más pequeñas y composables:

```
.opencode/skills/
├── evaluator_skill.md          # Skill principal (orquestador)
├── extract_skill.md            # Extracción: objetivos, requisitos, casos de uso
├── analyze_skill.md            # Análisis: trazabilidad, completitud, huérfanos
├── evaluate_skill.md           # Evaluación por criterio con prompts
├── grade_skill.md              # Calificación determinística
├── report_skill.md             # Generación de informe final
└── batch_skill.md              # Procesamiento por lotes
```

Cada skill define su propio rol, herramientas y reglas, y la skill principal las orquesta.

**Esfuerzo:** Medio | **Impacto:** Medio

---

## 6. Gestión de Ficheros Intermedios y Auditoría

### Problema
No queda claro si se guardan los resultados de cada fase (extracción, análisis, evaluación) para auditoría posterior. Perder los intermedios impide:
- Verificar por qué se asignó una nota concreta.
- Re-evaluar sin re-ejecutar todo el pipeline.
- Cumplir con requisitos de transparencia académica.

### Mejora Propuesta
Guardar automáticamente cada fase en una estructura de directorios organizada:

```
output/<doc_id>/
├── phase1_extraction/
│   ├── objectives.md
│   ├── requirements.md
│   ├── use_cases.md
│   └── diagram_summary.md
├── phase2_analysis/
│   ├── traceability.md
│   ├── completeness.md
│   ├── orphans.md
│   ├── smart.md
│   └── iso25010.md
├── phase3_evaluation/
│   ├── eval_objetivos.md
│   ├── eval_req_info.md
│   ├── eval_req_nf.md
│   ├── eval_casos_uso.md
│   └── eval_matrices.md
├── phase4_grading/
│   ├── scores.json
│   └── rubric_table.md
└── evaluacion_final.md
```

**Implementación:**
- Crear `core/utils/output_manager.py`.
- Cada módulo recibe un `output_dir` y guarda su resultado.
- Preservar timestamps para trazabilidad temporal.

**Esfuerzo:** Bajo | **Impacto:** Alto

---

## 7. Mejora del Pipeline de Extracción PDF

### Problema
La combinación PyMuPDF + pytesseract es funcional pero puede perder estructura en documentos complejos (tablas, listas anidadas, fórmulas, columnas).

### Mejora Propuesta
Evaluar integrar **Docling** (IBM) como motor principal de conversión PDF → Markdown. Docling preserva mejor:
- Jerarquía de encabezados.
- Tablas estructuradas.
- Listas y párrafos.
- Referencias cruzadas.

**Implementación:**
- Añadir `docling` a `requirements.txt`.
- Crear `core/extraction/pdf_converter.py` con adaptador Docling.
- Mantener PyMuPDF como fallback si Docling no está disponible.

**Esfuerzo:** Alto | **Impacto:** Medio

---

## 8. Skill de Validación de Entorno

### Problema
El usuario no sabe si Ollama está corriendo, si los modelos están descargados, si las dependencias están instaladas o si hay problemas de conectividad hasta que ejecuta la evaluación y falla.

### Mejora Propuesta
Crear una skill `/status` o `/setup` que verifique al inicio:

| Check | Descripción |
|-------|-------------|
| Ollama activo | `GET /api/tags` responde correctamente |
| Modelos disponibles | `qwen3` y `qwen3-vl` están descargados |
| Versión Python | >= 3.11 |
| Dependencias | Todos los paquetes de `requirements.txt` instalados |
| Espacio en disco | Suficiente para modelos y outputs |
| Permisos | Lectura/escritura en directorios de trabajo |

**Implementación:**
- Crear `core/utils/env_check.py`.
- Añadir skill `.opencode/skills/status_skill.md`.
- Output tipo reporte con ✅/❌ por cada check.

**Esfuerzo:** Bajo | **Impacto:** Medio

---

## 9. Soporte para Streaming en la UI

### Problema
La evaluación de un documento puede tardar varios minutos (especialmente con modelos grandes y diagramas). Sin feedback visual, el usuario piensa que el proceso se ha colgado.

### Mejora Propuesta
Mostrar progreso en tiempo real de cada fase y prompt usando `rich`:

```
┌─────────────────────────────────────────────┐
│ SE-Agentic-Evaluator v1.0                   │
├─────────────────────────────────────────────┤
│ Phase 1: Extracción                         │
│   ✅ Objetivos (3 encontrados)              │
│   ✅ Requisitos (5 encontrados)             │
│   ✅ Casos de uso (2 encontrados)           │
│ Phase 2: Análisis de Diagramas              │
│   🔄 Analizando diagrama_1.png... [====  ]  │
│ Phase 3: Evaluación por Criterio            │
│   ⏳ Pendiente                              │
└─────────────────────────────────────────────┘
```

**Implementación:**
- Usar `rich.live` y `rich.progress` para barras de progreso.
- Consumir el stream de Ollama vía `OllamaClient.generate_stream()`.
- Actualizar estado en tiempo real por fase.

**Esfuerzo:** Medio | **Impacto:** Medio

---

## 10. Modo Pipeline para Comparativa (Valor TFG)

### Problema
El proyecto actual es solo agéntico. Se pierde la oportunidad de comparar ambos enfoques (pipeline scriptado vs. agente dinámico), algo que aporta valor académico significativo a la memoria del TFG.

### Mejora Propuesta
Implementar un **modo pipeline scriptado** que ejecute las fases en orden fijo y comparar con el modo agéntico en:

| Métrica | Pipeline | Agente |
|---------|----------|--------|
| Tiempo total de ejecución | | |
| Calidad de evaluación (vs nota profesor) | | |
| Tokens consumidos | | |
| Flexibilidad ante documentos atípicos | | |
| Facilidad de reconfiguración | | |

**Implementación:**
- Crear `pipeline_mode.py` que ejecute: extracción → análisis → evaluación → grading en orden fijo.
- Script de comparativa `compare_modes.py` que ejecute ambos modos sobre los mismos documentos y genere tabla comparativa.
- Incluir capítulo en la memoria del TFG con análisis de resultados.

**Esfuerzo:** Alto | **Impacto:** Alto (para TFG)

---

## Resumen de Prioridades

| # | Mejora | Prioridad | Esfuerzo | Impacto |
|---|--------|-----------|----------|---------|
| 1 | Configuración YAML externa | 🔴 Alta | Bajo | Muy Alto |
| 2 | Procesamiento por lotes | 🔴 Alta | Medio | Muy Alto |
| 3 | Validación de modelos | 🔴 Alta | Bajo | Alto |
| 4 | Abstracción API + Streaming | 🟡 Media | Medio | Alto |
| 5 | Modularización de Skills | 🟡 Media | Medio | Medio |
| 6 | Auditoría de ficheros intermedios | 🟡 Media | Bajo | Alto |
| 7 | Integrar Docling | 🟢 Baja | Alto | Medio |
| 8 | Skill de status/setup | 🟢 Baja | Bajo | Medio |
| 9 | UI con streaming y progreso | 🟢 Baja | Medio | Medio |
| 10 | Modo Pipeline para comparativa TFG | 🟡 Media | Alto | Alto |

---

## Hoja de Ruta Recomendada

### Fase 1: Cimientos (Semanas 1-2)
1. Configuración YAML externa
2. Validación de modelos
3. Gestión de ficheros intermedios

### Fase 2: Funcionalidad Crítica (Semanas 3-4)
4. Procesamiento por lotes
5. Skill de status/setup
6. Abstracción API de Ollama

### Fase 3: Valor TFG (Semanas 5-6)
7. Modo Pipeline scriptado
8. Comparativa Pipeline vs Agente
9. UI con streaming y progreso

### Fase 4: Refinamiento (Semanas 7-8)
10. Modularización de Skills
11. Integración de Docling
12. Documentación final y memoria

---

*Documento generado para el Trabajo de Fin de Grado (TFG)*
*Proyecto: SE-Agentic-Evaluator*
