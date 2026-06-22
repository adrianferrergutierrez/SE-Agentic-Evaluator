#!/bin/bash
# Script to run workflow with clean cache and detailed logging

echo "=========================================="
echo "🧹 Limpiando caché de Python..."
echo "=========================================="

cd /home/adrif/Evaluaitor-Lamb

# Clean all Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -name '*.pyc' -delete 2>/dev/null

echo "✓ Caché limpiada"

echo ""
echo "=========================================="
echo "🚀 Ejecutando workflow con logging..."
echo "=========================================="
echo ""

export PYTHONPATH=/home/adrif/Evaluaitor-Lamb

# Run with detailed logging output
python3 run_evaluation.py evaluate \
  --workflow tests/test-1-hito-2/output/workflow_hito2_vision.json \
  --input "tests/test-1-hito-2/A1.1 Memoria trabajo final (2).docx" \
  --output tests/test-1-hito-2/output/results_hotfix_final 2>&1 | tee /tmp/workflow_run.log

echo ""
echo "=========================================="
echo "📊 Resultados Resumidos"
echo "=========================================="
echo ""

echo "✓ Imágenes procesadas:"
grep -c "Processing:" /tmp/workflow_run.log || echo "N/A"

echo ""
echo "✓ Imágenes comprimidas:"
grep -c "compressed for API" /tmp/workflow_run.log || echo "N/A"

echo ""
echo "✓ Errores HTTP (antes de retry):"
grep "Attempt 1" /tmp/workflow_run.log | grep -c "Error" || echo "0"

echo ""
echo "✓ Reintentos realizados:"
grep -c "Retrying in" /tmp/workflow_run.log || echo "0"

echo ""
echo "✓ Descripciones finales:"
grep "descriptions added" /tmp/workflow_run.log || echo "N/A"

echo ""
echo "📝 Log completo: /tmp/workflow_run.log"
