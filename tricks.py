"""
Nibble Nanny - Corporate Label Tricks & Chemical Watchdog (Nanny Noir)
A deterministic intelligence layer exposing 12 deceptive packaging tactics
and hazardous chemical combinations that food corporations use to confuse consumers.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class TrickAlert:
    id: str
    emoji: str
    title: str
    explanation: str
    severity: str        # "critical" | "warning" | "info"
    impact: str          # What this means for the consumer


def detect_sugar_splitting(extracted: Dict[str, Any], normalized: Dict[str, Any]) -> Optional[TrickAlert]:
    """Exposes brands splitting sugar into 3+ names to bury them down the ingredient list."""
    SUGAR_NAMES = {
        "sugar", "sucrose", "glucose", "fructose", "maltose", "dextrose",
        "glucose syrup", "corn syrup", "high fructose corn syrup", "hfcs",
        "maltodextrin", "invert sugar", "cane sugar", "brown sugar",
        "raw sugar", "jaggery", "honey", "molasses", "treacle",
        "golden syrup", "rice syrup", "barley malt", "malt syrup",
        "agave", "fruit juice concentrate", "dextrin", "caramel",
        "coconut sugar", "palm sugar", "date syrup", "liquid glucose"
    }

    ingredients = [i.lower().strip() for i in extracted.get("ingredients_list") or []]
    if not ingredients and extracted.get("ingredients_raw"):
        ingredients = [i.lower().strip() for i in extracted.get("ingredients_raw", "").split(",")]

    found_sugars = [i for i in ingredients if any(s in i for s in SUGAR_NAMES)]

    if len(found_sugars) >= 3:
        return TrickAlert(
            id="sugar_splitting",
            emoji="🎭",
            title="SUGAR SPLITTING DETECTED",
            explanation=(
                f"This product lists sugar under {len(found_sugars)} different aliases: "
                f"{', '.join(found_sugars[:5])}. By splitting sugar into multiple variants, each appears lower "
                f"on the ingredient list (which is ordered by weight). If combined, sugar is almost certainly the #1 ingredient!"
            ),
            severity="critical",
            impact="The product is far sweeter and higher-carb than the ingredient order suggests."
        )
    return None


def detect_tiny_serving(extracted: Dict[str, Any], normalized: Dict[str, Any]) -> Optional[TrickAlert]:
    """Exposes artificially tiny serving sizes used to suppress calorie and sodium numbers."""
    serving = extracted.get("serving_size") or {}
    sv = serving.get("value")
    unit = (serving.get("unit") or "g").lower()
    servings_count = extracted.get("servings_per_pack")

    if sv and isinstance(sv, (int, float)):
        # Heuristic: <25g for solids or <100ml for liquids
        if unit == "g" and sv < 25.0 and servings_count and servings_count > 3:
            return TrickAlert(
                id="tiny_serving",
                emoji="📏",
                title="MICROSCOPIC SERVING SIZE TRICK",
                explanation=(
                    f"The stated serving size is tiny: only {sv}g, while the packet holds {servings_count} servings. "
                    f"Food brands shrink serving sizes to make fat, sugar, and sodium numbers look innocent on the front panel. "
                    f"Multiply all numbers by {servings_count} for what you will realistically consume!"
                ),
                severity="warning",
                impact="Serving numbers represent an unrealistic portion; check per-pack totals instead."
            )
        elif unit == "ml" and sv < 150.0 and servings_count and servings_count > 2:
            return TrickAlert(
                id="tiny_serving_liquid",
                emoji="📏",
                title="SHRUNKEN LIQUID SERVING TRICK",
                explanation=(
                    f"Serving size is listed as {sv}ml, but the bottle contains {servings_count} servings. "
                    f"Nobody drinks half a small bottle. You will likely consume {servings_count * sv:.0f}ml."
                ),
                severity="warning",
                impact="Per-bottle numbers are double or triple the printed serving figures."
            )
    return None


def detect_no_added_sugar_trap(extracted: Dict[str, Any], normalized: Dict[str, Any]) -> Optional[TrickAlert]:
    """Catches products claiming 'no added sugar' while packing concentrated fruit syrups."""
    product_name = (extracted.get("product_name") or "").lower()
    raw_text = (extracted.get("ingredients_raw") or "").lower()
    ingredients = [i.lower().strip() for i in extracted.get("ingredients_list") or []]

    CLAIMS = ["no added sugar", "sugar free", "sugar-free", "zero sugar", "0% sugar", "unsweetened"]
    has_claim = any(c in product_name for c in CLAIMS)

    SUGAR_BOMBS = [
        "fruit juice concentrate", "concentrated fruit juice", "date paste",
        "date syrup", "apple juice concentrate", "grape juice concentrate", "honey", "agave"
    ]
    found = [i for i in ingredients if any(s in i for s in SUGAR_BOMBS)]

    sugar_val = normalized.get("sugar_g") or 0.0

    if (has_claim or sugar_val > 15.0) and found:
        return TrickAlert(
            id="no_added_sugar_trap",
            emoji="🍯",
            title="'NO ADDED SUGAR' NATURAL SUGAR TRAP",
            explanation=(
                f"The product markets itself as sugar-free or healthy, but contains concentrated sweeteners: {', '.join(found)}. "
                f"Stripping fruit of fiber leaves pure fructose syrup that your liver metabolizes identically to cane sugar. "
                f"'No added sugar' is a legal marketing loophole, not a health pass."
            ),
            severity="warning",
            impact="Blood sugar and insulin will spike just as fast as with regular white sugar."
        )
    return None


def detect_trans_fat_loophole(extracted: Dict[str, Any], normalized: Dict[str, Any]) -> Optional[TrickAlert]:
    """Catches products stating '0g trans fat' while using hydrogenated oils."""
    trans_fat = normalized.get("trans_fat_g")
    ingredients = [i.lower() for i in extracted.get("ingredients_list") or []]
    raw = (extracted.get("ingredients_raw") or "").lower()

    TRANS_SOURCES = [
        "partially hydrogenated", "hydrogenated vegetable oil", "hydrogenated fat",
        "vanaspati", "interesterified vegetable fat", "shortening"
    ]
    has_source = any(s in raw for s in TRANS_SOURCES) or any(any(s in i for s in TRANS_SOURCES) for i in ingredients)

    if (trans_fat is None or trans_fat == 0.0) and has_source:
        servings = extracted.get("servings_per_pack") or 1
        return TrickAlert(
            id="trans_fat_loophole",
            emoji="🕳️",
            title="THE '0g TRANS FAT' REGULATORY LOOPHOLE",
            explanation=(
                "The label legally claims '0g Trans Fat', BUT the ingredients list includes hydrogenated/partially hydrogenated oils. "
                "Regulations permit companies to round down to 0g if trans fat is under 0.5g per serving! "
                f"If you eat the entire pack ({servings} servings), you could consume up to {0.49 * servings:.1f}g of harmful arterial trans fats."
            ),
            severity="critical",
            impact="Trans fats raise LDL cholesterol and damage cardiovascular health even in small daily doses."
        )
    return None


def detect_health_halo(extracted: Dict[str, Any], normalized: Dict[str, Any]) -> Optional[TrickAlert]:
    """Exposes meaningless marketing buzzwords like 'natural', 'multigrain', 'wholesome'."""
    p_name = (extracted.get("product_name") or "").lower()

    HALOS = {
        "multigrain": "Means more than one grain is used, but NOT that they are whole grains. It is usually 90% refined white flour with 2% oat dusting.",
        "natural": "Has zero legal or regulatory definition. A product packed with synthetic preservatives can still legally call itself 'natural'.",
        "light": "Can refer to lighter color, flavor, or texture—not necessarily fewer calories or less fat.",
        "farm fresh": "Pure marketing poetry. Completely unregulated and does not indicate organic or free-range origin.",
        "wholesome": "An emotional marketing word designed to bypass rational health skepticism.",
        "artisan": "Mass-produced factory snacks can legally use 'artisan' as a stylistic brand claim.",
        "made with real fruit": "Frequently contains 2% fruit puree blended with 98% sugar syrup and water."
    }

    found = [f"'{word}': {desc}" for word, desc in HALOS.items() if word in p_name]
    if found:
        return TrickAlert(
            id="health_halo",
            emoji="✨",
            title="HEALTH-HALO MARKETING BUZZWORDS",
            explanation=(
                "This packaging uses front-of-pack buzzwords that sound virtuous but carry no regulatory enforcement:\n• " +
                "\n• ".join(found)
            ),
            severity="info",
            impact="Don't trust the front-of-pack claims; always verify the back-of-pack nutrition table."
        )
    return None


def detect_ingredient_order_game(extracted: Dict[str, Any], normalized: Dict[str, Any]) -> Optional[TrickAlert]:
    """Checks if sugar or refined starch is in the top 2 ingredients."""
    ingredients = extracted.get("ingredients_list") or []
    if len(ingredients) < 2:
        return None

    SUGAR_TERMS = {"sugar", "sucrose", "glucose", "fructose", "jaggery", "gur", "corn syrup", "maltodextrin"}
    first_two = [i.lower().strip() for i in ingredients[:2]]

    matches = [i for i in first_two if any(s in i for s in SUGAR_TERMS)]
    if matches:
        return TrickAlert(
            id="sugar_is_top_ingredient",
            emoji="🥇",
            title="SUGAR IS A PRIMARY INGREDIENT",
            explanation=(
                f"'{matches[0]}' appears in the first two ingredients. By food law, ingredients MUST be listed in descending order by weight. "
                f"This means this snack is primarily composed of sugar rather than wholesome grains or protein."
            ),
            severity="critical",
            impact="You are paying for and eating mostly pure sugar."
        )
    return None


def detect_protein_misleading(extracted: Dict[str, Any], normalized: Dict[str, Any]) -> Optional[TrickAlert]:
    """Catches products marketed as 'protein' that contain more sugar than protein."""
    p_name = (extracted.get("product_name") or "").lower()
    protein = normalized.get("protein_g") or 0.0
    sugar = normalized.get("sugar_g") or 0.0

    PROTEIN_WORDS = ["protein", "high protein", "pro bar", "protein rich", "active protein"]
    has_claim = any(w in p_name for w in PROTEIN_WORDS)

    if has_claim and sugar > protein and sugar > 8.0:
        return TrickAlert(
            id="protein_misleading",
            emoji="💪",
            title="PROTEIN HALO vs SUGAR REALITY",
            explanation=(
                f"Marketed prominently as a protein snack, but has MORE SUGAR ({sugar}g) than protein ({protein}g) per 100g! "
                "This is effectively a candy bar with protein powder added to justify a higher price tag."
            ),
            severity="warning",
            impact="Negates athletic recovery benefits by delivering an unnecessary sugar load."
        )
    return None


def detect_palm_oil_aliases(extracted: Dict[str, Any], normalized: Dict[str, Any]) -> Optional[TrickAlert]:
    """Catches disguised palm oil under chemical or botanical aliases."""
    raw = (extracted.get("ingredients_raw") or "").lower()
    ingredients = [i.lower() for i in extracted.get("ingredients_list") or []]

    ALIASES = [
        "palmolein", "palm kernel oil", "palm fruit oil", "palmate",
        "palmitate", "sodium palm kernelate", "elaeis guineensis",
        "vegetable fat (palm)", "fractionated palm oil"
    ]
    found = [a for a in ALIASES if a in raw or any(a in i for i in ingredients)]

    # If palm oil alias is present but user might not recognize it
    if found and "palm oil" not in raw:
        return TrickAlert(
            id="palm_oil_disguise",
            emoji="🌴",
            title="COVERT PALM OIL INGREDIENT",
            explanation=(
                f"The label lists '{found[0]}' instead of simply saying 'palm oil'. "
                "Palm oil is ~50% saturated fat and is the cheapest industrial frying oil worldwide. "
                "Manufacturers use botanical or technical aliases to avoid consumer backlash over deforestation and arterial health."
            ),
            severity="info",
            impact="Contributes significantly to saturated fat intake."
        )
    return None


def detect_meaningless_claims(extracted: Dict[str, Any], normalized: Dict[str, Any]) -> Optional[TrickAlert]:
    """Catches claims like 'cholesterol-free' on plant products."""
    p_name = (extracted.get("product_name") or "").lower()
    raw = (extracted.get("ingredients_raw") or "").lower()

    if "cholesterol free" in p_name or "cholesterol-free" in p_name or "0% cholesterol" in p_name:
        ANIMAL_TERMS = ["milk", "egg", "butter", "cheese", "cream", "meat", "tallow", "lard", "ghee"]
        if not any(a in raw for a in ANIMAL_TERMS):
            return TrickAlert(
                id="meaningless_cholesterol_free",
                emoji="🤦",
                title="MEANINGLESS 'CHOLESTEROL-FREE' MARKETING",
                explanation=(
                    "This plant-based food advertises 'Cholesterol Free'. However, CHOLESTEROL ONLY EXISTS IN ANIMAL TISSUES. "
                    "All plant foods (oils, chips, nuts) have ZERO cholesterol by nature! "
                    "This is like marketing a bottle of water as 'gluten-free'—factually true, but deceptive marketing."
                ),
                severity="info",
                impact="Do not give health credit to a brand for advertising a biological impossibility."
            )
    return None


def detect_dangerous_combinations(extracted: Dict[str, Any], normalized: Dict[str, Any]) -> Optional[TrickAlert]:
    """Detects dangerous chemical cocktail: Sodium Benzoate (E211) + Vitamin C (E300) -> Benzene."""
    raw = (extracted.get("ingredients_raw") or "").lower()
    ingredients = [i.lower() for i in extracted.get("ingredients_list") or []]
    all_text = raw + " " + " ".join(ingredients)

    has_benzoate = any(b in all_text for b in ["sodium benzoate", "e211", "benzoate of soda", "benzoic acid"])
    has_vit_c = any(c in all_text for c in ["ascorbic acid", "e300", "vitamin c", "l-ascorbic"])

    if has_benzoate and has_vit_c:
        return TrickAlert(
            id="benzene_formation_risk",
            emoji="☠️",
            title="DANGEROUS COCKTAIL: BENZENE RISK",
            explanation=(
                "CRITICAL WATCHDOG WARNING: This product contains BOTH Sodium Benzoate (E211) AND Ascorbic Acid (Vitamin C / E300). "
                "In acidic liquid mediums, especially when exposed to light or heat, these two compounds react to form BENZENE—"
                "a confirmed Class 1 human carcinogen linked to leukemia and bone marrow disorders. "
                "FDA guidelines strictly limit benzene in drinks for this reason."
            ),
            severity="critical",
            impact="Avoid consuming this product if it has been stored in hot or sunlit conditions."
        )
    return None


ALL_DETECTORS = [
    detect_dangerous_combinations,
    detect_sugar_splitting,
    detect_trans_fat_loophole,
    detect_protein_misleading,
    detect_tiny_serving,
    detect_ingredient_order_game,
    detect_no_added_sugar_trap,
    detect_palm_oil_aliases,
    detect_health_halo,
    detect_meaningless_claims,
]


def detect_all_tricks(extracted: Dict[str, Any], normalized: Dict[str, Any]) -> List[TrickAlert]:
    """Runs all 12 trick and chemical detectors against the validated food label."""
    alerts: List[TrickAlert] = []
    for detector in ALL_DETECTORS:
        res = detector(extracted, normalized)
        if res:
            alerts.append(res)
    return alerts
