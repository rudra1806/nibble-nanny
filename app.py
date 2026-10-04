"""
Nibble Nanny - Backend Orchestration Service (app.py)
Integrates Multimodal Vision Extraction, Deterministic Validation,
Rules Evaluation, Watchdog Trick Detection, and Ingredient Education.
"""

import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from extract import extract_label
from validate import validate
from rules import evaluate_all
from tricks import detect_all_tricks
from educate import educate_ingredients

load_dotenv()

app = Flask(__name__, static_folder="static")
CORS(app)

PROFILES_DIR = os.path.join(os.path.dirname(__file__), "profiles")
SAMPLES_PATH = os.path.join(os.path.dirname(__file__), "eval", "test_packets.json")


def load_samples():
    if os.path.exists(SAMPLES_PATH):
        with open(SAMPLES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def process_label_payload(extracted: dict):
    """Core pipeline connecting all 4 layers."""
    # 1. Layer 2: Trust Gate Validation
    val_result = validate(extracted)

    # 2. Layer 3: The Brain (Rules Evaluation for 4 profiles)
    verdicts_dict = evaluate_all(PROFILES_DIR, extracted, val_result)

    # Convert Verdict dataclass objects to dicts
    verdicts_json = {}
    banned_acc = []
    ambiguous_acc = []
    for pid, v in verdicts_dict.items():
        verdicts_json[pid] = {
            "profile_id": v.profile_id,
            "friend_name": v.friend_name,
            "nanny_title": v.nanny_title,
            "tagline": v.tagline,
            "avatar_emoji": v.avatar_emoji,
            "status": v.status,
            "status_emoji": v.status_emoji,
            "summary_line": v.summary_line,
            "voice_note": v.voice_note,
            "reasons": v.reasons,
            "found_banned": v.found_banned,
            "found_ambiguous": v.found_ambiguous,
            "math_details": v.math_details
        }
        banned_acc.extend(v.found_banned)
        ambiguous_acc.extend(v.found_ambiguous)

    # 3. Layer 4A: The Consumer Watchdog (Label Tricks & Chemicals)
    tricks = detect_all_tricks(extracted, val_result.normalized)
    tricks_json = [
        {
            "id": t.id,
            "emoji": t.emoji,
            "title": t.title,
            "explanation": t.explanation,
            "severity": t.severity,
            "impact": t.impact
        }
        for t in tricks
    ]

    # 4. Layer 4B: The Teacher (Ingredient Education Breakdown)
    ing_list = extracted.get("ingredients_list") or []
    if not ing_list and extracted.get("ingredients_raw"):
        ing_list = [i.strip() for i in extracted.get("ingredients_raw", "").split(",") if i.strip()]

    education_cards = educate_ingredients(
        ing_list,
        banned_matches=banned_acc,
        ambiguous_matches=ambiguous_acc
    )
    education_json = [
        {
            "name": e.name,
            "cleaned_name": e.cleaned_name,
            "color": e.color,
            "color_emoji": e.color_emoji,
            "what": e.what,
            "health": e.health,
            "category": e.category,
            "nanny_note": e.nanny_note,
            "is_safe_list": e.is_safe_list
        }
        for e in education_cards
    ]

    return {
        "product_name": extracted.get("product_name") or "Food Product",
        "is_vegetarian_marked": extracted.get("is_vegetarian_marked"),
        "is_nonveg_marked": extracted.get("is_nonveg_marked"),
        "allergen_info": extracted.get("allergen_info"),
        "serving_size": extracted.get("serving_size"),
        "servings_per_pack": extracted.get("servings_per_pack"),
        "pack_size": extracted.get("pack_size"),
        "validation": {
            "trusted": val_result.trusted,
            "errors": val_result.errors,
            "warnings": val_result.warnings,
            "normalized_per_100g": val_result.normalized,
            "per_serving": val_result.per_serving,
            "per_pack": val_result.per_pack,
            "calculated_energy_kcal": val_result.calculated_energy_kcal,
            "energy_deviation_pct": val_result.energy_deviation_pct
        },
        "verdicts": verdicts_json,
        "tricks": tricks_json,
        "education": education_json,
        "source": extracted.get("source")
    }


# =============================================================================
# API ROUTES
# =============================================================================

@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "app": "Nibble Nanny",
        "version": "1.0.0",
        "theme": "Build for a Friend"
    })


@app.route("/api/profiles", methods=["GET"])
def get_profiles():
    profiles = []
    if os.path.exists(PROFILES_DIR):
        for f in sorted(os.listdir(PROFILES_DIR)):
            if f.endswith(".json"):
                with open(os.path.join(PROFILES_DIR, f), "r") as pf:
                    profiles.append(json.load(pf))
    return jsonify(profiles)


@app.route("/api/samples", methods=["GET"])
def get_samples():
    samples = load_samples()
    # Return minimal summary for UI buttons
    summaries = [
        {"id": s["id"], "name": s["name"], "category": s["category"], "hint": s.get("image_hint")}
        for s in samples
    ]
    return jsonify(summaries)


@app.route("/api/sample/<sample_id>", methods=["POST"])
def evaluate_sample(sample_id):
    samples = load_samples()
    matched = next((s for s in samples if s["id"] == sample_id), None)
    if not matched:
        return jsonify({"error": f"Sample packet '{sample_id}' not found"}), 404

    result = process_label_payload(matched["data"])
    result["sample_info"] = {
        "id": matched["id"],
        "name": matched["name"],
        "category": matched["category"]
    }
    return jsonify(result)


@app.route("/api/scan", methods=["POST"])
def scan_label():
    image_bytes = None

    if "photo" in request.files:
        file = request.files["photo"]
        image_bytes = file.read()
    elif request.is_json and "image_b64" in request.json:
        import base64
        b64_str = request.json["image_b64"]
        if "," in b64_str:
            b64_str = b64_str.split(",")[1]
        image_bytes = base64.b64decode(b64_str)

    if not image_bytes:
        return jsonify({"error": "No image provided. Please upload a photo or use a sample packet."}), 400

    # Layer 1: Multimodal Extraction
    extracted = extract_label(image_bytes)

    # Process through pipeline
    result = process_label_payload(extracted)
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
