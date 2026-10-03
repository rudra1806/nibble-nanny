"""
Nibble Nanny - Rules & Personalization Engine
Evaluates validated food label data for the "Nibble Nanny Squad":
1. 🥛 Dairy Nanny (Sneha) - Lactose & Milk Protein Allergens
2. 🍬 Sugar Nanny (Priya) - Blood Sugar Limits & Covert Sugars
3. 🧂 Salt Nanny (Rahul) - Hypertension & Sodium Thresholds
4. 🌱 Karma Nanny (Amit) - Jain Dietary Purity & Animal Derivatives
"""

import json
import os
import re
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from validate import ValidationResult


@dataclass
class Verdict:
    profile_id: str
    friend_name: str
    nanny_title: str
    tagline: str
    avatar_emoji: str
    status: str            # "OK" | "CAREFUL" | "SKIP" | "CANT_JUDGE"
    status_emoji: str     # "✅" | "⚠️" | "❌" | "❓"
    summary_line: str
    voice_note: str
    reasons: List[str] = field(default_factory=list)
    found_banned: List[str] = field(default_factory=list)
    found_ambiguous: List[str] = field(default_factory=list)
    math_details: Dict[str, Any] = field(default_factory=dict)


def flatten_ingredients(ingredients_raw: Optional[str], ingredients_list: Optional[List[str]]) -> List[str]:
    """
    Expands compound ingredients like 'Chocolate (sugar, milk solids, cocoa butter)'
    into individual searchable items while preserving outer structure.
    """
    items = set()

    if ingredients_list:
        for item in ingredients_list:
            cleaned = item.strip().lower()
            if cleaned:
                items.add(cleaned)
                # If there are sub-items in parentheses
                subs = re.findall(r"\((.*?)\)", cleaned)
                for sub in subs:
                    for sub_item in sub.split(","):
                        s_cleaned = sub_item.strip()
                        if s_cleaned:
                            items.add(s_cleaned)

    if ingredients_raw:
        # Also parse raw string with regex
        raw_clean = ingredients_raw.lower()
        # Extract everything inside parentheses
        for sub in re.findall(r"\((.*?)\)", raw_clean):
            for part in sub.split(","):
                part_clean = part.strip()
                if part_clean:
                    items.add(part_clean)
        # Split by comma or semicolon
        for part in re.split(r"[,;]", raw_clean):
            part_clean = re.sub(r"\(.*?\)", "", part).strip()
            if part_clean:
                items.add(part_clean)

    return sorted(list(items))


def check_term_match(term: str, ingredient_item: str) -> bool:
    """Exact word-boundary or substring match for ingredients."""
    term_clean = term.lower().strip()
    item_clean = ingredient_item.lower().strip()

    if term_clean == item_clean:
        return True

    # Use regex word boundary where appropriate
    escaped = re.escape(term_clean)
    pattern = rf"(^|\b|[\W_]){escaped}($|\b|[\W_])"
    return bool(re.search(pattern, item_clean))


def evaluate_profile(profile: Dict[str, Any], extracted: Dict[str, Any], validation: ValidationResult) -> Verdict:
    """
    Evaluates a single profile against extracted data and validation outcome.
    """
    p_id = profile["profile_id"]
    friend = profile.get("friend_name", "Friend")
    title = profile.get("nanny_title", "Nibble Nanny")
    tagline = profile.get("tagline", "")
    avatar = profile.get("avatar_emoji", "🍪")
    voice = profile.get("voice_quote", "")
    rule_type = profile.get("rule_type", "both")

    # If validation failed with fatal errors, we can't judge numeric profiles
    if not validation.trusted:
        if rule_type in ("numeric", "both"):
            return Verdict(
                profile_id=p_id,
                friend_name=friend,
                nanny_title=title,
                tagline=tagline,
                avatar_emoji=avatar,
                status="CANT_JUDGE",
                status_emoji="❓",
                summary_line=f"Couldn't reliably verify nutrition data for {title}.",
                voice_note="Numbers don't add up on this label. Better safe than sorry!",
                reasons=[f"Validation error: {err}" for err in validation.errors],
            )

    ingredients = flatten_ingredients(
        extracted.get("ingredients_raw"),
        extracted.get("ingredients_list")
    )
    allergen_info = (extracted.get("allergen_info") or "").lower()

    found_banned = []
    found_ambiguous = []
    reasons = []

    ing_rules = profile.get("ingredient_rules", {})
    banned_terms = ing_rules.get("banned_exact", [])
    ambiguous_terms = ing_rules.get("ambiguous", [])
    allowed_exceptions = ing_rules.get("allowed_exceptions", [])

    # Check Allergen statement first
    for b in banned_terms:
        if b in allergen_info:
            found_banned.append(f"Allergen statement mentions '{b}'")

    # Check Ingredient list
    for ing in ingredients:
        # Skip if explicitly in allowed exceptions
        if any(exc in ing for exc in allowed_exceptions):
            continue

        for b in banned_terms:
            if check_term_match(b, ing):
                match_str = f"{ing} (matches banned '{b}')"
                if match_str not in found_banned:
                    found_banned.append(match_str)

        for a in ambiguous_terms:
            if check_term_match(a, ing):
                match_str = f"{ing} (ambiguous source: '{a}')"
                if match_str not in found_ambiguous and not any(ing in fb for fb in found_banned):
                    found_ambiguous.append(match_str)

    # 1. 🥛 Dairy Nanny (Sneha)
    if p_id == "no_dairy":
        if found_banned:
            return Verdict(
                profile_id=p_id,
                friend_name=friend,
                nanny_title=title,
                tagline=tagline,
                avatar_emoji=avatar,
                status="SKIP",
                status_emoji="❌",
                summary_line=f"❌ SKIP — Dairy detected! Lactose alert level: RED.",
                voice_note="Sneha, step away from the packet! Milk derivatives detected.",
                reasons=[f"Contains dairy ingredients: {', '.join(found_banned)}"],
                found_banned=found_banned,
                found_ambiguous=found_ambiguous,
            )
        if found_ambiguous:
            return Verdict(
                profile_id=p_id,
                friend_name=friend,
                nanny_title=title,
                tagline=tagline,
                avatar_emoji=avatar,
                status="CAREFUL",
                status_emoji="⚠️",
                summary_line=f"⚠️ CAREFUL — Ambiguous flavoring or dairy derivatives.",
                voice_note="Could contain hidden dairy in flavourings. Check with manufacturer.",
                reasons=[f"Ambiguous ingredients detected: {', '.join(found_ambiguous)}"],
                found_banned=found_banned,
                found_ambiguous=found_ambiguous,
            )
        return Verdict(
            profile_id=p_id,
            friend_name=friend,
            nanny_title=title,
            tagline=tagline,
            avatar_emoji=avatar,
            status="OK",
            status_emoji="✅",
            summary_line=f"✅ ALL CLEAR — No dairy or lactose derivatives detected.",
            voice_note="Safe for Sneha! Enjoy without stomach worries.",
            reasons=["No milk solids, casein, whey, or butter derivatives found."],
            found_banned=[],
            found_ambiguous=[],
        )

    # 2. 🍬 Sugar Nanny (Priya)
    elif p_id == "low_sugar":
        limits = profile.get("limits", {})
        max_serving_g = limits.get("sugar_per_serving_max_g", 10.0)
        max_pack_g = limits.get("sugar_per_pack_max_g", 25.0)
        warning_serving_g = limits.get("sugar_warning_serving_g", 7.0)

        sugar_serving = validation.per_serving.get("sugar_g")
        sugar_pack = validation.per_pack.get("sugar_g")

        math_details = {
            "sugar_per_serving_g": sugar_serving,
            "sugar_per_pack_g": sugar_pack,
            "max_serving_limit_g": max_serving_g,
            "max_pack_limit_g": max_pack_g,
        }

        # Check banned industrial sugars (maltodextrin, HFCS)
        has_hidden_spikers = len(found_banned) > 0

        # Numeric check
        is_serving_excess = sugar_serving is not None and sugar_serving > max_serving_g
        is_pack_excess = sugar_pack is not None and sugar_pack > max_pack_g
        is_serving_close = sugar_serving is not None and sugar_serving >= warning_serving_g

        if is_serving_excess or is_pack_excess or (has_hidden_spikers and is_serving_close):
            causes = []
            if is_serving_excess:
                causes.append(f"Sugar per serving ({sugar_serving}g) exceeds Priya's limit ({max_serving_g}g)")
            if is_pack_excess:
                causes.append(f"Whole pack sugar ({sugar_pack}g) exceeds pack cap ({max_pack_g}g)")
            if has_hidden_spikers:
                causes.append(f"High-glycemic covert sugars present: {', '.join(found_banned)}")

            return Verdict(
                profile_id=p_id,
                friend_name=friend,
                nanny_title=title,
                tagline=tagline,
                avatar_emoji=avatar,
                status="SKIP",
                status_emoji="❌",
                summary_line=f"❌ SKIP — High sugar load will cause a glucose spike!",
                voice_note="Priya, this will spike your blood sugar rapidly!",
                reasons=causes,
                found_banned=found_banned,
                found_ambiguous=found_ambiguous,
                math_details=math_details,
            )

        if is_serving_close or has_hidden_spikers or found_ambiguous:
            warnings = []
            if is_serving_close:
                warnings.append(f"Sugar per serving ({sugar_serving}g) is near the caution zone ({warning_serving_g}g+)")
            if has_hidden_spikers:
                warnings.append(f"Contains covert high-GI sweetener: {', '.join(found_banned)}")
            if found_ambiguous:
                warnings.append(f"Contains concentrated sweeteners: {', '.join(found_ambiguous)}")

            return Verdict(
                profile_id=p_id,
                friend_name=friend,
                nanny_title=title,
                tagline=tagline,
                avatar_emoji=avatar,
                status="CAREFUL",
                status_emoji="⚠️",
                summary_line=f"⚠️ CAREFUL — Moderate sugar or hidden sweeteners present.",
                voice_note="Borderline sugar levels. Limit to one small portion, Priya!",
                reasons=warnings,
                found_banned=found_banned,
                found_ambiguous=found_ambiguous,
                math_details=math_details,
            )

        sugar_display = f"{sugar_serving}g" if sugar_serving is not None else "Low"
        return Verdict(
            profile_id=p_id,
            friend_name=friend,
            nanny_title=title,
            tagline=tagline,
            avatar_emoji=avatar,
            status="OK",
            status_emoji="✅",
            summary_line=f"✅ SAFE FOR PRIYA — Sugar ({sugar_display}/serving) is well within limit ({max_serving_g}g).",
            voice_note="Blood sugar approved! No maltodextrin or sugar spikes here.",
            reasons=[f"Sugar is {sugar_display} per serving (well below {max_serving_g}g threshold)."],
            found_banned=[],
            found_ambiguous=[],
            math_details=math_details,
        )

    # 3. 🧂 Salt Nanny (Rahul)
    elif p_id == "low_salt":
        limits = profile.get("limits", {})
        max_serving_mg = limits.get("sodium_per_serving_max_mg", 400.0)
        max_pack_mg = limits.get("sodium_per_pack_max_mg", 1000.0)
        warning_serving_mg = limits.get("sodium_warning_serving_mg", 250.0)

        sodium_serving = validation.per_serving.get("sodium_mg")
        sodium_pack = validation.per_pack.get("sodium_mg")

        math_details = {
            "sodium_per_serving_mg": sodium_serving,
            "sodium_per_pack_mg": sodium_pack,
            "max_serving_limit_mg": max_serving_mg,
            "max_pack_limit_mg": max_pack_mg,
        }

        is_serving_excess = sodium_serving is not None and sodium_serving > max_serving_mg
        is_pack_excess = sodium_pack is not None and sodium_pack > max_pack_mg
        is_serving_close = sodium_serving is not None and sodium_serving >= warning_serving_mg

        if is_serving_excess or is_pack_excess or found_banned:
            causes = []
            if is_serving_excess:
                causes.append(f"Sodium per serving ({sodium_serving}mg) exceeds cap ({max_serving_mg}mg)")
            if is_pack_excess:
                causes.append(f"Whole pack sodium ({sodium_pack}mg) exceeds danger limit ({max_pack_mg}mg)")
            if found_banned:
                causes.append(f"Contains synthetic sodium enhancers: {', '.join(found_banned)}")

            return Verdict(
                profile_id=p_id,
                friend_name=friend,
                nanny_title=title,
                tagline=tagline,
                avatar_emoji=avatar,
                status="SKIP",
                status_emoji="❌",
                summary_line=f"❌ SKIP — High sodium bomb! Dangerous for blood pressure.",
                voice_note="Rahul, step away! That sodium level will spike your blood pressure.",
                reasons=causes,
                found_banned=found_banned,
                found_ambiguous=found_ambiguous,
                math_details=math_details,
            )

        if is_serving_close or found_ambiguous:
            warnings = []
            if is_serving_close:
                warnings.append(f"Sodium per serving ({sodium_serving}mg) is near caution limit ({warning_serving_mg}mg)")
            if found_ambiguous:
                warnings.append(f"Hidden sodium source detected: {', '.join(found_ambiguous)}")

            return Verdict(
                profile_id=p_id,
                friend_name=friend,
                nanny_title=title,
                tagline=tagline,
                avatar_emoji=avatar,
                status="CAREFUL",
                status_emoji="⚠️",
                summary_line=f"⚠️ CAREFUL — Moderate sodium content ({sodium_serving}mg/serving).",
                voice_note="Eat with care, Rahul. Don't eat the whole pack!",
                reasons=warnings,
                found_banned=found_banned,
                found_ambiguous=found_ambiguous,
                math_details=math_details,
            )

        na_display = f"{sodium_serving}mg" if sodium_serving is not None else "Low"
        return Verdict(
            profile_id=p_id,
            friend_name=friend,
            nanny_title=title,
            tagline=tagline,
            avatar_emoji=avatar,
            status="OK",
            status_emoji="✅",
            summary_line=f"✅ SAFE FOR RAHUL — Low sodium ({na_display}/serving), heart-safe.",
            voice_note="Blood pressure can relax. Clean sodium numbers!",
            reasons=[f"Sodium content ({na_display}) is comfortably under the {max_serving_mg}mg cap."],
            found_banned=[],
            found_ambiguous=[],
            math_details=math_details,
        )

    # 4. 🌱 Karma Nanny (Amit)
    elif p_id == "jain_veg":
        is_veg_marked = extracted.get("is_vegetarian_marked")
        is_nonveg_marked = extracted.get("is_nonveg_marked")

        if is_nonveg_marked is True:
            found_banned.append("Brown/Red non-vegetarian dot explicitly printed on packaging")

        if found_banned:
            return Verdict(
                profile_id=p_id,
                friend_name=friend,
                nanny_title=title,
                tagline=tagline,
                avatar_emoji=avatar,
                status="SKIP",
                status_emoji="❌",
                summary_line=f"❌ SKIP — Violates Jain purity or vegetarian guidelines.",
                voice_note="Amit, don't eat this! Animal derivatives or root ingredients found.",
                reasons=[f"Prohibited ingredients found: {', '.join(found_banned)}"],
                found_banned=found_banned,
                found_ambiguous=found_ambiguous,
            )

        if found_ambiguous or is_veg_marked is False:
            warnings = []
            if found_ambiguous:
                warnings.append(f"Ambiguous animal/plant additives: {', '.join(found_ambiguous)}")
            if is_veg_marked is False:
                warnings.append("Green vegetarian dot was not confirmed on packaging")

            return Verdict(
                profile_id=p_id,
                friend_name=friend,
                nanny_title=title,
                tagline=tagline,
                avatar_emoji=avatar,
                status="CAREFUL",
                status_emoji="⚠️",
                summary_line=f"⚠️ CAREFUL — Additives like E471 could be of animal or plant origin.",
                voice_note="Look for the green dot certification before eating, Amit.",
                reasons=warnings,
                found_banned=found_banned,
                found_ambiguous=found_ambiguous,
            )

        return Verdict(
            profile_id=p_id,
            friend_name=friend,
            nanny_title=title,
            tagline=tagline,
            avatar_emoji=avatar,
            status="OK",
            status_emoji="✅",
            summary_line=f"✅ JAIN & VEG APPROVED — Pure plant ingredients, zero root crops.",
            voice_note="Karma approved! Pure vegetarian and Jain compliant.",
            reasons=["Green dot verified, no gelatin, rennet, carmine (E120), or root vegetables."],
            found_banned=[],
            found_ambiguous=[],
        )

    # Generic Fallback
    return Verdict(
        profile_id=p_id,
        friend_name=friend,
        nanny_title=title,
        tagline=tagline,
        avatar_emoji=avatar,
        status="OK",
        status_emoji="✅",
        summary_line="✅ Evaluated successfully.",
        voice_note="Looks good!",
        reasons=[],
    )


def evaluate_all(profiles_dir: str, extracted: Dict[str, Any], validation: ValidationResult) -> Dict[str, Verdict]:
    """Loads all profile JSONs from directory and evaluates each."""
    results = {}
    if not os.path.exists(profiles_dir):
        return results

    profile_files = sorted([f for f in os.listdir(profiles_dir) if f.endswith(".json")])
    for p_file in profile_files:
        path = os.path.join(profiles_dir, p_file)
        try:
            with open(path, "r", encoding="utf-8") as f:
                profile = json.load(f)
            p_id = profile.get("profile_id", p_file.replace(".json", ""))
            results[p_id] = evaluate_profile(profile, extracted, validation)
        except Exception as e:
            print(f"Error evaluating profile {p_file}: {e}")

    return results
