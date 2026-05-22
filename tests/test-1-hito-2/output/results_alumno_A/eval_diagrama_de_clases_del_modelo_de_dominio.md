# Evaluación: Diagrama de clases del modelo de dominio

## Análisis
Tras revisar el apartado 12 (diagrama) y, principalmente, el **Glosario de clases (Tablas 43 a 53)**, se identifican deficiencias estructurales y conceptuales que impiden considerar el modelo como un diagrama de dominio válido según los estándares de UML y la ingeniería de software:

1. **Enfoque no conceptual:** Un modelo de dominio debe representar los conceptos del problema, no elementos de la interfaz, operaciones del sistema ni detalles de implementación. En el documento se observan múltiples violaciones a este principio:
   - `Hacer ruta` se define como una "opción" o acción, no como una entidad conceptual. Debería modelarse como `Ruta` o `RegistroDeRuta`.
   - Se incluyen atributos de implementación como `Contraseña` en `Empresa de plantación` o `Número de cuenta` en `Donaciones`, que pertenecen al diseño técnico o a la capa de persistencia/seguridad, no al dominio.
   - Se mencionan elementos de UI como `"botón" de inicio` o `"botón" para marcar completado` en las clases `Ruta no predeterminada` y `Objetivos`.
   - Las "operaciones" listadas son en realidad comandos del sistema o casos de uso (`Realizar donación`, `Ver objetivos`, `Plantar árbol`), no comportamientos intrínsecos del dominio.

2. **Uso incorrecto de la notación UML:** En el glosario, las **asociaciones entre clases se describen erróneamente dentro del apartado "Operaciones"**. Por ejemplo, en `Mantenimiento` se indica `Zona: Un mantenimiento en específico se realiza en una zona...` y en `Empresa de plantación` se listan `Árbol`, `Mantenimiento` y `Donación` como operaciones. En UML, estas son relaciones de asociación (con multiplicidad y roles), no métodos. Esta confusión indica una falta de comprensión de la sintaxis y semántica del diagrama de clases.

3. **Cobertura incompleta frente a los requisitos:** Aunque se cubren conceptos centrales (`Usuario`, `Ruta`, `Árbol`, `Empresa`, `Zona`), el modelo omite clases explícitas para conceptos recurrentes en los casos de uso y requisitos de información:
   - No existe una clase `Amistad` o `RelaciónSocial` para soportar el objetivo de "Competencia amistosa" y los casos de uso de compartir logros.
   - No se modela `Historial` o `Logro` como entidad independiente, a pesar de que los IRQ-005 e IRQ-006 los tratan como información persistente y diferenciada de los objetivos activos.
   - La clase `Árbol` contiene el atributo `Cantidad (Integer)`, lo que sugiere una agregación mal definida; conceptualmente, cada árbol debería ser una instancia, y la cantidad sería un atributo de una clase `ContadorDeÁrboles` o `ProgresoUsuario`.

4. **Aspectos positivos:** Se ha realizado un esfuerzo por identificar las entidades principales del negocio y se ha intentado documentar cada una en el glosario. La inclusión de `Tipo de transporte` como enumeración es acertada y la clase `Zona` (añadida tras corrección) aporta contexto geográfico necesario.

En conjunto, el modelo se aproxima más a un borrador de diseño de software mezclado con descripciones de casos de uso que a un **modelo de dominio conceptual**. La notación se utiliza de forma inconsistente y se priorizan detalles de implementación sobre la abstracción del problema.

## Puntuación
**Puntuación:** 2/10

## Observaciones
- **Separar dominio de solución:** Elimina atributos de implementación (`Contraseña`, `Número de cuenta`, referencias a "botones") y operaciones de sistema (`Ver objetivos`, `Realizar donación`). El modelo de dominio solo debe contener atributos conceptuales y, opcionalmente, comportamientos de negocio de alto nivel.
- **Corregir la notación UML:** Las relaciones entre clases deben representarse como **líneas de asociación** con multiplicidad (ej. `1..*`, `0..1`) y roles, nunca como operaciones. Revisa la diferencia entre atributos, operaciones y asociaciones en la especificación UML.
- **Refactorizar clases problemáticas:** 
  - Cambia `Hacer ruta` por `Ruta` (con subclases o atributo discriminador para predeterminada/no predeterminada).
  - Separa `Árbol` (instancia única) de `ProgresoUsuario` o `ContadorDeÁrboles`.
  - Modela explícitamente `Amistad`/`RedSocial` y `HistorialDeLogros` para cubrir los requisitos de competencia y compartición.
- **Validar con los casos de uso:** Cruza cada caso de uso y requisito de información con el diagrama. Si un concepto aparece repetidamente en los flujos de negocio, debe tener su clase o asociación correspondiente en el modelo de dominio.
- **Revisar el glosario:** Asegúrate de que cada tabla siga estrictamente la estructura: `Nombre`, `Descripción conceptual`, `Atributos` (solo datos del dominio), `Relaciones/Asociaciones` (con multiplicidad), y evita mezclar responsabilidades de la capa de aplicación.