"""
Nibble Nanny - The Ingredient Teacher (educate.py)
Translates scientific, corporate, or obscure chemical names into plain English:
1. What it actually is (source, manufacturing process)
2. What it does to your body (metabolic, allergic, or physiological impact)
3. Color-codes items for the specific Nanny Squad member
"""

import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from ingredient_db import INGREDIENT_KNOWLEDGE


@dataclass
class IngredientExplanation:
    name: str
    cleaned_name: str
    color: str             # "red" | "yellow" | "green" | "neutral"
    color_emoji: str       # "🔴" | "🟡" | "🟢" | "⚪"
    what: str
    health: str
    category: str
    nanny_note: Optional[str] = None
    is_safe_list: bool = False


def clean_ingredient_string(raw: str) -> str:
    """Removes percentages, brackets, and extra punctuation from ingredient tokens."""
    cleaned = raw.lower().strip()
    cleaned = re.sub(r"\d+[\.\d]*\s*%", "", cleaned)     # Remove '15%' or '2.5%'
    cleaned = re.sub(r"\(.*?\)", "", cleaned)            # Remove inner parens
    cleaned = re.sub(r"[\[\]\*\:]", "", cleaned)         # Remove brackets, colons
    cleaned = cleaned.replace("e-", "e").replace("ins-", "ins").replace("ins ", "ins")
    return cleaned.strip()


def lookup_ingredient_in_db(token: str) -> Optional[Dict[str, Any]]:
    """Looks up token in INGREDIENT_KNOWLEDGE by direct key or alias match."""
    token_clean = clean_ingredient_string(token)
    if not token_clean:
        return None

    # 1. Direct match
    if token_clean in INGREDIENT_KNOWLEDGE:
        return INGREDIENT_KNOWLEDGE[token_clean]

    # 2. Check all keys for substring/boundary match
    for key, data in INGREDIENT_KNOWLEDGE.items():
        if key in token_clean or token_clean in key:
            return data

    # 3. Check aliases
    for key, data in INGREDIENT_KNOWLEDGE.items():
        aliases = data.get("aliases") or []
        for alias in aliases:
            alias_clean = clean_ingredient_string(alias)
            if alias_clean == token_clean or alias_clean in token_clean or token_clean in alias_clean:
                return data

    return None


def educate_ingredients(
    ingredients: List[str],
    profile: Optional[Dict[str, Any]] = None,
    banned_matches: Optional[List[str]] = None,
    ambiguous_matches: Optional[List[str]] = None
) -> List[IngredientExplanation]:
    """
    Analyzes each ingredient and produces a color-coded educational card.
    """
    banned_matches = banned_matches or []
    ambiguous_matches = ambiguous_matches or []
    results: List[IngredientExplanation] = []
    seen = set()

    COLOR_EMOJIS = {
        "red": "🔴",
        "yellow": "🟡",
        "green": "🟢",
        "neutral": "⚪"
    }

    p_id = profile.get("profile_id") if profile else None

    for raw in ingredients:
        cleaned = clean_ingredient_string(raw)
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)

        db_info = lookup_ingredient_in_db(raw)

        if db_info:
            category = db_info.get("category", "general")
            what = db_info.get("what", "Food ingredient.")
            health = db_info.get("health", "Used in processed foods.")
            is_safe = category == "safe_chemical"

            # Determine color
            is_banned_here = any(cleaned in b.lower() for b in banned_matches)
            is_ambiguous_here = any(cleaned in a.lower() for a in ambiguous_matches)

            nanny_name = profile.get("nanny_title", "the Nibble Nanny Squad") if profile else "the Nibble Nanny Squad"
            if is_banned_here or (p_id and p_id in db_info.get("profiles_affected", []) and db_info.get("severity") == "banned"):
                color = "red"
                nanny_note = f"Triggered an alert for {nanny_name}!"
            elif is_ambiguous_here or (p_id and p_id in db_info.get("profiles_affected", []) and db_info.get("severity") == "ambiguous"):
                color = "yellow"
                nanny_note = f"Caution recommended for {nanny_name}."
            elif is_safe:
                color = "green"
                nanny_note = "Safe & beneficial ingredient despite the complex chemical name."
            else:
                color = "neutral"
                nanny_note = None

            results.append(IngredientExplanation(
                name=raw.strip(),
                cleaned_name=cleaned,
                color=color,
                color_emoji=COLOR_EMOJIS[color],
                what=what,
                health=health,
                category=category,
                nanny_note=nanny_note,
                is_safe_list=is_safe
            ))
        else:
            # Not in curated database - provide helpful neutral card
            results.append(IngredientExplanation(
                name=raw.strip(),
                cleaned_name=cleaned,
                color="neutral",
                color_emoji=COLOR_EMOJIS["neutral"],
                what="Common dietary ingredient.",
                health="Standard food component with no immediate high-risk alerts flagged in our database.",
                category="general",
                nanny_note=None,
                is_safe_list=False
            ))

    # Sort priority: Red first -> Yellow -> Green -> Neutral
    ORDER = {"red": 0, "yellow": 1, "green": 2, "neutral": 3}
    results.sort(key=lambda x: ORDER.get(x.color, 3))

    return results
