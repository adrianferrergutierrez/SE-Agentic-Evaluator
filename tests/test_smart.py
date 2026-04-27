#!/usr/bin/env python3
"""Test para verificar las mejoras SMART"""

from core.analysis.smart import evaluate_objectives_smart, smart_summary_markdown

# Test con los objetivos del test2
objectives_text = """
## OBJ-1: Checkout simplificado
**Descripción:** El sistema permitirá a los clientes realizar compras online de productos con un proceso de checkout simplificado en menos de 3 minutos.

## OBJ-2: Gestión de inventario
**Descripción:** El sistema gestionará el inventario de productos en tiempo real con actualización automática tras cada compra.

## OBJ-3: Notificaciones automáticas
**Descripción:** El sistema enviará confirmaciones de pedido por email y SMS en menos de 5 minutos tras la compra.

## OBJ-4: Informes de ventas
**Descripción:** El sistema permitirá a los administradores generar informes de ventas semanales y mensuales.
"""

print("=" * 60)
print("PRUEBA DE MEJORAS SMART")
print("=" * 60)

scores = evaluate_objectives_smart(objectives_text)
print(smart_summary_markdown(scores))

# Mostrar resultados detallados
print("\n" + "=" * 60)
print("DETALLE POR OBJETIVO")
print("=" * 60)

for score in scores:
    print(f"\n{score.objective_id}:")
    print(f"  Specific:   {'✅' if score.specific else '❌'}")
    print(f"  Measurable: {'✅' if score.measurable else '❌'}")
    print(f"  Achievable: {'✅' if score.achievable else '❌'}")
    print(f"  Relevant:   {'✅' if score.relevant else '❌'}")
    print(f"  Time-bound: {'✅' if score.time_bound else '❌'}")
    print(f"  Puntuación: {score.score}/5")