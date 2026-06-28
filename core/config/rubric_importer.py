#!/usr/bin/env python3
"""
core/config/rubric_importer.py
================================
Converts Markdown table rubrics into YAML config + prompt files.

Parses a rubric table like:
| Criterio | Insuficiente (0) | ... | Excelente (10) | Peso |
| **Objetivos** | ... | ... | ... | 8 % |

And generates:
1. A YAML config file compatible with ConfigManager.
2. Individual prompt files for each criterion with level descriptions.

Usage:
    python core/config/rubric_importer.py \
        --input tests/rubrica-hito-1.md \
        --output configs/rubric_hito1.yaml \
        --prompts-dir prompts/hito1/
"""

from __future__ import annotations

import argparse
import logging
import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Parsing logic
# ---------------------------------------------------------------------------

def _normalize_id(text: str) -> str:
    """Convert 'Diagrama de casos de uso' to 'diagrama_casos_de_uso'."""
    text = text.strip().strip("*").strip("_")
    # Remove accents
    text = "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )
    # Lowercase and replace spaces with underscores
    return re.sub(r"[^a-z0-9_]", "", text.lower().replace(" ", "_"))


def _parse_weight(weight_str: str) -> float:
    """Parse '8 %' or '0.08' into a float."""
    val = weight_str.replace("%", "").strip()
    try:
        f = float(val)
        if f > 1.0:
            return f / 100.0
        return f
    except ValueError:
        return 0.0


def parse_markdown_rubric(md_content: str) -> List[Dict]:
    """Parse a Markdown table into a list of criterion dicts.

    Returns
    -------
    list of dict
        Each dict has keys: name, id, levels (dict 0/4/7/10 -> text), weight.
    """
    lines = [l.strip() for l in md_content.strip().splitlines() if l.strip()]
    
    # Find the table header
    header_idx = -1
    for i, line in enumerate(lines):
        if line.startswith("|") and any(w in line.lower() for w in ["criterio", "criteri", "criterion"]):
            header_idx = i
            break

    if header_idx == -1:
        raise ValueError("No rubric table header found (looked for 'Criterio')")

    # Identify column indices
    header_parts = [p.strip() for p in lines[header_idx].split("|") if p.strip()]
    
    # Expected columns: Criterio, Level1, Level2, Level3, Level4, Peso
    # We need to find which columns correspond to levels and which to weight.
    # Usually: Criterio | ...levels... | Peso
    
    # Find Peso column index
    peso_idx = None
    for idx, part in enumerate(header_parts):
        if any(w in part.lower() for w in ["peso", "pes", "weight"]):
            peso_idx = idx
            break
    
    if peso_idx is None:
        raise ValueError("No 'Peso' column found in rubric table")

    # Level columns are between Criterio (0) and Peso
    level_indices = [i for i in range(1, len(header_parts)) if i != peso_idx]
    
    # Extract level scores from header (e.g. "Insuficiente (0)" -> 0)
    level_scores = []
    for idx in level_indices:
        match = re.search(r"\((\d+)\)", header_parts[idx])
        if match:
            level_scores.append(int(match.group(1)))
        else:
            level_scores.append(0) # Fallback

    criteria = []
    for line in lines[header_idx + 1:]:
        if not line.startswith("|"):
            continue
        
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 2:
            continue

        name_raw = parts[0]
        # Skip separator rows like |---|---|
        if re.match(r"^[-:| ]+$", name_raw):
            continue
            
        name = name_raw.strip("*").strip("_")
        if not name or name == "---":
            continue

        criterion_id = _normalize_id(name)
        
        levels = {}
        for i, lvl_idx in enumerate(level_indices):
            if lvl_idx < len(parts):
                levels[level_scores[i]] = parts[lvl_idx]
            else:
                levels[level_scores[i]] = ""

        weight_raw = parts[peso_idx] if peso_idx < len(parts) else "0 %"
        weight = _parse_weight(weight_raw)

        criteria.append({
            "name": name,
            "id": criterion_id,
            "levels": levels,
            "weight": weight,
        })

    return criteria


# ---------------------------------------------------------------------------
# Generation logic
# ---------------------------------------------------------------------------

def generate_prompt(criterion: Dict) -> str:
    """Generate a prompt file for a single criterion."""
    name = criterion["name"]
    levels = criterion["levels"]
    
    level_text = ""
    for score in sorted(levels.keys()):
        desc = levels[score]
        if desc:
            level_text += f"- **{score}/10**: {desc}\n"

    return f"""Analiza el siguiente documento y evalúa el criterio: **{name}**.

Documento:
--{{DOCUMENTO}}--

## Contexto de Análisis Previo

--{{CONTEXTO}}--

Niveles de evaluación definidos en la rúbrica:
{level_text}

Evalúa el criterio asignando una puntuación global de 0 a 10 basándote en los niveles descritos.
Utiliza el contexto de análisis previo como evidencia complementaria.

Formato de respuesta:
# Evaluación: {name}

## Análisis
[Comentarios detallados con evidencias del documento y contexto]

## Puntuación
**Puntuación:** X/10

## Observaciones
[Recomendaciones de mejora]
"""


def generate_yaml(criteria: List[Dict], prompts_dir: str, rubric_id: str = "imported") -> str:
    """Generate the YAML config string."""
    total_weight = sum(c["weight"] for c in criteria)
    if total_weight <= 0:
        raise ValueError("Total weight is 0. Cannot normalize.")
    
    # Normalize weights to sum to 1.0
    for c in criteria:
        c["weight"] = round(c["weight"] / total_weight, 4)

    rubric_criteria = []
    for c in criteria:
        prompt_filename = f"{rubric_id}_{c['id']}.md"
        rubric_criteria.append({
            "id": c["id"],
            "name": c["name"],
            "weight": c["weight"],
            "prompt": prompt_filename,
            "description": f"Evaluación de {c['name']} según rúbrica importada.",
        })

    config = {
        "version": "1.0",
        "id": rubric_id,
        "description": f"Rúbrica importada desde Markdown ({len(criteria)} criterios)",
        "provider": {
            "type": "ollama",
            "text_model": "qwen2.5-coder",
            "vision_model": "llava",
        },
        "rubric": {
            "criteria": rubric_criteria,
        },
        "options": {
            "multimodal": True,
            "skip_existing": False,
            "detailed_scoring": False,
        },
    }
    return yaml.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def import_rubric(
    input_path: str,
    output_yaml: str,
    prompts_dir: str,
) -> None:
    """Convert a Markdown rubric table to YAML + prompts."""
    md_content = Path(input_path).read_text(encoding="utf-8")
    criteria = parse_markdown_rubric(md_content)
    
    if not criteria:
        raise ValueError("No criteria found in the Markdown table.")

    logger.info("Parsed %d criteria from %s", len(criteria), input_path)

    # Determine rubric ID from output filename
    rubric_id = Path(output_yaml).stem.replace("rubric_", "").replace("rubrica_", "")
    if not rubric_id:
        rubric_id = "imported"

    # Create prompts directory
    p_dir = Path(prompts_dir)
    p_dir.mkdir(parents=True, exist_ok=True)

    # Generate prompts
    for c in criteria:
        prompt_content = generate_prompt(c)
        prompt_file = p_dir / f"{rubric_id}_{c['id']}.md"
        prompt_file.write_text(prompt_content, encoding="utf-8")
        logger.info("Generated prompt: %s", prompt_file)

    # Generate YAML
    yaml_content = generate_yaml(criteria, str(p_dir), rubric_id)
    yaml_path = Path(output_yaml)
    yaml_path.write_text(yaml_content, encoding="utf-8")
    logger.info("Generated config: %s", yaml_path)

    print(f"\n✅ Rúbrica importada: {len(criteria)} criterios")
    print(f"   Config: {yaml_path}")
    print(f"   Prompts: {p_dir}/")


def main() -> None:
    parser = argparse.ArgumentParser(description="Import Markdown rubric table to YAML + prompts.")
    parser.add_argument("--input", type=str, required=True, help="Path to Markdown rubric table")
    parser.add_argument("--output", type=str, required=True, help="Path to output YAML config")
    parser.add_argument("--prompts-dir", type=str, required=True, help="Directory to write prompt files")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    import_rubric(args.input, args.output, args.prompts_dir)


if __name__ == "__main__":
    main()
