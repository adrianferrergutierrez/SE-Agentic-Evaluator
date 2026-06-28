# Memòria del Sistema de Gestió de Biblioteques (SGB)

## 1. Introducció i Objectius (OBJ)
L'objectiu principal d'aquest projecte és desenvolupar un sistema informàtic per a gestionar els préstecs i usuaris de la biblioteca municipal.

- **OBJ-1:** El sistema ha de permetre registrar nous usuaris en menys de 2 minuts.
- **OBJ-2:** S'ha de reduir el temps d'espera per agafar un llibre en un 30% respecte al sistema manual antic.
- **OBJ-3:** El sistema ha d'estar disponible per a ser utilitzat des de navegadors web.

## 2. Requisits d'Informació (IRQ)
- **IRQ-1:** El sistema ha de guardar les següents dades d'un llibre: títol, autor, ISBN, any de publicació i estat (disponible o prestat).
- **IRQ-2:** El sistema ha de guardar dels usuaris: DNI, nom, cognoms i correu electrònic.

## 3. Requisits No Funcionals (NFR)
- **NFR-1 (Rendiment):** El sistema ha de respondre a les cerques de llibres en menys de 2 segons.
- **NFR-2 (Seguretat):** Totes les contrasenyes s'han de guardar xifrades utilitzant l'algorisme bcrypt.

## 4. Casos d'Ús (CU)
### CU-1: Prestar Llibre
**Actor principal:** Bibliotecari
**Descripció:** El bibliotecari introdueix el DNI de l'usuari i l'ISBN del llibre. El sistema comprova que el llibre està disponible i registra el préstec amb la data de devolució prevista (15 dies).

### CU-2: Cerca per Autor
**Actor principal:** Usuari
**Descripció:** L'usuari introdueix el nom d'un autor i el sistema retorna una llista amb tots els llibres d'aquest autor que pertanyen a la biblioteca.
