# Informe Final d'Avaluació - Escenari 6

## Resum Executiu

Aquest informe presenta l'avaluació del document "A1.1 Memoria trabajo final (2).docx" segons la rúbrica del Hito 2, utilitzant el sistema SE-Agentic-Evaluator amb anàlisi de diagrames mitjançant visió per computador.

**Nota Final Ponderada: 6.30/10**

## Resultats per Criteri

| Criteri | Pes | Puntuació | Contribució |
|---------|-----|-----------|-------------|
| memoria_tecnica | 25% | 7/10 | 1.75 |
| diagrama_de_clases_del_modelo_de_dominio | 65% | 7/10 | 4.55 |
| glosario_de_clases | 10% | 0/10 | 0.00 |
| **TOTAL** | **100%** | | **6.30/10** |

## Anàlisi Detallada per Criteri

### diagrama_de_clases_del_modelo_de_dominio

# Evaluación: Diagrama de clases del modelo de dominio

## Análisis
El diagrama de clases del modelo de dominio (Imagen 31) aplica correctamente la notación UML estándar: utiliza rectángulos con compartimentos para atributos, líneas de asociación con multiplicidades explícitas (`0..*`, `1`, etc.) y estereotipos adecuados (`<<enumeration>>`). Captura las entidades nucleares del dominio como `Usuario`, `Donación`, `Empresa de plantación`, `Árbol`, `Zona`, `Mantenimiento` y `Objetivos`, lo que evidencia una base conceptual sólida.

No obstante, el modelo presenta desviaciones conceptuales y omisiones respecto a la especificación de requisitos y casos de uso del documento:
- **Clases mal planteadas:** `Hacer ruta` se modela como una clase cuando, en el dominio, representa una acción o caso de uso. Debería ser una entidad conceptual como `Ruta` o `RegistroDeRuta`. Además, aparece una asociación con la clase `Computador` que no está definida en el diagrama.
- **Atributos conceptuales incorrectos:** `Zona` incluye `Habitantes: Float`, un dato irrelevante para la gestión de reforestación; `Árbol` incluye `Cantidad: Integer`, lo que confunde una instancia individual con un agregado o métrica.
- **Falta de cobertura de requisitos:** No se reflejan conceptos clave mencionados en los casos de uso y requisitos, como `Amigo`/`Competencia`, `Logro` (diferenciado explícitamente de `Objetivo` en los IRQ), `Empleado`/`Personal` (distinto de la entidad empresa) o `Transacción`/`Pago`.
- **Notación en asociaciones:** Las líneas de asociación utilizan verbos de acción (`Envía`, `Crear`, `Hacer ruta`) en lugar de nombres de roles o indicadores de navegabilidad estándar en UML.
- **Nivel de abstracción:** El glosario de clases (Tablas 43-53) añade operaciones detalladas, lo que acerca el modelo a un nivel de diseño técnico en lugar de mantenerlo estrictamente como un modelo de dominio conceptual (que debe centrarse en entidades, atributos y relaciones del mundo real).

En conjunto, la notación UML se ha utilizado bien, pero el diagrama no es del todo correcto conceptualmente y omite clases y relaciones derivadas directamente de la especificación de requisitos. Esto se ajusta al descriptor de 7/10 de la rúbrica.

## Puntuación
**Puntuación:** 7/10

## Observaciones
- Renombrar `Hacer ruta` a `Ruta` o `Trayecto` y eliminar la referencia a `Computador` o definirla si es estrictamente necesaria para el dominio.
- Corregir atributos conceptuales: `Zona` debería reflejar ubicación geográfica, coordenadas o hectáreas; `Árbol` debe representar una instancia única (eliminar `Cantidad` y moverlo a un agregado o métrica de usuario).
- Incorporar clases faltantes derivadas de los requisitos: `Amigo` (o relación de amistad), `Logro`, `Empleado` y `Transacción`/`Pago`.
- Sustituir los verbos en las asociaciones por nombres de roles estándar (ej. `donante`, `receptor`, `creador`) y añadir flechas de navegabilidad si corresponde.
- Mantener el diagrama estrictamente conceptual: reservar las operaciones y detalles de implementación para el modelo de diseño, no para el modelo de dominio.

---

### glosario_de_clases

# Avaluació: Glosario de clases

**Puntuación:** 0/10

---

### memoria_tecnica

# Evaluación: Memoria técnica

## Análisis
La sección **3. Memoria técnica** cumple con la estructura solicitada, presentando los **6 apartados exigidos**: Introducción general del trabajo (3.1), Objetivos (3.2), Técnicas y herramientas (3.3), Descripción del grupo de trabajo (3.4), Aspectos relevantes (3.5) y Conclusiones (3.6). En cuanto a la extensión, el documento supera ampliamente el mínimo de 5 páginas, con un desarrollo detallado y bien distribuido.

El contenido es coherente, reflexivo y muestra un seguimiento real del proceso de desarrollo. Se evidencia una organización clara del equipo, una justificación honesta del uso de herramientas (p. ej., el abandono de Trello en favor de Telegram por agilidad) y una identificación precisa de las dificultades técnicas encontradas (modelado de dominio, definición de casos de uso, matrices de rastreabilidad). La declaración del uso de IA generativa (Sección 2) es transparente y se ajusta a buenas prácticas académicas.

En el plano lingüístico, el texto está **escrito correctamente** en su mayoría, con una estructura lógica y vocabulario adecuado para un trabajo universitario. No obstante, se detectan algunas informalidades y leves imprecisiones gramaticales que no afectan la comprensión pero restan rigor académico:
- `"utilizaran"` → debería ser `"utilizarán"`.
- `"Se hace cuenta del tiempo total"` → expresión coloquial; lo adecuado sería `"Se contabiliza"` o `"Se lleva un registro"`.
- `"Nuestro principal método de trabajo ha sido llamarnos y repartirnos el trabajo"` → tono excesivamente informal para una memoria técnica.
- `"En primer lugar, se introduce de forma general que aborda nuestra aplicación"` → construcción sintáctica mejorable (`"lo que aborda"` o `"el enfoque de"`).

Estos detalles sitúan el documento en el nivel intermedio-alto de la rúbrica, cumpliendo todos los requisitos estructurales y de extensión, con una redacción correcta pero con margen de mejora en el registro formal.

## Puntuación
**Puntuación:** 7/10

## Observaciones
- **Formalizar el registro lingüístico**: Sustituir expresiones coloquiales por terminología técnica o académica (p. ej., `"llamarnos y repartirnos"` → `"coordinación mediante reuniones síncronas y distribución equitativa de tareas"`).
- **Revisión ortotipográfica y gramatical**: Corregir acentuación (`utilizarán`), concordancias y estructuras sintácticas ambiguas. Una lectura final enfocada en estilo académico elevaría significativamente la calidad.
- **Profundizar en la metodología**: Aunque se mencionan el Proceso Unificado y el método de Durán y Bernárdez, sería valioso explicitar brevemente cómo se aplicaron concretamente en la elicitación, priorización o validación de requisitos.
- **Consistencia en la nomenclatura**: Unificar el formato de los identificadores (p. ej., `OBJ-001` vs `OBJ-1`, `IRQ-001` vs `IRQ-1`) a lo largo de toda la memoria para evitar confusiones en la trazabilidad.

---

## Observacions Generals

### Punts Forts
- **Memoria tècnica (7/10)**: Bona documentació tècnica amb estructura clara
- **Diagrama de clases (7/10)**: Diagrama complet amb relacions ben definides
- **Processament d'imatges**: 25 de 26 imatges processades correctament amb visió per computador

### Àrees de Millora
- **Glosario de clases (0/10)**: El glosari no s'ha trobat o no compleix els requisits mínims
- **Imatge no processada**: 1 imatge va fallar per filtre de contingut inapropiat

### Recomanacions
1. Afegir un glosari de classes complet amb definicions clares
2. Revisar les imatges que van fallar el filtre de contingut
3. Millorar la coherència entre el diagrama de classes i el glosari

## Conclusió

El document presenta una bona base tècnica amb una nota final de **6.30/10**, principalment afectada per l'absència del glosari de classes. La memòria tècnica i el diagrama de classes mostren un bon nivell de qualitat.

---

*Informe generat automàticament per SE-Agentic-Evaluator*
