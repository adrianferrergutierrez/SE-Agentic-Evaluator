# Documento de Requisitos - Sistema de E-Commerce

## 1. Objetivos del Proyecto

### OBJ-1
El sistema permitirá a los clientes realizar compras online de productos con un proceso de checkout simplificado en menos de 3 minutos.

### OBJ-2
El sistema gestionará el inventario de productos en tiempo real con actualización automática tras cada compra.

### OBJ-3
El sistema enviará confirmaciones de pedido por email y SMS en menos de 5 minutos tras la compra.

### OBJ-4
El sistema permitirá a los administradores generar informes de ventas semanales y mensuales.

---

## 2. Requisitos Funcionales

### IRQ-1
El sistema shall permitir a los usuarios buscar productos por nombre, categoría, precio y marca.
- **Objetivos asociados:** OBJ-1

### IRQ-2
El sistema shall gestionar un carrito de compra con capacidad mínima de 50 productos.
- **Objetivos asociados:** OBJ-1

### IRQ-3
El sistema shall procesar pagos con tarjeta de crédito/débito mediante pasarela segura (PCI-DSS).
- **Objetivos asociados:** OBJ-1

### IRQ-4
El sistema shall actualizar el inventario automáticamente tras cada compra completada.
- **Objetivos asociados:** OBJ-2

### IRQ-5
El sistema shall enviar email de confirmación con detalle del pedido y número de seguimiento.
- **Objetivos asociados:** OBJ-3

### IRQ-6
El sistema shall generar informes de ventas con filtros por fecha, categoría y producto.
- **Objetivos asociados:** OBJ-4

### IRQ-7
El sistema shall permitir registro de usuarios con validación de email.
- **Objetivos asociados:** OBJ-1

---

## 3. Requisitos No Funcionales

### NFR-1 (Rendimiento)
El sistema deberá soportar 500 usuarios concurrentes con tiempo de respuesta inferior a 2 segundos.

### NFR-2 (Seguridad)
Las contraseñas deberán almacenarse encriptadas con bcrypt y las comunicaciones usarán TLS 1.3.

### NFR-3 (Disponibilidad)
El sistema deberá estar disponible el 99.9% del tiempo (SLA) excepto en mantenimiento programado.

### NFR-4 (Escalabilidad)
El sistema deberá escalar horizontalmente para soportar picos de tráfico del 200% en campañas especiales.

### NFR-5 (Usabilidad)
La interfaz deberá ser responsive y accesible según WCAG 2.1 nivel AA.

---

## 4. Casos de Uso

### CU-001: Registrar Usuario
**Actor:** Cliente potencial  
**Precondición:** El usuario no tiene cuenta  
**Postcondición:** El usuario tiene cuenta activa  
**Flujo Principal:**
1. El usuario accede a formulario de registro
2. El sistema muestra campos: nombre, email, contraseña
3. El usuario completa el formulario
4. El sistema valida los datos
5. El sistema envía email de verificación
6. El usuario confirma el email
7. El sistema activa la cuenta

**Flujo Alternativo:**
- 4a. Si los datos son inválidos, el sistema muestra errores y vuelve al paso 2

**Excepciones:**
- E1: Email ya registrado → mostrar mensaje de error

---

### CU-002: Realizar Compra
**Actor:** Cliente registrado  
**Precondición:** El usuario está logueado y hay productos en el carrito  
**Postcondición:** Pedido creado y confirmación enviada  
**Flujo Principal:**
1. El usuario accede al carrito
2. El sistema muestra productos y total
3. El usuario inicia checkout
4. El sistema solicita dirección de envío
5. El usuario introduce dirección
6. El sistema calcula gastos de envío
7. El usuario selecciona método de pago
8. El sistema procesa el pago
9. El sistema confirma el pedido
10. El sistema envía confirmación por email/SMS

**Flujos Alternativos:**
- 8a. Pago rechazado → mostrar error y permitir otro método de pago
- 8b. Sin stock → informar y eliminar producto del carrito

**Excepciones:**
- E1: Error en pasarela de pago → cancelar pedido y notificar
- E2: Timeout de sesión → guardar carrito y redirigir a login

---

### CU-003: Gestionar Inventario
**Actor:** Administrador  
**Precondición:** El administrador está logueado  
**Postcondición:** Inventario actualizado  
**Flujo Principal:**
1. El administrador accede a gestión de inventario
2. El sistema muestra lista de productos con stock
3. El administrador selecciona producto
4. El sistema muestra detalle del producto
5. El administrador modifica cantidad
6. El sistema guarda cambios
7. El sistema registra la modificación en log

**Flujos Alternativos:**
- 3a. Añadir producto nuevo → formulario de alta

**Excepciones:**
- E1: Producto no encontrado → mostrar error

---

### CU-004: Generar Informe de Ventas
**Actor:** Administrador  
**Precondición:** El administrador está logueado  
**Postcondición:** Informe generado y descargado  
**Flujo Principal:**
1. El administrador accede a informes
2. El sistema muestra opciones de filtro
3. El administrador selecciona rango de fechas
4. El administrador selecciona filtros (categoría, producto)
5. El sistema genera el informe
6. El sistema muestra resultados en pantalla
7. El administrador descarga en PDF/Excel

**Flujos Alternativos:**
- 6a. Sin datos → mostrar mensaje informativo

**Excepciones:**
- E1: Error al generar → reintentar o notificar error

---

## 5. Diagramas

### Figura 1: Arquitectura del Sistema

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Cliente   │────▶│  Load Balancer│────▶│  Web Server │
│  (Browser)  │     │   (NGINX)    │     │   (Node.js) │
└─────────────┘     └──────────────┘     └─────────────┘
                                                  │
                    ┌─────────────┐              │
                    │   Email     │◀─────────────┤
                    │   Service   │              │
                    └─────────────┘              │
                                                  ▼
                    ┌─────────────┐     ┌─────────────┐
                    │  Payment    │◀───▶│  Database   │
                    │  Gateway    │     │  (PostgreSQL)│
                    └─────────────┘     └─────────────┘
```

### Figura 2: Diagrama de Casos de Uso

```
                    ┌─────────────────────────────────┐
                    │      Sistema E-Commerce         │
                    │                                 │
┌──────────┐        │  ┌─────────┐  ┌─────────────┐  │
│ Cliente  │───────▶│  │ Registrar│  │Realizar     │  │
└──────────┘        │  │ Usuario │  │  Compra     │  │
                    │  └─────────┘  └─────────────┘  │
                    │                                 │
┌──────────┐        │  ┌─────────┐  ┌─────────────┐  │
│Administr.│───────▶│  │Gestionar│  │  Generar    │  │
└──────────┘        │  │Inventario│ │  Informes   │  │
                    │  └─────────┘  └─────────────┘  │
                    └─────────────────────────────────┘
```

---

## 6. Matriz de Trazabilidad

| Objetivo | IRQ-1 | IRQ-2 | IRQ-3 | IRQ-4 | IRQ-5 | IRQ-6 | IRQ-7 | NFR-1 | NFR-2 | NFR-3 | NFR-4 | NFR-5 |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| OBJ-1    |   ✓   |   ✓   |   ✓   |       |       |       |   ✓   |   ✓   |   ✓   |       |       |   ✓   |
| OBJ-2    |       |       |       |   ✓   |       |       |       |   ✓   |       |   ✓   |   ✓   |       |
| OBJ-3    |       |       |       |       |   ✓   |       |       |   ✓   |       |   ✓   |       |       |
| OBJ-4    |       |       |       |       |       |   ✓   |       |   ✓   |       |       |   ✓   |       |

---

## 7. Glosario

| Término | Definición |
|---------|------------|
| Checkout | Proceso de finalización de compra |
| PCI-DSS | Estándar de seguridad para pagos con tarjeta |
| SLA | Acuerdo de nivel de servicio |
| TLS | Protocolo de seguridad para comunicaciones |
| WCAG | Pautas de accesibilidad para contenido web |