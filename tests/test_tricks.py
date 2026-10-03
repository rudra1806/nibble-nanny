"""
Unit Tests for tricks.py (Nanny Noir - Corporate Deception Watchdog)
"""

from tricks import detect_all_tricks


def test_detect_sugar_splitting():
    extracted = {
        "product_name": "Crunchy Biscuits",
        "ingredients_list": ["wheat flour", "sugar", "maltodextrin", "liquid glucose", "dextrose", "palm oil"]
    }
    alerts = detect_all_tricks(extracted, {})
    assert any(a.id == "sugar_splitting" for a in alerts)


def test_detect_trans_fat_loophole():
    extracted = {
        "product_name": "Bakery Rusk",
        "ingredients_raw": "Refined flour, partially hydrogenated vegetable oil, sugar, yeast",
        "ingredients_list": ["refined flour", "partially hydrogenated vegetable oil", "sugar"]
    }
    normalized = {"trans_fat_g": 0.0}
    alerts = detect_all_tricks(extracted, normalized)
    assert any(a.id == "trans_fat_loophole" for a in alerts)


def test_detect_dangerous_combination_benzene():
    extracted = {
        "product_name": "Orange Fruit Drink",
        "ingredients_raw": "Water, sugar, orange pulp, preservative (sodium benzoate - E211), antioxidant (ascorbic acid - E300)",
        "ingredients_list": ["water", "sugar", "orange pulp", "sodium benzoate", "ascorbic acid"]
    }
    alerts = detect_all_tricks(extracted, {})
    assert any(a.id == "benzene_formation_risk" for a in alerts)


def test_detect_tiny_serving():
    extracted = {
        "product_name": "Potato Crisps",
        "serving_size": {"value": 15, "unit": "g"},
        "servings_per_pack": 10,
        "ingredients_list": ["potato", "palm oil", "salt"]
    }
    alerts = detect_all_tricks(extracted, {})
    assert any(a.id == "tiny_serving" for a in alerts)
