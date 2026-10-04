"""
Unit Tests for educate.py (The Ingredient Teacher)
"""

import json
from educate import educate_ingredients, lookup_ingredient_in_db


def test_lookup_ingredient_in_db():
    info = lookup_ingredient_in_db("maltodextrin")
    assert info is not None
    assert "glycemic" in info["health"].lower()

    # Alias check: 'sodium caseinate' should match casein
    casein_info = lookup_ingredient_in_db("sodium caseinate")
    assert casein_info is not None
    assert "casein" in casein_info["what"].lower() or "casein" in casein_info["category"]


def test_educate_ingredients_color_coding():
    with open("profiles/no_dairy.json") as f:
        profile = json.load(f)

    ingredients = [
        "wheat flour",
        "milk solids",
        "maltodextrin",
        "ascorbic acid"
    ]
    results = educate_ingredients(
        ingredients,
        profile=profile,
        banned_matches=["milk solids"]
    )

    # Milk solids should be red for Dairy Nanny
    milk_item = next(r for r in results if "milk" in r.cleaned_name)
    assert milk_item.color == "red"
    assert milk_item.color_emoji == "🔴"

    # Ascorbic acid is on the safe list -> green
    vit_c = next(r for r in results if "ascorbic" in r.cleaned_name)
    assert vit_c.color == "green"
    assert vit_c.color_emoji == "🟢"
    assert vit_c.is_safe_list is True

    # Wheat flour is neutral
    wheat = next(r for r in results if "wheat" in r.cleaned_name)
    assert wheat.color == "neutral"
