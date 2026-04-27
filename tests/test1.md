# Documento de Requisitos - Sistema de Gestión de Biblioteca

## 1. Objetivos

### OBJ-1
El sistema permitirá a los usuarios buscar libros por título, autor y categoría.

### OBJ-2
El sistema gestionará préstamos y devoluciones de libros con control de fechas.

### OBJ-3
El sistema enviará notificaciones automáticas de recordatorio antes del vencimiento.

## 2. Requisitos Funcionales

### IRQ-1
El sistema shall permitir búsqueda de libros en menos de 2 segundos.

### IRQ-2
El sistema shall registrar todos los préstamos con fecha y hora.

### IRQ-3
El sistema shall generar informes mensuales de actividad.

## 3. Requisitos No Funcionales

### NFR-1 (Rendimiento)
El sistema deberá soportar 100 usuarios concurrentes.

### NFR-2 (Seguridad)
Las contraseñas deberán almacenarse encriptadas con SHA-256.

## 4. Casos de Uso

### CU-001: Buscar Libro
**Actor:** Usuario
**Precondición:** El usuario está logueado
**Flujo:**
1. El usuario ingresa términos de búsqueda
2. El sistema muestra resultados coincidentes
3. El usuario selecciona un libro

### CU-002: Registrar Préstamo
**Actor:** Bibliotecario
**Precondición:** El libro está disponible
**Flujo:**
1. El bibliotecario escanea el libro
2. El sistema verifica disponibilidad
3. El sistema registra el préstamo