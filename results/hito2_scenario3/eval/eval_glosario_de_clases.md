# Evaluación: Glosario de clases

## Análisis
El documento incluye la sección 13 "Glosario de clases" con 11 tablas (Tablas 43 a 53) que cubren las entidades identificadas en el modelo de dominio. Cada clase cuenta con una **descripción clara** de su significado y un listado de **atributos** con sus tipos de datos. Sin embargo, el apartado de **"Operaciones"** presenta un error conceptual recurrente y significativo: en lugar de definir métodos o comportamientos funcionales propios de la clase (ej. `registrar()`, `calcularDistancia()`, `actualizarEstado()`), se utilizan sistemáticamente para describir **relaciones de asociación y multiplicidades** con otras clases (ej. *"el usuario puede enviar 0 o varias donaciones"*, *"una ruta predeterminada puede ser creada por uno o varios usuarios"*, *"Zona: Un mantenimiento en específico se realiza en una zona..."*).

Además, se detectan inconsistencias de modelado:
- La clase **"Hacer ruta"** (Tabla 44) corresponde conceptualmente a un caso de uso o acción del sistema, no a una entidad del dominio, y carece de atributos intrínsecos.
- Atributos como `Usuario (String)` en la clase `Árbol` o `Empresa de plantación` en `Mantenimiento` actúan como claves foráneas. En un glosario de modelo de dominio conceptual, estas deberían modelarse como asociaciones en el diagrama, no como atributos primitivos.
- La clase `Tipo de transporte` se define correctamente como enumeración, pero el resto de operaciones no reflejan responsabilidades cohesivas ni lógica de negocio.

Por tanto, aunque se describen todas las clases y su significado, y se listan atributos, los métodos/operaciones **no están correctamente explicados** ni alineados con la notación UML estándar, lo que impide alcanzar el nivel de 7/10.

## Puntuación
**Puntuación:** 3/10

## Observaciones
- **Corregir el campo "Operaciones":** Debe listar métodos reales con su firma o descripción funcional (ej. `crearRutaPredeterminada(origen, destino)`, `procesarDonación(monto)`, `registrarMantenimiento()`), eliminando las descripciones de cardinalidades y asociaciones.
- **Revisar la naturaleza de las clases:** La clase "Hacer ruta" debe eliminarse o renombrarse, ya que representa un caso de uso, no una entidad del modelo de dominio. Las relaciones deben modelarse mediante asociaciones en el diagrama, no como operaciones.
- **Separar atributos de relaciones:** Sustituir atributos que actúan como referencias externas por asociaciones explícitas en el diagrama de clases, manteniendo en el glosario solo atributos intrínsecos a la entidad.
- **Estandarizar la notación:** Utilizar una sintaxis clara para los métodos (nombre, parámetros, tipo de retorno) y asegurar que cada operación refleje una responsabilidad cohesiva de la clase según los principios de diseño orientado a objetos.