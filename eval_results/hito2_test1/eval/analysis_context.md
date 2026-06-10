### Objetivos Extraídos

# Objetivos del Proyecto

## OBJ-001: Rutas sostenibles
**Descripción:** La aplicación permitirá al usuario registrar todas sus rutas que sean beneficiosas para el medio ambiente, entre ellas el uso de transporte público (autobús, tren), caminar, utilizar bicicletas, patinete, entre otros. Permitirá registrarlas de varias maneras: rutas predeterminadas o no predeterminadas. Rutas predeterminadas: Son aquellas que el usuario tenga ya registradas, como puede ser ir al trabajo, a la universidad o al supermercado. Rutas no predeterminadas: Son rutas espontáneas, como puede ser salir a correr, salir a dar una vuelta con amigos o pasear. Se hace cuenta del tiempo total de estas rutas y al llegar a cierto objetivo, se planta un árbol en nombre del usuario.

## OBJ-002: Plantación de árboles
**Descripción:** A través de la donación de los usuarios a la aplicación, diversas empresas de reforestación que estén de voluntarios en el proyecto utilizaran los fondos para plantar árboles en zonas preasignadas. De esta manera se contribuye activamente al cuidado y recuperación del ecosistema.

## OBJ-003: Competencia amistosa
**Descripción:** La aplicación también fomentará la interacción entre usuarios. Estos podrán añadir amigos, y compartir con ellos sus logros y árboles que han ayudado a plantar. Este intercambio refuerza la motivación de los usuarios y su compromiso con el medio ambiente.

## OBJ-004: Promover la actividad física
**Descripción:** Buscamos fomentar la actividad física incentivando a las personas a moverse más mediante el uso de la aplicación. Los usuarios serán motivados a través de recompensas relacionadas con la plantación y la interacción con amigos. De esta manera se fomenta el interés por la actividad física.

### Requisitos Extraídos

# Requisitos del Sistema

## Requisitos de Información

### IRQ-001: Usuario
- **Descripción:** El sistema deberá permitir al usuario: Registrarse, si no tiene una cuenta: deberá almacenar la información correspondiente al registro del usuario. En concreto: los datos personales del usuario. Iniciar sesión, si ya tiene una cuenta registrada: para ello requerirá ciertos datos. En concreto: el nombre de usuario y la contraseña. Tener amistades, para lo que tendrá un buscador para poder encontrar a sus amigos y establecer amistades entre los usuarios. Deberá almacenar el nombre de usuario de estos.
- **Objetivos asociados:** OBJ-001, OBJ-002, OBJ-003, OBJ-004
- **Datos específicos:** Nombre, Apellidos, Edad, Correo electrónico/número de teléfono, Contraseña, Nombre de usuario, Nombre de usuario de las amistades
- **Tiempo de vida:**
  - Medio: <tiempo medio de vida>
  - Máximo: <tiempo máximo de vida>
- **Ocurrencias:**
  - Medio: <nº medio de ocurr. simult.>
  - Máximo: <nº máximo de ocurr. simult.>
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### IRQ-002: Ruta nueva
- **Descripción:** El sistema deberá permitir al usuario inicializar y finalizar nuevas rutas, para ello requerirá cierta información sobre ella.
- **Objetivos asociados:** OBJ-001
- **Datos específicos:** Ubicación de origen y destino, Tipo de ruta, Método de transporte (caminar, bicicleta, patinete, autobús y metro)
- **Tiempo de vida:**
  - Medio: <tiempo medio de vida>
  - Máximo: <tiempo máximo de vida>
- **Ocurrencias:**
  - Medio: <nº medio de ocurr. simult.>
  - Máximo: <nº máximo de ocurr. simult.>
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### IRQ-003: Ruta predeterminada
- **Descripción:** El sistema deberá permitir al usuario establecer una ruta predeterminada, para ello guardará los datos obtenidos al crear una ruta y los guardará como una ruta predeterminada bajo un nombre.
- **Objetivos asociados:** OBJ-001
- **Datos específicos:** Nombre de la ruta, Ubicación de origen y destino, Tipo de ruta, Método de transporte (caminar, bicicleta, patinete, autobús y metro)
- **Tiempo de vida:**
  - Medio: <tiempo medio de vida>
  - Máximo: <tiempo máximo de vida>
- **Ocurrencias:**
  - Medio: <nº medio de ocurr. simult.>
  - Máximo: <nº máximo de ocurr. simult.>
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### IRQ-004: Objetivos
- **Descripción:** El sistema deberá permitir al usuario crear objetivos y ver los detalles de los objetivos establecidos por el sistema, este guardará los siguientes datos respecto a los objetivos:
- **Objetivos asociados:** OBJ-003, OBJ-004
- **Datos específicos:** Nombre del objetivo, Descripción del objetivo, Estado del objetivo (booleano)
- **Tiempo de vida:**
  - Medio: <tiempo medio de vida>
  - Máximo: <tiempo máximo de vida>
- **Ocurrencias:**
  - Medio: <nº medio de ocurr. simult.>
  - Máximo: <nº máximo de ocurr. simult.>
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### IRQ-005: Historial de objetivos
- **Descripción:** El sistema deberá mostrar la información correspondiente a los objetivos y los logros, ya sean creados por el usuario o establecidos por el sistema. En concreto:
- **Objetivos asociados:** OBJ-004
- **Datos específicos:** Nombre del objetivo, Descripción del objetivo, Estado del objetivo
- **Tiempo de vida:**
  - Medio: <tiempo medio de vida>
  - Máximo: <tiempo máximo de vida>
- **Ocurrencias:**
  - Medio: <nº medio de ocurr. simult.>
  - Máximo: <nº máximo de ocurr. simult.>
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### IRQ-006: Compartir logros
- **Descripción:** El sistema deberá permitir al usuario compartir con sus amigos los logros alcanzados.
- **Objetivos asociados:** OBJ-003, OBJ-004
- **Datos específicos:** Nombre del logro, Descripción del logro
- **Tiempo de vida:**
  - Medio: <tiempo medio de vida>
  - Máximo: <tiempo máximo de vida>
- **Ocurrencias:**
  - Medio: <nº medio de ocurr. simult.>
  - Máximo: <nº máximo de ocurr. simult.>
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### IRQ-007: Donación
- **Descripción:** Los usuarios podrán realizar donaciones para contribuir con la aplicación y favorecer la plantación de árboles.
- **Objetivos asociados:** OBJ-002
- **Datos específicos:** Cantidad a abonar, Método de pago, Datos necesarios para el pago
- **Tiempo de vida:**
  - Medio: <tiempo medio de vida>
  - Máximo: <tiempo máximo de vida>
- **Ocurrencias:**
  - Medio: <nº medio de ocurr. simult.>
  - Máximo: <nº máximo de ocurr. simult.>
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### IRQ-008: Empresa
- **Descripción:** Los usuarios trabajadores del sistema de plantación o de la aplicación podrán registrarse e iniciar sesión con un rol distinto. Para ello el sistema deberá almacenar los datos personales necesarios para ello. La empresa que haya iniciado sesión en el sistema podrá recibir las peticiones de plantación de los usuarios y registrar su proceso. El sistema almacenará esta información.
- **Objetivos asociados:** OBJ-002
- **Datos específicos:** Nombre, Apellidos, Edad, Correo electrónico/número de teléfono, Contraseña, Nombre del usuario solicitante, Información de registro del árbol
- **Tiempo de vida:**
  - Medio: <tiempo medio de vida>
  - Máximo: <tiempo máximo de vida>
- **Ocurrencias:**
  - Medio: <nº medio de ocurr. simult.>
  - Máximo: <nº máximo de ocurr. simult.>
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

## Requisitos No Funcionales

### NFR-001: Seguridad de los datos
- **Descripción:** El sistema deberá asegurar que la información que se pide al iniciar sesión está totalmente encriptada y sigue patrones de alta seguridad, y que la autenticación es segura para los usuarios registrados.
- **Objetivos asociados:** OBJ-001, OBJ-002, OBJ-003
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### NFR-002: Interfaz sencilla e intuitiva
- **Descripción:** El sistema deberá mostrar una interfaz sencilla e intuitiva durante cualquier tipo de uso de la aplicación, con gráficos con la suficiente calidad.
- **Objetivos asociados:** OBJ-001, OBJ-003
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### NFR-003: Plazo de plantación
- **Descripción:** Cuando un usuario consigue plantar un árbol, la plantación real del árbol debe ocurrir en el plazo de un mes.
- **Objetivos asociados:** OBJ-002
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### NFR-004: Leyes del país donde se realice la plantación
- **Descripción:** La plantación de árboles debe estar regulada cumpliendo todas las leyes que deba.
- **Objetivos asociados:** OBJ-002
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### NFR-005: Aplicación móvil
- **Descripción:** La aplicación será móvil y estará disponible para los sistemas operativos más utilizados (Android, iOS).
- **Objetivos asociados:** OBJ-001, OBJ-002, OBJ-004
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### NFR-006: Contestación del sistema
- **Descripción:** El sistema deberá responder a la mayoría de interacciones en un plazo menor a dos segundos.
- **Objetivos asociados:** OBJ-001, OBJ-002, OBJ-003, OBJ-004
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### NFR-007: Actualización del código
- **Descripción:** El código debe estar documentado para facilitar futuras mejoras.
- **Objetivos asociados:** OBJ-001, OBJ-003, OBJ-004
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### NFR-008: Uso de buenas prácticas de desarrollo
- **Descripción:** El sistema utilizará buenas prácticas de desarrollo (arquitectura modular, pruebas automatizadas).
- **Objetivos asociados:** OBJ-001, OBJ-003
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### NFR-009: Prevención de caídas
- **Descripción:** Uso de servidores redundantes para evitar caídas del sistema.
- **Objetivos asociados:** OBJ-001, OBJ-002, OBJ-003, OBJ-004
- **Importancia:** <importancia del requisito>
- **Urgencia:** <urgencia del requisito>
- **Estado:** <estado del requisito>
- **Estabilidad:** <estabilidad del requisito>

### Casos de Uso Extraídos

# Casos de Uso del Sistema

## CU-001: Iniciar sesión/registrarse
- **Actores:** Usuario
- **Objetivos asociados:** OBJ-001
- **Requisitos asociados:** IRQ-001, NFR-001
- **Descripción:** Los usuarios podrán iniciar sesión con su cuenta y/o registrarse una vez descargada la aplicación.
- **Precondición:** Tener la aplicación descargada en el móvil
- **Postcondición:** El usuario accede a su cuenta

### Flujo Normal:
1. **p1:** El usuario selecciona iniciar sesión
2. **p2:** El sistema debe solicitar el usuario y contraseña
3. **p3:** El usuario introduce los datos solicitados
4. **p4:** El sistema verifica los datos
5. **p5:** Si el usuario no existe en el sistema entonces el sistema debe solicitar los datos necesarios para la creación de la cuenta
6. **p6:** El sistema comprueba los datos
7. **p7:** Si el usuario ha introducido los datos que se requieren correctamente, hay una creación de cuenta exitosa
8. **p8:** En caso de datos correctos, el sistema debe acceder a la cuenta del usuario y el caso de uso finaliza

### Excepciones:
- **En paso p4:** Si el usuario intenta registrarse con una cuenta ya iniciada, le dara error y solicitará otra
- **En paso p6:** Si el usuario no ha introducido los datos requeridos correctamente indicar qué datos son incorrectos o faltan, y no hay creación de cuenta aún.
- **En paso p6:** Si el usuario existe en el sistema y los datos son correctos entonces se salta al paso 8

## CU-002: Hacer ruta
- **Actores:** Usuario, GPS
- **Objetivos asociados:** OBJ-001
- **Requisitos asociados:** IRQ-002, IRQ-003, NFR-001
- **Descripción:** Al elegir la opción de "Hacer ruta", el usuario podrá seleccionar el método de transporte sostenible que utilizará (caminar, bicicleta, patinete, transporte público, etc.) y registrar la información del punto de inicio y destino. Además, podrá establecer rutas predeterminadas para facilitar su uso en futuras ocasiones. Al finalizar la ruta, el sistema la registrará y actualizará el progreso del usuario en la aplicación.
- **Precondición:** Estar registrado con una cuenta y tener el gps activado
- **Postcondición:** El sistema actualiza el historial de rutas y logros del usuario.

### Flujo Normal:
1. **p1:** El usuario elige la opción de “Hacer ruta”
2. **p2:** El usuario elige el método de transporte sostenible que utilizará
3. **p3:** El usuario puede elegir una ruta predeterminada si tiene, o comenzar una ruta nueva
4. **p4:** El usuario ingresa el punto de inicio y el destino
5. **p5:** El usuario inicia la ruta
6. **p6:** El sistema comienza a registrar el recorrido
7. **p7:** Una vez completada la ruta, el sistema la detecta automáticamente
8. **p8:** El sistema registra la distancia recorrida y el tiempo empleado
9. **p9:** Si el usuario ha alcanzado un objetivo de distancia o tiempo acumulado, el sistema le asigna una recompensa
10. **p10:** La ruta queda guardada en el historial del usuario y puede ser marcada como predeterminada si el usuario lo desea

### Excepciones:
- **En paso p3:** Si el usuario elige una ruta predeterminada, entonces se salta al paso 5
- **En paso p6:** Si el usuario finaliza la ruta manualmente, entonces se salta al paso 7
- **En paso p1:** Si el usuario elige una ruta predeterminada y no la termina, es decir la finaliza antes o después, esta se tomará por el sistema como una ruta no predeterminada para contar la distancia y tiempo y asignar su respectiva recompensa.

## CU-003: Ver logros/objetivos
- **Actores:** Usuario
- **Objetivos asociados:** OBJ-001
- **Requisitos asociados:** IRQ-004, IRQ-005, IRQ-006
- **Descripción:** Los usuarios pueden ver los logros y objetivos alcanzados en la aplicación como árboles plantados o metas completadas.
- **Precondición:** Tener una cuenta en la aplicación
- **Postcondición:** Los usuarios han accedido a un resumen de sus logros y objetivos actualizados

### Flujo Normal:
1. **p1:** Seleccionar la opción de logros y objetivos
2. **p2:** La aplicación muestra en pantalla un resumen de logros conseguidos con relación a las recompensas conseguidas por cada ruta y futuros objetivos, como árboles plantados, kilómetros recorridos o número de rutas realizadas
3. **p3:** El usuario puede seleccionar cualquiera de estas opciones para ver detalles más específicos
4. **p4:** El sistema le muestra los detalles del dato elegido
5. **p5:** El usuario tiene la opción de compartir sus logros
6. **p6:** El usuario tiene la opción de añadir objetivos propios, selecciona “configurar objetivos” y lo personaliza
7. **p7:** La aplicación guarda automáticamente los cambios realizados

### Excepciones:
- **En paso p1:** Si la aplicación no puede añadir un objetivo propio, salta mensaje de error y la aplicación queda como estaba

## CU-004: Configurar objetivos
- **Actores:** Usuario
- **Objetivos asociados:** OBJ-001, OBJ-003, OBJ-004
- **Requisitos asociados:** IRQ-004, IRQ-005, IRQ-006
- **Descripción:** Los usuarios pueden configurar objetivos en la aplicación
- **Precondición:** Tener una cuenta en la aplicación
- **Postcondición:** Los usuarios han accedido a un resumen de sus objetivos por alcanzar

### Flujo Normal:
1. **p1:** Seleccionar la opción de crear objetivos
2. **p2:** La aplicación le pide al usuario que ingrese el número objetivo de árboles plantados/kilómetros/tiempo de ruta que desea llegar a alcanzar
3. **p3:** El sistema le muestra los detalles del objetivo creado
4. **p4:** La aplicación guarda automáticamente los cambios realizados
5. **p5:** La aplicación marcará como alcanzado el objetivo una vez el usuario lo complete

### Excepciones:
- **En paso p2:** Si la aplicación no puede añadir un objetivo propio, salta mensaje de error y la aplicación queda como estaba

## CU-005: Competir con amigos
- **Actores:** Usuario
- **Objetivos asociados:** OBJ-003
- **Requisitos asociados:** IRQ-006
- **Descripción:** Los usuarios pueden añadir amigos con los que automáticamente se comparten los objetivos alcanzados
- **Precondición:** Tener una cuenta en la aplicación
- **Postcondición:** El usuario interactúa y se motiva con los logros de sus amigos, pudiendo acceder al progreso de cada uno

### Flujo Normal:
1. **p1:** El usuario selecciona la opción de “amigos” en la aplicación
2. **p2:** Si quiere añadir a un amigo, selecciona la opción e introduce el nombre con el que está registrado su amigo, le aparecerá la opción de “seguir”
3. **p3:** El sistema lo añade a su lista de amigos
4. **p4:** El usuario puede ver una tabla en la que aparecen sus amigos y los principales logros de cada uno
5. **p5:** El sistema se encarga de actualizar en tiempo real las estadísticas de cada uno en el tablero de amigos según los usuarios van avanzando

### Excepciones:
- **En paso p2:** Si el usuario no encuentra al amigo en la base de datos, el sistema le da la opción de invitación a la aplicación
- **En paso p4:** Si la tabla de amigos no se sincroniza correctamente, el sistema lanza mensaje de error

## CU-006: Hacer donación
- **Actores:** Usuario, Cuenta Bancaria
- **Objetivos asociados:** OBJ-002
- **Requisitos asociados:** IRQ-007
- **Descripción:** Los usuarios podrán hacer donaciones monetarias que contribuyan al financiamiento de la aplicación.
- **Precondición:** Estar registrado en la aplicación
- **Postcondición:** El usuario tiene una donación adicional en el historial de donaciones

### Flujo Normal:
1. **p1:** El usuario elige la opción de donaciones
2. **p2:** El usuario indica el monto de donación
3. **p3:** El usuario selecciona el método de pago disponible
4. **p4:** El usuario realiza el pago
5. **p5:** El sistema procesa el pago y genera una comprobación de pago
6. **p6:** El sistema actualiza el historial de donaciones del usuario
7. **p7:** El usuario recibe una notificación de donación

### Excepciones:
- **En paso p5:** El usuario ingresa un método de pago inválido, por lo que no se realiza la donación y el caso de uso finaliza

## CU-007: Iniciar sesión empresa
- **Actores:** Personal de árboles
- **Objetivos asociados:** OBJ-002
- **Requisitos asociados:** IRQ-001, IRQ-008, NFR-001
- **Descripción:** Para registrar los árboles plantados las empresas deben iniciar sesión
- **Precondición:** Tener la aplicación descargada en el móvil
- **Postcondición:** El personal de las empresas de árboles accede a su cuenta para registrar los árboles

### Flujo Normal:
1. **p1:** Personal de empresa inicia sesión en la aplicación con usuario empresarial
2. **p2:** El sistema verifica los datos
3. **p4:** En caso de datos correctos acceder a la cuenta

### Excepciones:
- **En paso p1:** El personal ingresa los datos incorrectos por lo que no puede acceder a su cuenta
- **En paso p2:** En caso de datos incorrectos volverlos a pedir

## CU-008: Plantar
- **Actores:** Personal de árboles
- **Objetivos asociados:** OBJ-002
- **Requisitos asociados:** IRQ-008, NFR-003, NFR-004
- **Descripción:** Las empresas de plantación voluntarias en la iniciativa recibirán notificaciones de los árboles a plantar asignados a su empresa, gestionando su participación.
- **Precondición:** Tener una cuenta registrada en la aplicación y estar inscrito como empresa voluntaria
- **Postcondición:** La empresa debe iniciar la actividad de plantar los árboles

### Flujo Normal:
1. **p1:** El sistema muestra la cuenta de árboles a plantar contados durante la semana
2. **p2:** La empresa voluntaria selecciona que quiere ser el que plante los árboles
3. **p3:** El sistema asigna ubicación para la plantación
4. **p4:** El sistema actualiza el estado de los árboles a plantar como “en proceso”

### Excepciones:
- **En paso p2:** Si la ubicación asignada no es válida, el sistema asigna otra

## CU-009: Mantenimiento de árboles
- **Actores:** Personal de árboles
- **Objetivos asociados:** OBJ-002
- **Requisitos asociados:** IRQ-008, NFR-004
- **Descripción:** La empresa voluntaria de plantar los árboles, queda a cargo de su mantenimiento regular; riego, revisión de su estado, o notificación de cualquier problema al sistema.
- **Precondición:** La empresa debe de haber plantado los árboles asignados
- **Postcondición:** El estado de la zona de árboles queda actualizado

### Flujo Normal:
1. **p1:** El sistema muestra qué zona árboles plantados necesita mantenimiento
2. **p3:** La empresa registra en el sistema la zona de árboles como “mantenido”
3. **p4:** El sistema actualiza el estado de la zona de árboles planteados y el caso de uso finaliza

### Excepciones:
- **En paso p3:** Si se presenta problemas como enfermedad o plagas, se notifica al sistema y este adapta futuros mantenimientos en base a esto

## CU-010: Registrar árboles
- **Actores:** Personal de árboles
- **Objetivos asociados:** OBJ-002
- **Requisitos asociados:** IRQ-008
- **Descripción:** Una vez las empresas voluntarias hayan realizado la plantación de árboles, esto deben ser registrados en el sistema para actualizar el proceso
- **Precondición:** Tener la aplicación descargada en el móvil
- **Postcondición:** Los árboles quedan registrados en el sistema y se refleja en la aplicación

### Flujo Normal:
1. **p1:** Selecciona la opción de "Registrar árboles plantados"
2. **p2:** Ingresa los detalles de la plantación, es decir evidencia
3. **p3:** Confirma la información ingresada.
4. **p4:** El sistema verifica y registra los árboles como plantados.
5. **p5:** Los árboles registrados aparecen reflejados en la cuenta del usuario y en el historial general de la aplicación

### Excepciones:
- **En paso p1:** La empresa no ingresa una evidencia válida de que los árboles han sido plantados

## CU-011: Gestionar usuarios
- **Actores:** Administrador técnico
- **Objetivos asociados:** OBJ-003
- **Requisitos asociados:** IRQ-001, IRQ-008
- **Descripción:** El administrador técnico puede gestionar los usuarios de la aplicación, pudiendo activar, desactivar y modificar cuentas.
- **Precondición:** Tener permisos de administrador técnico
- **Postcondición:** Los cambios en la cuenta del usuario quedan registrados en el sistema

### Flujo Normal:
1. **p1:** Seleccionar la opción de gestionar usuarios
2. **p2:** Seleccionar usuario a gestionar
3. **p3:** Elegir la acción a realizar (activar cuenta, desactivar cuenta, modificar cuenta)
4. **p4:** Confirmar la acción realizada

### Excepciones:
- **En paso p1:** Si se intenta modificar un usuario sin los permisos necesarios, se notifica al administrador
- **En paso p2:** Si los datos ingresados para modificar un usuario no son válidos, se solicitan de nuevo

## CU-012: Activar usuarios
- **Actores:** Administrador técnico
- **Objetivos asociados:** OBJ-003
- **Requisitos asociados:** IRQ-001, IRQ-008
- **Descripción:** El administrador técnico puede gestionar los usuarios de la aplicación, pudiendo activar, desactivar y modificar cuentas.
- **Precondición:** Tener permisos de administrador técnico y haber seleccionado activar usuario
- **Postcondición:** Los cambios en la cuenta del usuario quedan registrados en el sistema

### Flujo Normal:
1. **p1:** Activar cuenta
2. **p2:** Mensaje de cuenta activada

### Excepciones:
- **En paso p1:** Si se intenta activar una cuenta ya activa se enviará un mensaje diciendo que la cuenta seleccionada ya está activa

## CU-013: Desactivar usuarios
- **Actores:** Administrador técnico
- **Objetivos asociados:** OBJ-003
- **Requisitos asociados:** IRQ-001, IRQ-008
- **Descripción:** El administrador técnico puede gestionar los usuarios de la aplicación, pudiendo activar, desactivar y modificar cuentas.
- **Precondición:** Tener permisos de administrador técnico
- **Postcondición:** Los cambios en la cuenta del usuario quedan registrados en el sistema

### Flujo Normal:
1. **p1:** Desactivar usuario
2. **p2:** Mensaje de cuenta desactivada

### Excepciones:
- **En paso p1:** Si intenta desactivar una cuenta ya inactiva, el sistema enviará un mensaje de error

## CU-014: Modificar usuarios
- **Actores:** Administrador técnico
- **Objetivos asociados:** OBJ-003
- **Requisitos asociados:** IRQ-001, IRQ-008
- **Descripción:** El administrador técnico puede gestionar los usuarios de la aplicación, pudiendo activar, desactivar y modificar cuentas.
- **Precondición:** Tener permisos de administrador técnico
- **Postcondición:** Los cambios en la cuenta del usuario quedan registrados en el sistema

### Flujo Normal:
1. **p1:** Modificar usuario
2. **p2:** Ingresar los nuevos datos
3. **p4:** Confirmar la acción realizada

### Excepciones:
- **En paso p1:** Si los datos ingresados para modificar un usuario no son válidos, se solicitan de nuevo

## CU-015: Gestionar pagos
- **Actores:** Administrador de gestión
- **Objetivos asociados:** OBJ-002
- **Requisitos asociados:** IRQ-008
- **Descripción:** El administrador de gestión podrá supervisar, gestionar y revisar los pagos y donaciones realizados por los usuarios.
- **Precondición:** Tener permisos de administrador de gestión
- **Postcondición:** Los pagos y donaciones quedan registrados y validados en el sistema

### Flujo Normal:
1. **p1:** Seleccionar la opción de gestión de pagos
2. **p2:** Revisar los pagos y donaciones realizados
3. **p3:** Validar estos pagos y donaciones
4. **p4:** Confirmar el buen uso de estos fondos

### Excepciones:
- **En paso p1:** Si el pago o donación no se ha validado correctamente, se solicita al usuario corregir o repetir el proceso de donación

---

## Resumen
- **Diagramas detectados:** Sí
- **Actores identificados:** Usuario, Personal de árboles, Administrador técnico, Administrador de gestión, GPS, Cuenta Bancaria

### Detección de Huérfanos

# Orphan Detection Report

## Summary
- **Total objectives declared:** 4
- **Total requirements:** 17
- **Orphan requirements (no objective):** 0
- **Orphan objectives (no requirements):** 0
- **Undeclared objectives (referenced but not defined):** 0

## Orphan Requirements

✅ None found – all requirements link to at least one objective.

## Orphan Objectives

✅ None found – all objectives are covered by at least one requirement.

## Objective Coverage
- ✅ **OBJ-001**: IRQ-001, IRQ-002, IRQ-003, NFR-001, NFR-002, NFR-005, NFR-006, NFR-007, NFR-008, NFR-009
- ✅ **OBJ-002**: IRQ-001, IRQ-007, IRQ-008, NFR-001, NFR-003, NFR-004, NFR-005, NFR-006, NFR-009
- ✅ **OBJ-003**: IRQ-001, IRQ-004, IRQ-006, NFR-001, NFR-002, NFR-006, NFR-007, NFR-008, NFR-009
- ✅ **OBJ-004**: IRQ-001, IRQ-004, IRQ-005, IRQ-006, NFR-005, NFR-006, NFR-007, NFR-009


### Evaluación SMART

# SMART Objectives Evaluation

**Total objectives evaluated:** 4
- ✅ Fully SMART (5/5): 0
- ⚠️ Partially SMART (1–4/5): 1
- ❌ Not SMART (0/5): 3

## Per-Objective Results

**OBJ-001** (Not SMART – 1/5)
  ❌ S (Specific) | ❌ M (Measurable) | ❌ A (Achievable) | ❌ R (Relevant) | ✅ T (Time-bound)
  Notes: No se detectaron métricas medibles. Añade KPIs, porcentajes u otras magnitudes cuantificables.
  El objetivo puede ser demasiado vago. Añade alcance y restricciones específicas.

**OBJ-002** (Not SMART – 0/5)
  ❌ S (Specific) | ❌ M (Measurable) | ❌ A (Achievable) | ❌ R (Relevant) | ❌ T (Time-bound)
  Notes: No se detectaron métricas medibles. Añade KPIs, porcentajes u otras magnitudes cuantificables.
  Sin indicadores temporales. Añade un plazo concreto o un hito de referencia.
  El objetivo puede ser demasiado vago. Añade alcance y restricciones específicas.

**OBJ-003** (Not SMART – 0/5)
  ❌ S (Specific) | ❌ M (Measurable) | ❌ A (Achievable) | ❌ R (Relevant) | ❌ T (Time-bound)
  Notes: No se detectaron métricas medibles. Añade KPIs, porcentajes u otras magnitudes cuantificables.
  Sin indicadores temporales. Añade un plazo concreto o un hito de referencia.
  El objetivo puede ser demasiado vago. Añade alcance y restricciones específicas.

**OBJ-004** (Not SMART – 0/5)
  ❌ S (Specific) | ❌ M (Measurable) | ❌ A (Achievable) | ❌ R (Relevant) | ❌ T (Time-bound)
  Notes: No se detectaron métricas medibles. Añade KPIs, porcentajes u otras magnitudes cuantificables.
  Sin indicadores temporales. Añade un plazo concreto o un hito de referencia.
  El objetivo puede ser demasiado vago. Añade alcance y restricciones específicas.



### Clasificación ISO/IEC 25010

# ISO/IEC 25010 NFR Classification Report

**Total NFRs analysed:** 9
**Unclassified NFRs:** 7

## Per-NFR Classification

- ✅ **NFR-001**: Security
- ✅ **NFR-002**: Usability
- ⚠️ **NFR-003**: *Unclassified* – no ISO/IEC 25010 characteristic matched. Consider adding measurable quality attributes.
- ⚠️ **NFR-004**: *Unclassified* – no ISO/IEC 25010 characteristic matched. Consider adding measurable quality attributes.
- ⚠️ **NFR-005**: *Unclassified* – no ISO/IEC 25010 characteristic matched. Consider adding measurable quality attributes.
- ⚠️ **NFR-006**: *Unclassified* – no ISO/IEC 25010 characteristic matched. Consider adding measurable quality attributes.
- ⚠️ **NFR-007**: *Unclassified* – no ISO/IEC 25010 characteristic matched. Consider adding measurable quality attributes.
- ⚠️ **NFR-008**: *Unclassified* – no ISO/IEC 25010 characteristic matched. Consider adding measurable quality attributes.
- ⚠️ **NFR-009**: *Unclassified* – no ISO/IEC 25010 characteristic matched. Consider adding measurable quality attributes.

## Coverage by ISO/IEC 25010 Characteristic

| Characteristic | NFRs Covering It |
|---|---|
| ❌ Functional Suitability | 0 |
| ❌ Performance Efficiency | 0 |
| ❌ Compatibility | 0 |
| ✅ Usability | 1 |
| ❌ Reliability | 0 |
| ✅ Security | 1 |
| ❌ Maintainability | 0 |
| ❌ Portability | 0 |

## ⚠️ Uncovered Characteristics

The following ISO/IEC 25010 characteristics have **no** associated NFR and should be considered:

- **Functional Suitability** (sub-characteristics: functional_completeness, functional_correctness, functional_appropriateness)
- **Performance Efficiency** (sub-characteristics: time_behaviour, resource_utilisation, capacity)
- **Compatibility** (sub-characteristics: co_existence, interoperability)
- **Reliability** (sub-characteristics: maturity, availability, fault_tolerance, recoverability)
- **Maintainability** (sub-characteristics: modularity, reusability, analysability, modifiability, testability)
- **Portability** (sub-characteristics: adaptability, installability, replaceability)
