"""
Nibble Nanny - Validation Layer (The Mathematical Trust Gate)
Ensures raw vision extraction data is mathematically consistent, unit-normalized,
and free from model hallucinations or decimal misreads before running rules.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    trusted: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    normalized: Dict[str, Any] = field(default_factory=dict)
    per_pack: Dict[str, Any] = field(default_factory=dict)
    per_serving: Dict[str, Any] = field(default_factory=dict)
    calculated_energy_kcal: Optional[float] = None
    energy_deviation_pct: Optional[float] = None


def parse_numeric(val: Any) -> Optional[float]:
    """Parse string or numeric values safely, handling trace strings like '<0.5g' or 'nil'."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        cleaned = val.strip().lower()
        if cleaned in ("trace", "nil", "negligible", "none", "0"):
            return 0.0
        if cleaned.startswith("<"):
            return 0.0
        # Strip units in specific order: kcal, kj, mg, g, ml
        for unit in ("kcal", "kj", "mg", "ml", "g"):
            cleaned = cleaned.replace(unit, "")
        try:
            return float(cleaned.strip())
        except ValueError:
            return None
    return None


def validate(extracted: Dict[str, Any]) -> ValidationResult:
    """
    Validates extracted nutrition data using 9 deterministic checks.
    Returns normalized data ready for rules evaluation.
    """
    errors: List[str] = []
    warnings: List[str] = []
    normalized: Dict[str, Any] = {}
    per_serving: Dict[str, Any] = {}
    per_pack: Dict[str, Any] = {}

    if not extracted or not isinstance(extracted, dict):
        return ValidationResult(trusted=False, errors=["Empty or invalid extraction payload"])

    nutrition = extracted.get("nutrition") or {}
    serving_size_dict = extracted.get("serving_size") or {}
    pack_size_dict = extracted.get("pack_size") or {}

    serving_size_g = parse_numeric(serving_size_dict.get("value"))
    pack_size_g = parse_numeric(pack_size_dict.get("value"))
    servings_per_pack = parse_numeric(extracted.get("servings_per_pack"))

    # Calculate missing servings_per_pack if both sizes present
    if not servings_per_pack and serving_size_g and pack_size_g and serving_size_g > 0:
        servings_per_pack = round(pack_size_g / serving_size_g, 1)

    # 1. Check readability & null count
    core_fields = ["energy_kcal", "protein_g", "carbohydrates_g", "sugar_g", "fat_g", "sodium_mg"]
    null_core_count = sum(1 for f in core_fields if parse_numeric(nutrition.get(f)) is None)

    if null_core_count >= 5 and not parse_numeric(nutrition.get("energy_kj")) and not parse_numeric(nutrition.get("salt_g")):
        if extracted.get("table_found") is False:
            errors.append("No nutrition table found in the image")
        else:
            errors.append("Nutrition table is largely unreadable (over 80% fields missing)")

    # 2. Extract & normalize raw values
    energy_kcal = parse_numeric(nutrition.get("energy_kcal"))
    energy_kj = parse_numeric(nutrition.get("energy_kj"))
    protein_g = parse_numeric(nutrition.get("protein_g")) or 0.0
    carbs_g = parse_numeric(nutrition.get("carbohydrates_g")) or 0.0
    sugar_g = parse_numeric(nutrition.get("sugar_g"))
    added_sugar_g = parse_numeric(nutrition.get("added_sugar_g"))
    fat_g = parse_numeric(nutrition.get("fat_g")) or 0.0
    sat_fat_g = parse_numeric(nutrition.get("saturated_fat_g"))
    trans_fat_g = parse_numeric(nutrition.get("trans_fat_g"))
    fibre_g = parse_numeric(nutrition.get("fibre_g")) or 0.0
    sodium_mg = parse_numeric(nutrition.get("sodium_mg"))
    salt_g = parse_numeric(nutrition.get("salt_g"))

    # 3. Unit Conversions: kJ -> kcal
    if energy_kcal is None and energy_kj is not None:
        energy_kcal = round(energy_kj / 4.184, 1)
        warnings.append(f"Converted stated energy {energy_kj} kJ to {energy_kcal} kcal")

    # Unit Conversions: salt -> sodium (1g salt ≈ 400mg sodium)
    if sodium_mg is None and salt_g is not None:
        sodium_mg = round(salt_g * 400.0, 1)
        warnings.append(f"Converted stated salt {salt_g}g to {sodium_mg}mg sodium")

    # 4. Energy Cross-Check (The Atwater Formula)
    calculated_energy = None
    deviation_pct = None
    if energy_kcal and (carbs_g or protein_g or fat_g):
        calculated_energy = round((carbs_g * 4.0) + (protein_g * 4.0) + (fat_g * 9.0) + (fibre_g * 2.0), 1)
        if energy_kcal > 0:
            deviation_pct = abs(calculated_energy - energy_kcal) / energy_kcal
            if deviation_pct > 0.25:
                # Big discrepancy: likely decimal misread or hallucinated number
                errors.append(
                    f"Energy mismatch: Stated {energy_kcal} kcal, but sum of macros (4C+4P+9F) = {calculated_energy} kcal "
                    f"({deviation_pct*100:.1f}% deviation). Possible label misread."
                )
            elif deviation_pct > 0.15:
                warnings.append(
                    f"Mild energy variance: Stated {energy_kcal} kcal vs calculated {calculated_energy} kcal ({deviation_pct*100:.1f}% deviation)"
                )

    # 5. Sanity Bounds Check (Per 100g max is 100g!)
    basis = (extracted.get("nutrition_basis") or "per_100g").lower()
    is_per_serving_basis = "serving" in basis

    if not is_per_serving_basis:
        if carbs_g > 105.0 or fat_g > 105.0 or protein_g > 105.0:
            errors.append("Impossible macronutrient values (>100g per 100g basis detected)")
        if (carbs_g + fat_g + protein_g) > 110.0:
            errors.append(f"Sum of macros ({carbs_g + fat_g + protein_g:.1f}g) exceeds physical packet weight of 100g")
        if sugar_g is not None and sugar_g > (carbs_g + 2.0):
            warnings.append(f"Stated sugar ({sugar_g}g) exceeds stated total carbohydrates ({carbs_g}g)")

    # 6. Normalization into Standard per-100g and per-serving dictionaries
    if is_per_serving_basis and serving_size_g and serving_size_g > 0:
        multiplier_to_100g = 100.0 / serving_size_g
        normalized = {
            "energy_kcal": round(energy_kcal * multiplier_to_100g, 1) if energy_kcal else None,
            "protein_g": round(protein_g * multiplier_to_100g, 2),
            "carbohydrates_g": round(carbs_g * multiplier_to_100g, 2),
            "sugar_g": round(sugar_g * multiplier_to_100g, 2) if sugar_g is not None else None,
            "added_sugar_g": round(added_sugar_g * multiplier_to_100g, 2) if added_sugar_g is not None else None,
            "fat_g": round(fat_g * multiplier_to_100g, 2),
            "saturated_fat_g": round(sat_fat_g * multiplier_to_100g, 2) if sat_fat_g is not None else None,
            "trans_fat_g": round(trans_fat_g * multiplier_to_100g, 2) if trans_fat_g is not None else None,
            "fibre_g": round(fibre_g * multiplier_to_100g, 2),
            "sodium_mg": round(sodium_mg * multiplier_to_100g, 1) if sodium_mg is not None else None,
        }
        per_serving = {
            "energy_kcal": energy_kcal,
            "protein_g": protein_g,
            "carbohydrates_g": carbs_g,
            "sugar_g": sugar_g,
            "added_sugar_g": added_sugar_g,
            "fat_g": fat_g,
            "saturated_fat_g": sat_fat_g,
            "trans_fat_g": trans_fat_g,
            "fibre_g": fibre_g,
            "sodium_mg": sodium_mg,
        }
    else:
        # Standard per-100g basis
        normalized = {
            "energy_kcal": energy_kcal,
            "protein_g": protein_g,
            "carbohydrates_g": carbs_g,
            "sugar_g": sugar_g,
            "added_sugar_g": added_sugar_g,
            "fat_g": fat_g,
            "saturated_fat_g": sat_fat_g,
            "trans_fat_g": trans_fat_g,
            "fibre_g": fibre_g,
            "sodium_mg": sodium_mg,
        }
        # Compute per-serving if serving_size is known
        if serving_size_g and serving_size_g > 0:
            factor = serving_size_g / 100.0
            per_serving = {
                "energy_kcal": round(energy_kcal * factor, 1) if energy_kcal else None,
                "protein_g": round(protein_g * factor, 2),
                "carbohydrates_g": round(carbs_g * factor, 2),
                "sugar_g": round(sugar_g * factor, 2) if sugar_g is not None else None,
                "added_sugar_g": round(added_sugar_g * factor, 2) if added_sugar_g is not None else None,
                "fat_g": round(fat_g * factor, 2),
                "saturated_fat_g": round(sat_fat_g * factor, 2) if sat_fat_g is not None else None,
                "trans_fat_g": round(trans_fat_g * factor, 2) if trans_fat_g is not None else None,
                "fibre_g": round(fibre_g * factor, 2),
                "sodium_mg": round(sodium_mg * factor, 1) if sodium_mg is not None else None,
            }
        else:
            per_serving = normalized.copy()

    # 7. Whole-Pack Calculations
    if servings_per_pack and servings_per_pack > 0:
        per_pack = {
            k: (round(v * servings_per_pack, 1) if v is not None else None)
            for k, v in per_serving.items()
        }
    elif pack_size_g and pack_size_g > 0:
        factor = pack_size_g / 100.0
        per_pack = {
            k: (round(v * factor, 1) if v is not None else None)
            for k, v in normalized.items()
        }
    else:
        per_pack = per_serving.copy()

    # Confidence check: model notes
    for note in extracted.get("confidence_notes") or []:
        warnings.append(f"Vision note: {note}")

    is_trusted = len(errors) == 0

    return ValidationResult(
        trusted=is_trusted,
        errors=errors,
        warnings=warnings,
        normalized=normalized,
        per_serving=per_serving,
        per_pack=per_pack,
        calculated_energy_kcal=calculated_energy,
        energy_deviation_pct=deviation_pct,
    )
