"""
Unit Tests for rules.py (The Nibble Nanny Squad Verdicts)
"""

import json
from validate import validate
from rules import evaluate_profile


def get_profile(filename):
    with open(f"profiles/{filename}", "r") as f:
        return json.load(f)


def test_dairy_nanny_catches_casein_and_whey():
    profile = get_profile("no_dairy.json")
    extracted = {
        "product_name": "Protein Bar",
        "ingredients_raw": "Protein blend (calcium caseinate, whey protein isolate), soy crisps",
        "ingredients_list": ["protein blend (calcium caseinate, whey protein isolate)", "soy crisps"],
        "allergen_info": "Contains milk and soy",
        "nutrition": {"energy_kcal": 200, "protein_g": 20, "carbohydrates_g": 15, "fat_g": 5}
    }
    v_result = validate(extracted)
    verdict = evaluate_profile(profile, extracted, v_result)

    assert verdict.status == "SKIP"
    assert verdict.avatar_emoji == "🥛"
    assert "Dairy Nanny" in verdict.nanny_title
    assert any("casein" in r.lower() or "whey" in r.lower() or "milk" in r.lower() for r in verdict.found_banned)


def test_sugar_nanny_flags_maltodextrin_and_high_sugar():
    profile = get_profile("low_sugar.json")
    extracted = {
        "product_name": "Energy Bar",
        "serving_size": {"value": 50, "unit": "g"},
        "servings_per_pack": 1,
        "ingredients_raw": "Oats, maltodextrin, cane sugar, honey",
        "ingredients_list": ["oats", "maltodextrin", "cane sugar", "honey"],
        "nutrition": {"energy_kcal": 220, "carbohydrates_g": 35, "sugar_g": 18, "protein_g": 4, "fat_g": 4}
    }
    v_result = validate(extracted)
    verdict = evaluate_profile(profile, extracted, v_result)

    assert verdict.status == "SKIP"
    assert verdict.avatar_emoji == "🍬"
    assert "Sugar Nanny" in verdict.nanny_title
    assert any("maltodextrin" in r.lower() for r in verdict.found_banned)


def test_salt_nanny_flags_high_sodium():
    profile = get_profile("low_salt.json")
    extracted = {
        "product_name": "Instant Noodles",
        "serving_size": {"value": 70, "unit": "g"},
        "servings_per_pack": 1,
        "ingredients_raw": "Wheat flour, palm oil, salt, monosodium glutamate",
        "ingredients_list": ["wheat flour", "palm oil", "salt", "monosodium glutamate"],
        "nutrition": {"energy_kcal": 320, "carbohydrates_g": 45, "protein_g": 7, "fat_g": 12, "sodium_mg": 950}
    }
    v_result = validate(extracted)
    verdict = evaluate_profile(profile, extracted, v_result)

    assert verdict.status == "SKIP"
    assert verdict.avatar_emoji == "🧂"
    assert "Salt Nanny" in verdict.nanny_title
    assert any("sodium" in r.lower() or "msg" in r.lower() for r in verdict.reasons)


def test_karma_nanny_catches_carmine_and_gelatin():
    profile = get_profile("jain_veg.json")
    extracted = {
        "product_name": "Red Berry Candy",
        "ingredients_raw": "Sugar, glucose syrup, gelatin, acidity regulator, color (E120)",
        "ingredients_list": ["sugar", "glucose syrup", "gelatin", "acidity regulator", "color (e120)"],
        "nutrition": {"energy_kcal": 150, "carbohydrates_g": 35, "sugar_g": 25, "protein_g": 2, "fat_g": 0}
    }
    v_result = validate(extracted)
    verdict = evaluate_profile(profile, extracted, v_result)

    assert verdict.status == "SKIP"
    assert verdict.avatar_emoji == "🌱"
    assert "Karma Nanny" in verdict.nanny_title
    assert any("e120" in r.lower() or "gelatin" in r.lower() for r in verdict.found_banned)
