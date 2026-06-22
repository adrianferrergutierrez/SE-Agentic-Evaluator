# Guía de Uso del CLI `se-agent`

## Qué es

`se-agent` es la interfaz de línea de comandos principal para interactuar con el agente de Evaluaitor-Lamb. Sigue el patrón Turtle y permite:

- iniciar una nueva sesión con una tarea
- continuar una sesión existente
- listar sesiones guardadas
- obtener salida en JSON

## Requisitos

- Python 3.11+ o compatible con el entorno del proyecto
- Variables de entorno cargadas desde `.env`
- Acceso a las dependencias del repositorio

Instalación típica:

```bash
pip install -r requirements.txt
```

## Comandos disponibles

### Ejecutar una tarea

```bash
./se-agent run "avalua aquesta memòria amb la rúbrica X"
```

**Nota:** El subcomando `run` es obligatorio. La forma corta sin `run` no está soportada.

### Continuar una sesión

```bash
./se-agent run --session-id abc123 "genera l'informe final"
```

Si el identificador de sesión existe, el agente reutiliza el contexto previo.

### Listar sesiones

```bash
./se-agent list-sessions
```

### Salida en JSON

```bash
./se-agent run --json "resum dels punts febles del document"
```

Esto devuelve un objeto con:

- `session_id`
- `response`

## Flujo interno

El CLI realiza estos pasos:

1. Carga variables de entorno con `python-dotenv`.
2. Crea una instancia de `Agent`.
3. Llama a `agent.run(message, session_id)`.
4. Guarda o reutiliza la sesión mediante `SessionStore`.
5. Imprime la respuesta en consola o en formato JSON.

## Ejemplos prácticos

### Evaluar una memoria

```bash
./se-agent run "avalua la memòria i destaca els punts febles"
```

### Continuar con correcciones manuales

```bash
./se-agent run --session-id 7c35a71a-3de4-4f5f-9777-4af9df3bba50 "aplica els canvis proposats a la secció d'arquitectura"
```

### Obtener una respuesta estructurada

```bash
./se-agent run --json "resumeix la rúbrica i proposa un workflow"
```

## Solución de problemas

### El comando no arranca

- Comprueba que el archivo `se-agent` tiene permisos de ejecución.
- Verifica que estás en la raíz del repositorio.

### No encuentra la sesión

- Usa `list-sessions` para ver los identificadores disponibles.
- Confirma que el `session-id` que pasas existe realmente.

### El agente devuelve errores de entorno

- Revisa que `.env` esté configurado correctamente.
- Confirma que las dependencias están instaladas.

## Relación con otros comandos del proyecto

Este CLI es independiente de los orquestadores de workflows:

- `run_evaluation.py`: genera y ejecuta workflows de evaluación.
- `core/meta_agent/workflow_generator.py`: genera workflows JSON.
- `core/workflow_executor.py`: ejecuta workflows ya creados.

`se-agent`, en cambio, sirve para interactuar directamente con el agente conversacional y sus sesiones.
