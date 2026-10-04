"""
Nibble Nanny - Multimodal Label Extraction Layer (extract.py)
Uses Gemma 3 Vision (via Ollama or API) to extract nutrition tables,
ingredients, allergen statements, and regulatory marks from packaging photos.
"""

import os
import re
import json
import base64
import io
from typing import Dict, Any, Optional
from PIL import Image
import requests

EXTRACTION_SYSTEM_PROMPT = """You are Nibble Nanny's food label reader. You will receive an image of a food product packaging or nutrition label.
Extract the nutrition table and ingredients EXACTLY as printed.

CRITICAL RULES:
1. Return ONLY valid JSON adhering strictly to the schema below. No commentary, no preamble.
2. Use null for any field you cannot clearly read or that is absent from the label. DO NOT GUESS OR ESTIMATE.
3. If nutrition is given per serving, set "nutrition_basis": "per_serving". If per 100g/ml, set "per_100g".
4. Split the ingredients into a clean array in "ingredients_list" AND include the full unedited text in "ingredients_raw".
5. Note Indian dietary dots: "is_vegetarian_marked": true (green dot in green square) or "is_nonveg_marked": true (brown/red dot).
6. In "confidence_notes", add flags like "curved surface", "glare on packet", or "text partially cut off".

SCHEMA:
{
  "product_name": "string or null",
  "table_found": true or false,
  "serving_size": {"value": number or null, "unit": "g" or "ml" or null},
  "servings_per_pack": number or null,
  "pack_size": {"value": number or null, "unit": "g" or "ml" or null},
  "nutrition": {
    "energy_kcal": number or null,
    "energy_kj": number or null,
    "protein_g": number or null,
    "carbohydrates_g": number or null,
    "sugar_g": number or null,
    "added_sugar_g": number or null,
    "fat_g": number or null,
    "saturated_fat_g": number or null,
    "trans_fat_g": number or null,
    "fibre_g": number or null,
    "sodium_mg": number or null,
    "salt_g": number or null
  },
  "nutrition_basis": "per_100g" or "per_serving" or "unclear",
  "ingredients_raw": "string or null",
  "ingredients_list": ["string"],
  "allergen_info": "string or null",
  "is_vegetarian_marked": true or false or null,
  "is_nonveg_marked": true or false or null,
  "multiple_tables": false,
  "confidence_notes": []
}
"""


def preprocess_image(image_bytes: bytes, max_dimension: int = 1024) -> bytes:
    """Resizes high-resolution smartphone images to prevent request timeouts and reduce token usage."""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        # Convert RGBA / P to RGB
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Downscale if wider/taller than max_dimension
        w, h = img.size
        if max(w, h) > max_dimension:
            scale = max_dimension / float(max(w, h))
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        return buffer.getvalue()
    except Exception as e:
        print(f"Warning: Image preprocessing failed: {e}")
        return image_bytes


def clean_json_response(raw_text: str) -> Optional[Dict[str, Any]]:
    """Extracts and parses JSON object from model output, handling markdown blocks."""
    if not raw_text:
        return None

    cleaned = raw_text.strip()
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(1)
    else:
        # Fallback regex for first { to last }
        match_brace = re.search(r"(\{.*\})", cleaned, re.DOTALL)
        if match_brace:
            cleaned = match_brace.group(1)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"JSON parse error on model response: {e}")
        return None


def extract_with_ollama(
    image_bytes: bytes,
    model: str = "gemma3:4b",
    host: str = "http://localhost:11434"
) -> Optional[Dict[str, Any]]:
    """Attempts local Gemma vision extraction via Ollama."""
    try:
        b64_img = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "model": model,
            "prompt": EXTRACTION_SYSTEM_PROMPT,
            "images": [b64_img],
            "stream": False,
            "options": {"temperature": 0.1}
        }
        res = requests.post(f"{host}/api/generate", json=payload, timeout=60)
        if res.status_code == 200:
            data = res.json()
            return clean_json_response(data.get("response", ""))
    except Exception as e:
        print(f"Ollama local extraction unavailable: {e}")
    return None


def extract_with_gemini_api(image_bytes: bytes, api_key: str) -> Optional[Dict[str, Any]]:
    """Calls Google AI Studio Gemini API for multimodal vision extraction."""
    models_to_try = [
        "gemini-flash-lite-latest",
        "gemini-flash-latest",
        "gemini-3.8-flash",
        "gemini-3.5-flash",
        "gemini-3.1-flash-lite"
    ]
    b64_img = base64.b64encode(image_bytes).decode("utf-8")

    for model_name in models_to_try:
        try:
            print(f"[VISION API] Attempting extraction with model: {model_name}...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            payload = {
                "contents": [{
                    "parts": [
                        {"text": EXTRACTION_SYSTEM_PROMPT},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": b64_img
                            }
                        }
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "response_mime_type": "application/json"
                }
            }
            res = requests.post(url, json=payload, timeout=15)
            if res.status_code == 200:
                result = res.json()
                candidates = result.get("candidates") or []
                if candidates:
                    text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    parsed = clean_json_response(text)
                    if parsed:
                        print(f"[VISION API] Extraction successful with {model_name}!")
                        parsed["source"] = f"google_ai_studio/{model_name}"
                        return parsed
            else:
                print(f"[VISION API ERROR] {model_name} returned HTTP {res.status_code}: {res.text}")
        except Exception as e:
            print(f"[VISION API EXCEPTION] {model_name} failed: {e}")

    return None


def extract_label(image_bytes: bytes) -> Dict[str, Any]:
    """
    Main extraction pipeline:
    1. Preprocesses image
    2. Tries local Ollama Gemma
    3. Tries Gemini API if key is present
    4. Returns structured error payload if model is unreachable
    """
    from dotenv import load_dotenv
    load_dotenv(override=True)

    processed_bytes = preprocess_image(image_bytes)

    # 1. Try Local Gemma via Ollama
    ollama_model = os.getenv("OLLAMA_MODEL", "gemma3:4b")
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    extracted = extract_with_ollama(processed_bytes, model=ollama_model, host=ollama_host)
    if extracted:
        extracted["source"] = f"ollama/{ollama_model}"
        return extracted

    # 2. Try Gemini API
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        print("[VISION API] GEMINI_API_KEY detected in environment. Calling vision model...")
        extracted = extract_with_gemini_api(processed_bytes, gemini_key)
        if extracted:
            return extracted
        else:
            print("[VISION API] Vision API call failed to extract valid data.")
    else:
        print("[VISION API WARNING] No GEMINI_API_KEY found in environment or .env file.")

    # 3. Fallback: If no AI endpoint is active, return informative payload
    return {
        "product_name": "Scanned Food Item",
        "table_found": False,
        "source": "offline_fallback",
        "confidence_notes": ["No vision model active. Use test samples or set GEMINI_API_KEY in .env."]
    }
