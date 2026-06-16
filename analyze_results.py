#!/usr/bin/env python3
"""
analyze_results.py
==================
Extracts final grades from all evaluated memories and compares with professor's categories.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

def extract_grade(report_path: Path) -> Tuple[float, str]:
    """Extract final grade and performance level from evaluation report."""
    if not report_path.exists():
        return None, None
    
    content = report_path.read_text(encoding='utf-8')
    
    # Look for "Nota final: X.X/10"
    grade_match = re.search(r'Nota final:\s*(\d+\.?\d*)/10', content)
    level_match = re.search(r'Nivel de desempeño:\s*(\w+)', content)
    
    grade = float(grade_match.group(1)) if grade_match else None
    level = level_match.group(1) if level_match else None
    
    return grade, level

def analyze_all_results():
    """Analyze all evaluation results and compare with professor's categories."""
    results_dir = Path("tests/test final/results")
    
    categories = {
        "APROVAT": [],
        "NOTABLE": [],
        "EXCEL·LENT": []
    }
    
    for category in categories.keys():
        category_dir = results_dir / category
        if not category_dir.exists():
            continue
        
        for memory_dir in category_dir.iterdir():
            if not memory_dir.is_dir():
                continue
            
            report_file = memory_dir / "evaluacion_final.md"
            grade, level = extract_grade(report_file)
            
            if grade is not None:
                categories[category].append({
                    "name": memory_dir.name,
                    "grade": grade,
                    "level": level,
                    "report": str(report_file)
                })
    
    # Print summary
    print("=" * 80)
    print("ANÀLISI COMPARATIVA: Agent vs Professora")
    print("=" * 80)
    
    all_grades = []
    
    for category, memories in categories.items():
        if not memories:
            print(f"\n{category}: No hi ha resultats")
            continue
        
        grades = [m["grade"] for m in memories]
        avg_grade = sum(grades) / len(grades)
        min_grade = min(grades)
        max_grade = max(grades)
        
        all_grades.extend(grades)
        
        print(f"\n{category} (n={len(memories)}):")
        print(f"  Mitjana: {avg_grade:.2f}/10")
        print(f"  Rang: {min_grade:.1f} - {max_grade:.1f}")
        print(f"  Memòries:")
        for m in memories:
            print(f"    - {m['name']}: {m['grade']:.1f}/10 ({m['level']})")
    
    # Overall statistics
    if all_grades:
        overall_avg = sum(all_grades) / len(all_grades)
        print(f"\n" + "=" * 80)
        print(f"ESTADÍSTIQUES GLOBALS:")
        print(f"  Total memòries avaluades: {len(all_grades)}")
        print(f"  Mitjana global: {overall_avg:.2f}/10")
        print(f"  Desviació estàndard: {(sum((g - overall_avg)**2 for g in all_grades) / len(all_grades))**0.5:.2f}")
    
    # Save results to JSON
    output = {
        "categories": categories,
        "statistics": {
            "total": len(all_grades),
            "overall_avg": overall_avg if all_grades else None,
        }
    }
    
    output_file = results_dir / "analysis_results.json"
    output_file.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\nResultats guardats a: {output_file}")

if __name__ == "__main__":
    analyze_all_results()
