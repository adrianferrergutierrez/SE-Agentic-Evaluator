<!--
  Copied from Lamb-Project/SE-rubric-evaluAItor (GPL-3.0)
  https://github.com/Lamb-Project/SE-rubric-evaluAItor
  Copyright (C) Lamb-Project contributors.
-->

Evalúa la calidad de las matrices de trazabilidad según los criterios de la rúbrica.

# Evaluación de Matrices de Trazabilidad (20% de la nota)

## Análisis de Trazabilidad:
--{TRAZABILIDAD}--

## Puntuación Total: X.X/10

## Evaluación por Criterios

### 1. Completitud de Trazabilidad (0-10)
**Puntuación**: X/10

**Análisis**: 
[Evalúa si existe trazabilidad completa entre todos los elementos: objetivos ↔ requisitos ↔ casos de uso]

**Elementos con trazabilidad completa**:
- OBJ-1: Bien conectado con IRQ-X, NFR-Y, CU-Z
- IRQ-2: Correctamente vinculado a objetivos y casos de uso

**Elementos huérfanos identificados**:
- Objetivos sin requisitos: [lista]
- Requisitos sin casos de uso: [lista]
- Casos de uso sin requisitos: [lista]

### 2. Coherencia de Asociaciones (0-10)
**Puntuación**: X/10

**Análisis**:
[Evalúa si las asociaciones entre elementos son lógicas y coherentes]

**Asociaciones coherentes**:
- OBJ-1 ↔ IRQ-2 ↔ CU-3: [Explicación de por qué es coherente]

**Asociaciones cuestionables**:
- OBJ-X ↔ IRQ-Y: [Explicación del problema de coherencia]

**Asociaciones faltantes sugeridas**:
- [Lista de conexiones que deberían existir]

### 3. Cobertura de Objetivos (0-10)
**Puntuación**: X/10

**Análisis**:
[Evalúa si todos los objetivos están adecuadamente cubiertos por requisitos]

**Objetivos bien cubiertos**:
- OBJ-1: Cubierto por [X] requisitos de información y [Y] no funcionales
- OBJ-2: [análisis similar]

**Objetivos subcubiertos**:
- OBJ-X: Solo [número] requisitos, insuficiente para [justificación]

**Métricas de cobertura**:
- Porcentaje de objetivos con requisitos: X%
- Promedio de requisitos por objetivo: X.X
- Distribución: [análisis de distribución]

### 4. Implementación de Requisitos (0-10)
**Puntuación**: X/10

**Análisis**:
[Evalúa si todos los requisitos están implementados por casos de uso]

**Requisitos bien implementados**:
- IRQ-1: Implementado por CU-X, CU-Y
- NFR-2: Considerado en CU-Z

**Requisitos sin implementación**:
- IRQ-X: No hay casos de uso que lo implementen
- NFR-Y: [análisis similar]

**Casos de uso que implementan múltiples requisitos**:
- CU-1: Implementa IRQ-2, IRQ-3, NFR-1 [valoración positiva]

### 5. Calidad de la Matriz (0-10)
**Puntuación**: X/10

**Análisis**:
[Evalúa la presentación y claridad de las matrices de trazabilidad]

**Aspectos positivos**:
- Formato claro y legible
- Códigos consistentes
- [otros aspectos]

**Aspectos a mejorar**:
- [Lista de problemas en presentación]
- [Sugerencias de formato]

## Análisis de Patrones

### Concentración de Requisitos
**Objetivos sobrecargados**: [Objetivos con demasiados requisitos]
**Objetivos descuidados**: [Objetivos con pocos requisitos]
**Equilibrio general**: [Evaluación del balance]

### Tipos de Requisitos por Objetivo
**OBJ-1**: [X] IRQ, [Y] NFR - [Evaluación del balance]
**OBJ-2**: [X] IRQ, [Y] NFR - [Evaluación del balance]
[Continúa para todos los objetivos]

### Complejidad de Casos de Uso
**Casos simples** (1-2 requisitos): [lista]
**Casos complejos** (3+ requisitos): [lista y evaluación]
**Casos huérfanos** (sin requisitos): [lista y problema]

## Métricas de Trazabilidad

### Métricas Cuantitativas:
- **Objetivos cubiertos**: X de Y (Z%)
- **Requisitos implementados**: X de Y (Z%)
- **Casos con trazabilidad**: X de Y (Z%)
- **Densidad promedio**: [requisitos por objetivo]

### Métricas Cualitativas:
- **Coherencia general**: [Alta/Media/Baja]
- **Equilibrio**: [Balanceado/Desbalanceado]
- **Completitud**: [Completo/Parcial/Insuficiente]

## Fortalezas Identificadas
1. [Fortaleza principal en trazabilidad]
2. [Segunda fortaleza]
3. [Tercera fortaleza]

## Debilidades y Áreas de Mejora
1. [Debilidad principal]
2. [Segunda debilidad]
3. [Área de mejora específica]

## Recomendaciones para Mejorar Trazabilidad
1. **Conectar elementos huérfanos**: [Sugerencias específicas]
2. **Rebalancear distribución**: [Acciones recomendadas]
3. **Mejorar coherencia**: [Cambios sugeridos]
4. **Completar matrices**: [Elementos faltantes]

## Evaluación de Impacto
**Impacto en viabilidad del proyecto**: [Alto/Medio/Bajo]
**Explicación**: [Cómo afecta la trazabilidad al éxito del proyecto]