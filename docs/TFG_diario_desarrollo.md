# Diario de Desarrollo - TFG

## Entrada 1: 2026-04-27

**Proyecto:** SE-Agentic-Evaluator  
**Fase:** Configuración inicial y pruebas

---

### Resumen

Hoy he configurado el proyecto SE-Agentic-Evaluator y he probado la skill `evaluator_skill` con un documento de prueba de un sistema de gestión de biblioteca.

---

### Trabajo Realizado

1. **Configuración del entorno**
   - Repositorio con estructura modular: `core/`, `prompts/`, `docs/`
   - Dependencias: `requests`, `ollama` (qwen2.5-coder:1.5b)
   - Skills disponibles: `evaluator_skill`, `tfg_documentation_skill`

2. **Prueba de evaluator_skill**
   - Evaluación completa de documento de requisitos (test1.md)
   - Pipeline ejecutado: extracción → análisis → grading
   - Resultado: 5.52/10

---

### Documento Evalado (test1.md)

| Elemento | Cantidad |
|----------|----------|
| Objetivos (OBJ) | 3 |
| Requisitos funcionales (IRQ) | 3 |
| Requisitos no funcionales (NFR) | 2 |
| Casos de uso (CU) | 2 |

---

### Hallazgos

- Objetivos cumplen estructura pero **no son SMART**
- NFR no categorizados según ISO/IEC 25010
- Casos de uso incompletos (falta postcondiciones)
- Trazabilidad: 80% cobertura

---

### Siguiente paso

- Mejorar calidad de objetivos (SMART)
- Completar análisis de requisitos no funcionales
- Añadir más casos de prueba