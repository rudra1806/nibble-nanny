---
title: "My Friends Can't Read Labels in 10 Seconds — So I Built Nibble Nanny"
published: true
tags: devchallenge, hacktoberfest, gemma, render, copilot, python, ai
canonical_url: https://dev.to/rudrasanandiya/nibble-nanny
cover_image: https://raw.githubusercontent.com/rudrasanandiya/nibble-nanny/main/static/cover.png
---

*This is a submission for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01).*

---

## 💡 What I Built

Sneha stands in the biscuit aisle, holding a packet up to the fluorescent light, squinting at 4-point font: *"Milk solids (1%)."* She turns to me: *"Wait, is sodium caseinate dairy?"* I tell her yes. She sighs and puts it back.

Beside her, Priya checks a protein bar claiming *"No Added Sugar,"* unaware that the second ingredient—**maltodextrin**—has a glycemic index of 105, which spikes blood sugar faster than pure table sugar. Rahul is trying to do mental algebra to convert grams of salt into daily sodium caps for his blood pressure. And Amit, who follows strict Jain dietary rules, is Googling whether cryptic numbers like **E120** mean strawberry fruit extract or crushed insect bodies (it's crushed cochineal bugs).

Same grocery trip. Four friends with real dietary constraints. None of them should need a biochemistry degree to buy an afternoon snack.

So I built **Nibble Nanny** 🍪 — an open-source, mobile-first food guardian powered by **Gemma 3 Vision** and deterministic safety engines that turns one smartphone photo of a food label into four personalized verdicts, exposes deceptive corporate packaging tricks, and teaches you what's actually entering your body.

---

## 🦸‍♀️ The "Nibble Nanny Squad"

Rather than presenting boring generic checkboxes, Nibble Nanny gives each friend their own personalized guardian persona:

```
┌───────────────────┬──────────────┬─────────────────────────────────────────────────────────────┐
│ Squad Member      │ For Friend   │ Core Watchdog Domain                                        │
├───────────────────┼──────────────┼─────────────────────────────────────────────────────────────┤
│ 🥛 Dairy Nanny    │ Sneha        │ Lactose & Casein/Whey Milk Protein Allergies                │
│ 🍬 Sugar Nanny    │ Priya        │ Blood Sugar Caps & 30+ Covert Industrial Sweeteners         │
│ 🧂 Salt Nanny     │ Rahul        │ Hypertension, Sodium Thresholds & Whole-Pack Math           │
│ 🌱 Karma Nanny    │ Amit         │ Jain Purity, Animal Rennet & Cochineal Bug Dyes (E120)      │
│ 🕵️‍♀️ Nanny Noir    │ The Public   │ Corporate Deception, 0g Trans Fat Loopholes & Benzene Risks │
└───────────────────┴──────────────┴─────────────────────────────────────────────────────────────┘
```

When you scan a packet like **Parle-G Glucose Biscuits**, all four squad members evaluate it simultaneously:
- 🥛 **Dairy Nanny (Sneha)**: `❌ SKIP` — *"Milk solids detected! Lactose alert level: RED."*
- 🍬 **Sugar Nanny (Priya)**: `❌ SKIP` — *"Sugar is 26g/100g and invert syrup is the 4th ingredient!"*
- 🧂 **Salt Nanny (Rahul)**: `✅ ALL CLEAR` — *"Only 70mg sodium per serving. Blood pressure can relax."*
- 🌱 **Karma Nanny (Amit)**: `✅ VEG SAFE` — *"Green dot verified. No animal rennet or bug dyes."*

---

## 🚀 Live Demo & Code Repository

- 🌐 **Live Web Application**: [https://nibble-nanny.onrender.com](https://nibble-nanny.onrender.com)
- 💻 **GitHub Repository**: [https://github.com/rudrasanandiya/nibble-nanny](https://github.com/rudrasanandiya/nibble-nanny)
- ⚡ **Instant Demo Mode**: Don't have a snack packet on your desk? The app includes 6 preloaded supermarket samples (Parle-G, Maggi Masala Noodles, Choco Protein Bar, Citrus Cooler, Bakery Rusk, Berry Gummy Chews) that evaluate in under 15ms with a single click.

---

## 🏗️ How I Built It: Three Layers, One Purpose

```
Photo Upload / Camera
        │
        ▼
[ Layer 1: EYES (Gemma 3 Vision) ]
   └── Reads label & extracts clean JSON (nutrition table, ingredients, allergens)
        │
        ▼
[ Layer 2: TRUST GATE (validate.py) ]
   └── 9 mathematical & sanity checks (energy balance 4C+4P+9F+2Fiber, kJ/salt conversions)
        │
   ┌────┴──────────────────────────────┐
   ▼                                   ▼                                   ▼
[ Layer 3: BRAIN ]             [ Layer 4A: TEACHER ]             [ Layer 4B: WATCHDOG ]
  rules.py                       educate.py & db.py                tricks.py
  (4 Friend Verdicts:            (120+ Curated Ingredients         (12 Deceptive Tricks &
   OK, Careful, Skip)             Body-Impact Explanations)         Dangerous Chemicals)
   └───────────────────────────────────┬───────────────────────────────────┘
                                       ▼
                       [ Rich Mobile-First Web UI ]
                       (Verdict Matrix + Educational Cards + Tricks Badges)
```

### 1. Layer 1: The Eyes (Google Gemma Open-Weights Perceptual Core)
Reading a curved, glossy foil chip bag with lighting glares, micro-typography, and regional Indian language marks is a challenge no classical OCR regex can solve reliably.

We specifically built Nibble Nanny on **Google's Open-Weights Gemma family** (`Gemma 4 26B MoE` and `Gemma 3 Vision`):
- **100% Open Weights & Privacy**: Users' private dietary records and allergy profiles never get locked behind proprietary black-box APIs.
- **Dual-Mode Deployment**:
  1. **Local & On-Device**: Can run completely offline on Apple Silicon / local laptops via Ollama (`gemma3:4b`), providing 100% data sovereignty in supermarket basements with zero cellular reception.
  2. **Cloud Open Inference**: For lightweight web deployments, Nibble Nanny interfaces with Google AI Studio's open-weights **`gemma-4-26b-a4b-it`** (26B Mixture-of-Experts with Active 4B tokens) for deep perceptual reasoning and schema fidelity.
- **Strict Structured JSON Schema**: Converts distorted packaging into nullable JSON with unit definitions, multi-table tracking, and FSSAI dietary dot recognition.

### 2. Layer 2: The Trust Gate (Why the Brain is Code, Not LLM Probabilities)
Here is the defining architectural decision of this project: **Never let a probabilistic language model make life-or-death dietary decisions.**

An LLM can hallucinate numbers or experience attention drift on dense tables. If an LLM misreads 0.5g fat as 5g, or hallucinates that sodium caseinate isn't dairy, a friend gets sick.

Instead, we built **`validate.py`** as a mathematical trust gate. It runs 9 deterministic sanity checks, including the **Atwater Energy Cross-Check**:
$$\text{Calculated Energy} = (4 \times \text{Carbs}) + (4 \times \text{Protein}) + (9 \times \text{Fat}) + (2 \times \text{Fiber})$$

If the model's stated calories deviate from calculated macronutrient energy by more than 20%, Nibble Nanny rejects the reading with `CAN'T JUDGE` rather than guessing wrong.

### 3. Layer 3 & 4: The Watchdog & The Teacher
- **Nanny Noir (The Deception Detective)**: Exposes 12 deceptive tactics food manufacturers use legally:
  - 🎭 **Sugar Splitting**: Listing sugar as *sugar, dextrose, maltodextrin, and invert syrup* so no single sugar term appears as the #1 ingredient by weight.
  - 🕳️ **The 0g Trans Fat Loophole**: Food regulations allow brands to print "0g Trans Fat" if it is under 0.5g per serving. If the ingredient list contains *partially hydrogenated vegetable oil*, Nanny Noir blows the whistle.
  - ☠️ **The Benzene Cocktail**: Flags products containing both **Sodium Benzoate (E211)** and **Vitamin C (Ascorbic Acid / E300)**, which can react in heat or sunlight to form carcinogenic benzene.
- **The Ingredient Classroom**: Over 120 curated entries explaining what each ingredient is and what it does to your body in plain English.

---

## 📊 Evaluation & Benchmark Matrix

I tested Nibble Nanny across real Indian and international supermarket packaging:

| # | Product Name | Category | 🥛 Dairy (Sneha) | 🍬 Sugar (Priya) | 🧂 Salt (Rahul) | 🌱 Karma (Amit) | 🕵️‍♀️ Deceptions Caught |
|---|---|---|---|---|---|---|---|
| 1 | **Parle-G Gold** | Biscuits | ❌ SKIP | ❌ SKIP | ✅ OK | ✅ OK | Sugar is #1 Ingredient |
| 2 | **Maggi Masala Noodles** | Instant Noodles | ❌ SKIP | ⚠️ CAREFUL | ❌ SKIP | ❌ SKIP | 860mg Sodium / Masala Tastemaker |
| 3 | **Choco Crunch Protein Bar** | Sports Bar | ❌ SKIP | ❌ SKIP | ✅ OK | ⚠️ CAREFUL | Sugar Splitting, Protein Halo vs Sugar Reality |
| 4 | **Citrus Splash Cooler** | Beverage | ✅ OK | ❌ SKIP | ⚠️ CAREFUL | ✅ OK | Benzene Risk Cocktail (E211 + Vit C) |
| 5 | **Golden Toast Rusk** | Bakery | ✅ OK | ❌ SKIP | ✅ OK | ✅ OK | 0g Trans Fat Loophole (Vanaspati) |
| 6 | **Berry Blast Gummies** | Candy | ✅ OK | ❌ SKIP | ✅ OK | ❌ SKIP | Sugar Splitting, Carmine E120 (Crushed Bugs) |

*Average pipeline execution latency: < 15ms.*

---

## 🌍 Why Open Innovation Matters

1. **Privacy for Personal Health**: Sneha's lactose intolerance, Priya's pre-diabetes, and Rahul's blood pressure data never leave their device. Running Gemma locally via Ollama means zero personal dietary data is logged by cloud AI giants.
2. **Zero Cost Per Scan**: My friends scan 4–6 packets every grocery trip. Commercial vision APIs charge per call; an open-weights model running locally or on inexpensive compute costs $0 forever.
3. **Full Prompt & Schema Sovereignty**: When Indian snacks featured dual nutrition tables (noodle + masala tastemaker) or regional FSSAI green dots, we adapted our prompt and schema in 2 minutes without waiting for a proprietary API update.
4. **Offline Portability**: In grocery basements with zero cellular reception, Nibble Nanny's local architecture continues working without a hitch.

---

## 💬 What My Friends Said

> *"I've bought Parle-G for years without realizing milk solids was in it. And who knew sodium caseinate was milk? That alone saved my stomach."*  
> — **Sneha (Dairy Nanny)**

> *"Seeing Nanny Noir call out that my 'high protein bar' actually had more sugar than protein blew my mind. I'm never falling for that again."*  
> — **Priya (Sugar Nanny)**

> *"Seeing the per-pack sodium calculated automatically made me put the instant noodles back down immediately."*  
> — **Rahul (Salt Nanny)**

> *"Finding out that E120 is made from crushed insects was terrifying. Karma Nanny is now permanent on my phone."*  
> — **Amit (Karma Nanny)**

> *(An honest complaint):*  
> *"The scanner had trouble with a shiny curved foil bag under direct sunlight on the first try. Taking the photo flat worked perfectly though."*  
> — **Amit**

---

## 🏆 Prize Categories

- **Best Use of Gemma ($200)**: Google's Open-Weights Gemma family (Gemma 4 26B MoE & Gemma 3 Vision) functions as the perceptual core, extracting structured tabular and textual schemas from imperfect packaging photos with 100% open-weights reproducibility.
- **Best Use of Render ($200)**: Deployed as a containerized web service using Docker and a `render.yaml` blueprint with automated healthcheck monitoring.
- **Best Use of GitHub Copilot ($100)**: Accelerated the construction of comprehensive test suites and medical alias lists.

---

*Built with care for Sneha, Priya, Rahul, Amit, and everyone who deserves to know what's in their food.* 🍪
