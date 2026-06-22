# Validació Comparativa: Agent vs Avaluador Humà

## Context Experimental

Per validar la fiabilitat del sistema Evaluaitor-Lamb, s'ha realitzat un experiment comparatiu utilitzant **12 memòries finals de pràctiques** d'un màster universitari, prèviament avaluades per una professora experta.

### Disseny Experimental

- **Conjunt de dades**: 12 memòries de pràctiques (4 Aprovat, 4 Notable, 4 Excel·lent)
- **Rúbrica**: 13 criteris d'avaluació amb 3 nivells (Insuficient 0-4, Correcte 5-7, Excel·lent 8-10)
- **Avaluador humà**: Professora experta (categoria qualitativa: Aprovat/Notable/Excel·lent)
- **Avaluador automàtic**: Evaluaitor-Lamb (nota quantitativa 0-10)

### Metodologia

1. **Generació de workflow reutilitzable**: S'ha creat un workflow únic per a totes les memòries
2. **Avaluació automàtica**: Cada memòria s'ha avaluat amb el mateix workflow
3. **Comparació**: S'han comparat les notes de l'agent amb les categories de la professora

## Resultats Preliminars

### Memòria 1: Memòria_FP_Aguayo_Morales (APROVAT)

| Aspecte | Resultat |
|---------|----------|
| **Categoria professora** | APROVAT |
| **Nota agent** | 8.0/10 (Bueno) |
| **Desviació** | +2.0 punts (sobre-evaluació) |

**Anàlisi**: L'agent ha assignat una nota significativament més alta que la categoria "Aprovat". Això suggereix una possible tendència a sobre-evaluar en comparació amb l'avaluador humà.

**Criteris millor puntuats** (9-10/10):
- Compliment, responsabilitat i dietari (10/10)
- Aportacions d'experiències (9/10)
- Capacitat d'observació i anàlisi (9/10)

**Criteris amb menor puntuació** (2-4/10):
- Perspectiva de gènere en STEM (2/10)
- Jornades o formació docent (4/10)

## Pròxims Passes

1. **Completar avaluació**: Avaluar les 11 memòries restants
2. **Anàlisi estadística**: Calcular desviació mitjana, correlació i biaixos
3. **Anàlisi per criteri**: Identificar criteris amb major discrepància
4. **Conclusions**: Determinar si l'agent és fiable com a eina d'assistència

---

*Última actualització: En curs (1/12 memòries avaluades)*
