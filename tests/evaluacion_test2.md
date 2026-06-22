# Informe de Evaluación - Sistema E-Commerce

**Entregable:** `tests/test2.md`  
**Fecha:** 2026-04-27  
**Evaluador:** Evaluaitor-Lamb v1.0

---

## Rúbrica de Evaluación

| Criterio | Puntuación (0-10) | Peso | Nota Ponderada |
|----------|-------------------|------|---------------|
| **Objetivos** | 2.0 | 20% | 0.40 |
| **Requisitos de Información** | 8.0 | 25% | 2.00 |
| **Requisitos No Funcionales** | 6.0 | 15% | 0.90 |
| **Casos de Uso** | 7.5 | 25% | 1.88 |
| **Matrices (Trazabilidad)** | 9.0 | 15% | 1.35 |
| **Nota Final Ponderada** | | | **6.52** |
| ** Media (x̄)** | | | **6.50** |

---

## Resumen Ejecutivo

**Nivel de Desempeño:**Bueno

Documento muy completo de un sistema e-commerce. Presenta 4 objetivos, 7 IRQ, 5 NFR, 4 casos de uso bien documentados, y matriz de trazabilidad. Incluye diagramas arquitectónicos y de casos de uso.

---

## Análisis por Criterio

### 1. Objetivos (2/10)

| ID | Objetivo | SMART | Evidencia |
|----|---------|-------|-----------|
| OBJ-1 | Checkout < 3 min | ⚠️ Parcial | Tiempo definidos pero no medible global |
| OBJ-2 | Inventario tiempo real | ❌ | Sin KPIs de latencia |
| OBJ-3 | Confirmaciones < 5 min | ⚠️ Parcial | Tiempo definido |
| OBJ-4 | Informes semanales/mensuales | ❌ | Sin frecuencia exacta |

**Hallazgos SMART:** Los objetivos tienen tiempos pero faltan:
- Métricas concretas de éxito
- Indicadores de verificación
- Restricciones de alcance

---

### 2. Requisitos de Información (8/10)

| ID | Descripción | Evaluación |
|----|-------------|-------------|
| IRQ-1 | Búsqueda por nombre, categoría, precio, marca | ✅ Completo |
| IRQ-2 | Carrito ≥50 productos | ✅ Medible |
| IRQ-3 | Pago PCI-DSS | ✅ Correcto |
| IRQ-4 | Actualización inventario automática | ✅ Claro |
| IRQ-5 | Email confirmación + seguimiento | ✅ Completo |
| IRQ-6 | Informes con filtros | ✅ Detallado |
| IRQ-7 | Registro con validación email | ✅ Correcto |

**Objetivos asociados:** Todos bien vinculados (ver matriz)

---

### 3. Requisitos No Funcionales (6/10)

| ID | Descripción | ISO 25010 |
|----|------------|-----------|
| NFR-1 | 500 usuarios, <2s respuesta | ✅ performance_efficiency |
| NFR-2 | bcrypt + TLS 1.3 | ⚠️ Sin clasificar (Security) |
| NFR-3 | 99.9% disponibilidad | ⚠️ Sin clasificar (Availability) |
| NFR-4 | 200% picos | ⚠️ Sin clasificar (Scalability) |
| NFR-5 | WCAG 2.1 AA | ✅ usability |

**Recomendación:** Clasificar NFR-2 a NFR-4 segúnISO/IEC 25010

---

### 4. Casos de Uso (7.5/10)

| CU | Completitud | Flujos | Postcondición |
|----|-----------|--------|----------------|
| CU-001 | ✅ Registro usuario | Principal + Alternativo + Excepciones | ✅ |
| CU-002 | ✅ Realizar compra | Principal + 2 Alternativos + 2 Excepciones | ✅ |
| CU-003 | ✅ Gestionar inventario | Principal + Alternativo + Excepción | ✅ |
| CU-004 | ✅ Generar informe | Principal + Alternativo + Excepción | ✅ |

**Calidad:** Buenos casos de uso con pre/postcondiciones claras, flujos alternativos y excepciones documentadas.

---

### 5. Matrices / Trazabilidad (9/10)

| Objetivo | IRQ-1 | IRQ-2 | IRQ-3 | IRQ-4 | IRQ-5 | IRQ-6 | IRQ-7 | NFR-1 | NFR-2 | NFR-3 | NFR-4 | NFR-5 |
|---------|------|------|------|------|------|------|------|-------|-------|-------|-------|-------|
| OBJ-1   |  ✓  |  ✓  |  ✓  |      |      |      |  ✓  |   ✓   |   ✓  |       |       |   ✓   |
| OBJ-2   |      |      |      |  ✓  |      |      |      |   ✓   |       |   ✓  |  ✓   |       |
| OBJ-3   |      |      |      |      |  ✓  |      |      |   ✓   |       |   ✓  |       |       |
| OBJ-4   |      |      |      |      |      |  ✓  |      |   ✓   |       |   ✓  |  ✓   |       |

**Cobertura:** 100%  
**Matriz proporcionada:** ✅ Sí (en documento)

---

### 6. Diagramas (No puntuado pero valorable)

- Figura 1: Arquitectura del sistema (NGINX → Node.js → PostgreSQL)
- Figura 2: Diagrama de casos de uso

**Nota:** Los diagramas están en formato texto ASCII. Para evaluación completa sería necesario usar VisionDescriber.

---

## Recomendaciones

1. **Revisar objetivos SMART** — Añadir KPIs verificables a cada objetivo
2. **Clasificar todos los NFR** según ISO 25010 (NFR-2→Security, NFR-3→Availability, NFR-4→Performance)
3. **Completar diagramas UML** — Usar estándar (no ASCII) para diagramas arquitectónicos

---

*Este informe es una herramienta de apoyo. La calificación final es responsabilidad exclusiva del profesorado.*