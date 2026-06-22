# Registro de Sesión - Evaluaitor-Lamb

## Sesión 1: 2026-04-27

**Fecha:** 2026-04-27  
**Duración:** Aprox. 45 min  
**Tipo:** Desarrollo y evaluación

---

### Objetivos de la Sesión

- [x] Explorar estructura del proyecto
- [x] Explicar cómo añadir skills
- [x] Evaluar entrega de prueba (test1.md)
- [x] Generar informe de evaluación

---

### Actividades Realizadas

| # | Actividad | Resultado |
|---|-----------|-----------|
| 1 | Revisión de archivos del proyecto | Estructura: `core/`, `prompts/`, `docs/` |
| 2 | Explicación de skills | Skills en `.opencode/skills/` |
| 3 | Evaluación de test1.md | Invoice + informe generado |
| 4 | Uso de Ollama (qwen2.5-coder:1.5b) | Extracción y análisis funcionando |

---

### Herramientas Utilizadas

- `core/extraction/objectives.py` — Extracción de objetivos
- `core/extraction/requirements.py` — Extracción de IRQ/NFR
- `core/extraction/use_cases.py` — Extracción de casos de uso
- `core/analysis/traceability.py` — Análisis de trazabilidad
- `core/analysis/smart.py` — Evaluación SMART
- `core/analysis/iso25010.py` — Clasificación ISO 25010
- `core/grading/grader.py` — Cálculo de notas

---

### Resultados de Evaluación (test1.md)

| Criterio | Nota |
|----------|------|
| Objetivos | 4.0 |
| Requisitos_info | 6.7 |
| Requisitos_nf | 5.0 |
| Casos_uso | 5.0 |
| Matrices | 7.0 |
| **Final** | **5.52** |

---

### Problemas Encontrados

| # | Problema | Solución |
|---|----------|----------|
| 1 | Timeout en `orphans.detect_orphans()` | No resuelto (falta verificar API) |
| 2 | Timeout en `completeness.analyze_completeness()` | Timeout excesivo |
| 3 | Atributos `smart.summary` y `iso_characteristic` | Usar `__dict__` para depurar |

---

### Decisiones Técnicas

| # | Decisión | Justificación |
|---|----------|---------------|
| 1 | Usar qwen2.5-coder:1.5b | Modelo local disponible |
| 2 | Evaluación manual de notas | `grader.calculate_scores` no existe |

---

---

## Sesión 2: 2026-04-27 (continuación)

**Fecha:** 2026-04-27  
**Duración:** Aprox. 30 min  
**Tipo:** Evaluación de documentos

---

### Objetivos de la Sesión

- [x] Explicar uso de skills (tfg_documentation_skill)
- [x] Crear diario de desarrollo TFG
- [x] Evaluar segunda entrega (test2.md)
- [x] Actualizar session_log

---

### Actividades Realizadas

| # | Actividad | Resultado |
|---|-----------|-----------|
| 1 | Explicación de tfg_documentation_skill | Creado TFG_diario_desarrollo.md |
| 2 | Evaluación de test2.md (E-Commerce) | Informe generado |
| 3 | Análisis SMART y ISO25010 | Objetivos 0/10, NFR clasificados parcialmente |
| 4 | Comparación de resultados | test2.md > test1.md |

---

### Resultados de Evaluación (test2.md)

| Criterio | Nota |
|----------|------|
| Objetivos | 2.0 |
| Requisitos_info | 8.0 |
| Requisitos_nf | 6.0 |
| Casos_uso | 7.5 |
| Matrices | 9.0 |
| **Final** | **6.52** |

---

### Comparativa test1 vs test2

| Aspecto | test1.md | test2.md |
|---------|----------|----------|
| Objetivos | 3 | 4 |
| IRQ | 3 | 7 |
| NFR | 2 | 5 |
| CU | 2 (incompletos) | 4 (completos) |
| Matriz | No | Sí |
| Diagramas | No | Sí (ASCII) |
| Nota final | 5.52 | 6.52 |

---

### Problemas Encontrados

| # | Problema | Estado |
|---|----------|-------|
| 1 | Timeout en extracción LLM (doc grande) | Persiste |
| 2 | NFR sin clasificar ISO25010 | Parcialmente resuelto |
| 3 | Diagramas en formato ASCII | No valorables con VisionDescriber |

---

### Problemas Encontrados (continuación)

| # | Problema | Análisis | Solución Aplicada |
|---|----------|----------|-------------------|
| 4 | SMART devuelve 0/10 a objetivos con medidas temporales | Patrones regex no reconocen "en menos de X minutos" | Mejorar patrones en `smart.py` |
| 5 | `grader.calculate_scores` no existe | Función no implementada | Usar `RubricGrader().grade()` |
| 6 | Timeout en `analyze_completeness()` | Modelo `qwen3` no instalado, solo `qwen2.5-coder:1.5b` | Cambiar default a `qwen2.5-coder:1.5b` |
| 7 | Agente no invoca herramientas automáticamente | Skills describen herramientas pero no son ejecutables | Pendiente: crear servidor MCP |

---

### Decisiones Técnicas (continuación)

| # | Decisión | Justificación |
|---|----------|---------------|
| 3 | Mejorar patrones SMART en `smart.py` | Reconocer medidas de tiempo explícitas |
| 4 | Cambiar modelo default a `qwen2.5-coder:1.5b` | Evitar timeout por descarga de modelo no disponible |
| 5 | URL Ollama confirmada: `http://localhost:11434/api/chat` | Verificado con `curl /api/tags` |

---

### Mejoras Aplicadas

#### Módulo `core/analysis/smart.py`

Se añadieron patrones regex para mejorar detección SMART:

```python
# measurable: ahora detecta medidas de tiempo
r"\b\d+\s*(segundos?|minutos?|horas?|días?|ms|milisegundos?)\b",
r"\b(en\s+menos\s+de|menos\s+de|máximo|como\s+máximo)\s+\d+\b",

# time_bound: ahora detecta frecuencias y tiempo real
r"\b(en\s+menos\s+de|en\s+más\s+de|hasta\s+)\s*\d+\s*(minutos?|segundos?|horas?|días?|semanas?|meses?)\b",
r"\b(tiempo\s+real|inmediato|instantáneo|automático|automática)\b",
r"\b(frecuencia|periódic|diari|semanal|mensual|anual|trimestral)\b",
```

**Resultado:** Objetivos pasaron de 0/5 a 2/5 (OBJ-1, OBJ-3) y 1/5 (OBJ-2).

---

### Próximos Pasos

- [ ] Añadir soporte para plurales en patrones SMART ("semanales", "mensuales")
- [ ] Integrar VisionDescriber para evaluación de diagramas
- [ ] Crear servidor MCP para exponer herramientas al agente
- [ ] Documentar decisiones arquitectónicas (ADR)
- [ ] Añadir tests unitarios para módulos de análisis
