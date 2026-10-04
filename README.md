# 🍪 Nibble Nanny — The AI Food Guardian Built for Friends

> **Submission for the Hacktoberfest Weekend Challenge: Build for a Friend**  
> *One photo. Four friends protected. Corporate deception unmasked.*

[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-2026%20Weekend%20Challenge-orange.svg)](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01)
[![Built with Gemma 3](https://img.shields.io/badge/AI%20Core-Gemma%203%20Vision-blue.svg)](https://ai.google.dev/gemma)
[![Deployed on Render](https://img.shields.io/badge/Deploy-Render%20Docker-46E3B7.svg)](https://render.com)
[![Tests Passing](https://img.shields.io/badge/Tests-19%2F19%20Passing-success.svg)]()

---

## 📖 The Story

Standing in a supermarket aisle with friends shouldn't require a master's degree in food chemistry.

- **Sneha** has severe lactose intolerance, constantly squinting at 4pt text wondering if *"sodium caseinate"* or *"whey powder"* counts as dairy.
- **Priya** is pre-diabetic, unaware that *"maltodextrin"* has a glycemic index of 105—spiking blood sugar faster than pure table sugar.
- **Rahul** manages hypertension, trying to mental-math grams of salt into milligrams of sodium across a 4-serving bag of chips.
- **Amit** follows strict Jain dietary rules, regularly having to search whether cryptic numbers like **E120** mean red fruit or boiled insect bodies.

We built **Nibble Nanny** so that a single smartphone snapshot answers all four friends' questions in seconds, exposes deceptive packaging loopholes, and teaches them what each ingredient actually does to the human body.

---

## 🦸‍♀️ Meet the "Nibble Nanny Squad"

```
┌───────────────────┬──────────────┬─────────────────────────────────────────────────────────────┐
│ Squad Member      │ For Friend   │ Core Domain & Watchdog Focus                                │
├───────────────────┼──────────────┼─────────────────────────────────────────────────────────────┤
│ 🥛 Dairy Nanny    │ Sneha        │ Lactose & Casein/Whey Milk Protein Allergies                │
│ 🍬 Sugar Nanny    │ Priya        │ Blood Sugar Caps & 30+ Covert Industrial Sweeteners         │
│ 🧂 Salt Nanny     │ Rahul        │ Hypertension, Sodium Thresholds & Whole-Pack Math           │
│ 🌱 Karma Nanny    │ Amit         │ Jain Purity, Animal Rennet & Cochineal Bug Dyes (E120)      │
│ 🕵️‍♀️ Nanny Noir    │ The Public   │ Corporate Deception, 0g Trans Fat Loopholes & Benzene Risks │
└───────────────────┴──────────────┴─────────────────────────────────────────────────────────────┘
```

---

## 🏛️ System Architecture

```
                    ┌──────────────────────────────────────────────┐
                    │            Friend's Phone / Web UI           │
                    │   Camera Capture / Upload / 1-Click Samples  │
                    └──────────────────────┬───────────────────────┘
                                           │ Packaging Photo
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: EYES — Multimodal Vision Extraction (`extract.py`)                           │
│ • Gemma 3 Vision (via Ollama / Local Open Weights / API Fallback)                     │
│ • Extracts structured JSON: Nutrition table, serving size, pack weight, raw & split   │
│   ingredients, allergen statements, green/red dietary dots, confidence flags          │
└──────────────────────────────────────────┬─────────────────────────────────────────────┘
                                           │ Raw Extracted JSON
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ LAYER 2: TRUST GATE — Deterministic Validation (`validate.py`)                         │
│ • 9 Mathematical & Sanity Checks:                                                     │
│   1. Missing field ratio gate (>50% unreadable = untrusted)                            │
│   2. Atwater Energy Balance: 4(carbs) + 4(protein) + 9(fat) + 2(fibre) ≈ stated kcal   │
│   3. Impossible bounds check (macronutrients > 100g per 100g)                          │
│   4. Basis normalization (per-serving vs per-100g)                                     │
│   5. Energy unit conversion (kJ / 4.184 -> kcal)                                       │
│   6. Salt-to-Sodium conversion (salt_g * 400 -> sodium_mg)                             │
│   7. Whole-pack consumption multiplier                                                 │
│   8. Decimal OCR misread rejection                                                     │
└──────────────────────────────────────────┬─────────────────────────────────────────────┘
                                           │ Validated & Normalized Data
                     ┌─────────────────────┼─────────────────────┐
                     ▼                     ▼                     ▼
┌───────────────────────────┐ ┌───────────────────────────┐ ┌───────────────────────────┐
│ LAYER 3: THE BRAIN        │ │ LAYER 4A: THE TEACHER     │ │ LAYER 4B: THE WATCHDOG    │
│ `rules.py`                │ │ `educate.py` & `db.py`    │ │ `tricks.py`               │
│                           │ │                           │ │                           │
│ • Evaluates 4 Squad Rules │ │ • 120+ Curated ingredient │ │ • 12 Deterministic trick  │
│ • Verdicts: OK, CAREFUL,  │ │   knowledge database      │ │   detectors:              │
│   SKIP, or CAN'T JUDGE    │ │ • Plain-English impact on │ │   • Sugar Splitting       │
│ • Nested parenthetical    │ │   the human body          │ │   • Microscopic Servings  │
│   ingredient parsing      │ │ • Color coding: 🔴 Banned,│ │   • "0g Trans Fat" Lie    │
│ • Clear personalized      │ │   🟡 Caution, 🟢 Safe     │ │   • Benzene Cocktail      │
│   voice lines             │ │   ⚪ General Info         │ │     (E211 + Vitamin C)    │
└─────────────┬─────────────┘ └─────────────┬─────────────┘ └─────────────┬─────────────┘
              │                             │                             │
              └─────────────────────────────┼─────────────────────────────┘
                                            ▼
                    ┌──────────────────────────────────────────────┐
                    │               Interactive UI                 │
                    │   4-Verdict Cards + Deception Alerts + Edu   │
                    └──────────────────────────────────────────────┘
```

---

## ⚡ Quickstart

### 1. Local Run
```bash
# Clone the repository
git clone https://github.com/your-username/nibble-nanny.git
cd nibble-nanny

# Create virtual environment & install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the application
python3 app.py
```
Open **`http://localhost:5001`** in your browser!

### 2. Run with Docker
```bash
docker build -t nibble-nanny .
docker run -p 10000:10000 -e PORT=10000 nibble-nanny
```

### 3. Run Test Suite
```bash
PYTHONPATH=. pytest tests/
```
*All 19 unit & integration tests pass with 100% success.*

### 4. Run Benchmark Suite
```bash
python3 eval/eval_runner.py
```
*Evaluates real snack packaging (Parle-G, Maggi, Protein Bars, Rusks) in under 15ms.*

---

## 🏆 Prize Categories

- **Best Use of Gemma ($200)**: Gemma 3 Vision acts as the optical engine, converting distorted packaging into structured, verifiable JSON schemas without leaking friend data to third parties.
- **Best Use of Render ($200)**: Fully containerized with a production `Dockerfile` and `render.yaml` blueprint with healthcheck monitoring.
- **Best Use of GitHub Copilot ($100)**: Used extensively for generating comprehensive edge-case tests and medical ingredient aliases.

---

## 📄 License
MIT © 2026. Built with care for friends everywhere.
