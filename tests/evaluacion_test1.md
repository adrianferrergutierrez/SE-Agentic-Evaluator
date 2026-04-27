# Informe de Evaluación - Sistema de Gestión de Biblioteca

**Entregable:** `tests/test1.md`  
**Fecha:** 2026-04-27  
**Evaluador:** SE-Agentic-Evaluator v1.0

---

## Rúbrica de Evaluación

| Criterio | Puntuación (0-10) | Peso | Nota Ponderada |
|----------|-------------------|------|---------------|
| **Objetivos** | 4.0 | 20% | 0.80 |
| **Requisitos de Información** | 6.7 | 25% | 1.67 |
| **Requisitos No Funcionales** | 5.0 | 15% | 0.75 |
| **Casos de Uso** | 5.0 | 25% | 1.25 |
| **Matrices (Trazabilidad)** | 7.0 | 15% | 1.05 |
| **Nota Final Ponderada** | | | **5.52** |
| ** Media (x̄)** | | | **5.53** |

---

## Resumen Ejecutivo

**Nivel de Desempeño:**，Aceptable con mejoras

El documento presenta una estructura correcta con objetivos, requisitos funcionales, no funcionales y casos de uso. Sin embargo, se detectan deficiencias en la calidad de los objetivos (no SMART), clasificación de NFR, y completitud de los casos de uso.

---

## Análisis por Criterio

### 1. Objetivos (4/10)

| ID | Objetivo | SMART | Evidencia |
|----|---------|-------|------------|
| OBJ-1 | Buscar libros por título, autor, categoría | ❌ | No medible, sin KPIs |
| OBJ-2 | Gestionar préstamos/devoluciones | ❌ | Sin plazo definido |
| OBJ-3 | Notificaciones automáticas | ❌ | Sin indicador temporal |

**Hallazgos (SMART):** Los tres objetivos obtienen 0/10 por:
- Falta de métricas medibles
- Sin indicadores temporales
- Objetivos demasiado vagos

> *"Añade KPIs, porcentajes u otras magnitudes cuantificables"* — smart.notes

---

### 2. Requisitos de Información (6.7/10)

| ID | Descripción | Evaluación |
|----|-------------|-------------|
| IRQ-1 | Búsqueda < 2 segundos | ✅ Medible (2s) |
| IRQ-2 | Registrar préstamos con fecha/hora | ✅ Completo |
| IRQ-3 | Informes mensuales | ⚠️ Incompleto (sin formato definido) |

---

### 3. Requisitos No Funcionales (5/10)

| ID | Descripción | ISO 25010 |
|----|------------|-----------|
| NFR-1 | 100 usuarios concurrentes | ❌ Sin clasificar |
| NFR-2 | SHA-256 para contraseñas | ❌ Sin clasificar |

**Hallazgos (ISO 25010):** Los NFR no fueron clasificados bajo las 8 características ISO/IEC 25010. Recomiendo:
- NFR-1 → **Performance** (Performance efficiency)
- NFR-2 → **Security** (Security confidentiality)

---

### 4. Casos de Uso (5/10)

| CU | Completitud | Observaciones |
|----|-------------|----------------|
| CU-001 | Parcial | Falta postcondición detallada |
| CU-002 | Parcial | Flujo básico, sin excepciones claras |

**Hallazgos:** Los casos de uso carecen de:
- Flujos alternativos completos
- Postcondiciones verificables
- Excepciones documentadas

---

### 5. Matrices / Trazabilidad (7/10)

| Objetivo | IRQ-1 | IRQ-2 | IRQ-3 | NFR-1 | NFR-2 |
|---------|------|------|------|-------|-------|
| OBJ-1   |  ✓   |      |      |   ✓   |       |
| OBJ-2   |      |  ✓   |      |       |   ✓   |
| OBJ-3   |      |      |  ✓   |       |       |

**Cobertura:** 80% de objetivos cubiertos  
**Requisitos huérfanos:** IRQ-3 → OBJ-3 (asociación questionable)

---

## Recomendaciones

1. **Revisar objetivos SMART** — Añadir KPIs, plazos y métricas medibles
2. **Completar casos de uso** — Incluir postcondiciones y flujos alternativos
3. **Clasificar NFR según ISO 25010** — Especificar categoría de calidad
4. **Mejorar IRQ-3** — Definir formato del informe mensual
5. **Verificar trazabilidad** — Asegurar cobertura complete de OBJ-3

---

## Detección de Huérfanos

- **Requisitos sin objetivo:** IRQ-3 (asociación questionable con OBJ-3)
- **Objetivos sin requisitos:** Ninguno (cubiertos al 80%)

---

*Este informe es una herramienta de apoyo. La calificación final es responsabilidad exclusiva del profesorado.*