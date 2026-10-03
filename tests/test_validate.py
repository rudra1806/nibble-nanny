"""
Unit Tests for validate.py (Mathematical Trust Gate)
"""

import pytest
from validate import validate, parse_numeric


def test_parse_numeric():
    assert parse_numeric("12.5g") == 12.5
    assert parse_numeric("400mg") == 400.0
    assert parse_numeric("<0.1g") == 0.0
    assert parse_numeric("trace") == 0.0
    assert parse_numeric("nil") == 0.0
    assert parse_numeric(None) is None


def test_validate_energy_cross_check_success():
    # 10g carbs (40kcal) + 5g protein (20kcal) + 10g fat (90kcal) = 150 kcal
    payload = {
        "table_found": True,
        "nutrition_basis": "per_100g",
        "nutrition": {
            "energy_kcal": 150.0,
            "protein_g": 5.0,
            "carbohydrates_g": 10.0,
            "fat_g": 10.0,
            "sugar_g": 6.0,
            "sodium_mg": 120.0
        }
    }
    res = validate(payload)
    assert res.trusted is True
    assert len(res.errors) == 0
    assert res.calculated_energy_kcal == 150.0


def test_validate_energy_mismatch_decimal_error():
    # Model misreads 0.5g fat as 50g fat -> calculated energy will wildly mismatch
    payload = {
        "table_found": True,
        "nutrition_basis": "per_100g",
        "nutrition": {
            "energy_kcal": 100.0,
            "protein_g": 2.0,
            "carbohydrates_g": 10.0,
            "fat_g": 50.0,  # 50*9 = 450 kcal alone!
        }
    }
    res = validate(payload)
    assert res.trusted is False
    assert any("Energy mismatch" in err for err in res.errors)


def test_validate_unit_conversion_kj_and_salt():
    payload = {
        "table_found": True,
        "nutrition_basis": "per_100g",
        "nutrition": {
            "energy_kj": 836.8,  # ~200 kcal
            "protein_g": 5.0,
            "carbohydrates_g": 30.0,
            "fat_g": 6.0,
            "salt_g": 1.5       # 1.5 * 400 = 600mg sodium
        }
    }
    res = validate(payload)
    assert res.trusted is True
    assert res.normalized["energy_kcal"] == pytest.approx(200.0, abs=1.0)
    assert res.normalized["sodium_mg"] == 600.0


def test_validate_impossible_bounds():
    payload = {
        "table_found": True,
        "nutrition_basis": "per_100g",
        "nutrition": {
            "energy_kcal": 400.0,
            "carbohydrates_g": 120.0,  # Impossible!
            "protein_g": 10.0,
            "fat_g": 10.0
        }
    }
    res = validate(payload)
    assert res.trusted is False
    assert any("Impossible macronutrient" in err for err in res.errors)
