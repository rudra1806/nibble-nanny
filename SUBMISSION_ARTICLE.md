---
title: "My Friends Spent 10 Minutes Squinting at Food Labels — So I Built Nibble Nanny"
published: true
tags: devchallenge, weekendchallenge, hf26challenge, gemma
canonical_url: https://dev.to/rudrasanandiya/nibble-nanny
cover_image: https://raw.githubusercontent.com/rudrasanandiya/nibble-nanny/main/static/cover.png
---

*This is a submission for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01)*

---

## What I Built

Picture this: Saturday afternoon in a crowded supermarket snack aisle.

**Sneha** is holding a biscuit packet up to the fluorescent light, squinting at 4-point font:  
*"Milk solids (1%). Wait, is sodium caseinate dairy?"*  
I tell her yes—casein is the primary milk protein that triggers her allergy. She sighs and puts the box back on the shelf.

Two feet away, **Priya** is holding a "fitness bar" proudly labeled **"NO ADDED SUGAR"**. She has no idea that the second ingredient by weight is **maltodextrin**—an industrial corn derivative with a glycemic index of **105 to 110**, spiking blood sugar faster than pure table sugar (GI 65).

Beside them, **Rahul** is pulling out his phone calculator, trying to convert grams of salt to milligrams of sodium against his doctor-mandated 1,500mg daily hypertension limit. And **Amit**, who follows strict Jain dietary rules, is frantically Googling whether mysterious code numbers like **E120** mean strawberry fruit extract or crushed insect bodies (*spoiler: it's crushed cochineal bugs*).

**Same grocery aisle. Four friends with real dietary constraints. None of them should need a biochemistry degree just to pick an afternoon snack.**

So I built **Nibble Nanny** 🍪 — an open-source, mobile-first food safety guardian powered by **Google Gemma Open-Weights Vision AI** and deterministic validation engines. One smartphone snap of a food package delivers four personalized verdicts simultaneously, unmasks deceptive corporate packaging loopholes, and explains every chemical ingredient in plain English.

---

### Meet the Nibble Nanny Squad 🦸‍♀️

Rather than generic checkboxes or walls of raw numbers, Nibble Nanny assigns each friend a dedicated guardian persona:

| Squad Member | For Friend | Dietary Guardrail | The Hidden Danger It Catches |
|---|---|---|---|
| 🥛 **Dairy Nanny** | **Sneha** | Lactose & Casein/Whey Milk Allergies | Sneaky dairy derivatives like sodium caseinate, milk solids, whey permeate, butter oil |
| 🍬 **Sugar Nanny** | **Priya** | Blood Glucose & Pre-Diabetes Caps | 30+ covert sugars (maltodextrin, high-fructose corn syrup, invert syrup, malt extract) |
| 🧂 **Salt Nanny** | **Rahul** | Hypertension & Daily Sodium Caps | Tiny 15g "serving size" tricks that hide massive whole-pack sodium payloads |
| 🌱 **Karma Nanny** | **Amit** | Jain Purity & Strict Vegetarianism | Animal rennet in cheeses, gelatin, bone char, and bug-based colorants like Carmine (E120) |
| 🕵️‍♀️ **Nanny Noir** | *Everyone* | Corporate Deception Watchdog | Trans fat 0g loopholes, sugar splitting, and carcinogenic chemical combos |

---

## Demo

- 🌐 **Live Web Application**: [https://nibble-nanny.onrender.com](https://nibble-nanny.onrender.com)
- ⚡ **Instant Interactive Demo Mode**: Don't have a snack packet on your desk? The app includes **6 preloaded supermarket presets** (Parle-G Glucose Biscuits, Maggi Masala Noodles, Choco Crunch Protein Bar, Citrus Cooler, Golden Toast Rusk, and Berry Blast Gummy Chews) that evaluate instantaneously in single clicks.

### Key Screens & Capabilities

1. **One-Tap Multi-Friend Verdicts**: Color-coded cards (**OK**, **CAREFUL**, **SKIP**) with an instant Quick Overview strip showing every friend's status at a glance.
2. **Nanny Noir Deception Radar**: Flags corporate marketing traps like **Sugar Splitting** (dividing sugar into 4 different names so none appears as ingredient #1) and the **0g Trans Fat Loophole** (using partially hydrogenated oils under 0.5g per serving).
3. **The Ingredient Classroom**: Tap any of 120+ ingredients to reveal plain-English explanations of what it is, why manufacturers use it, and what it does to your body.
4. **Mathematical Trust Gate**: Displays the **Atwater Energy Cross-Check**, recalculating calories from carbs, protein, fat, and fiber to catch misprinted or fraudulent nutrition tables.
5. **Mobile-First & Dark Mode**: Engineered for one-handed supermarket use with floating camera scan buttons and ambient dark mode.

---

## Code

{% github rudra1806/nibble-nanny %}

- **GitHub Repository**: [https://github.com/rudra1806/nibble-nanny](https://github.com/rudra1806/nibble-nanny)
- **License**: MIT (100% Free & Open Source)
- **Tech Stack**: Python 3.9+, Flask, Google Gemma Open-Weights Vision AI, Vanilla CSS (Zero Heavy Frameworks), Docker, Render Cloud.

### Clean Project Architecture

```
nibble-nanny/
├── extract.py         # Google Gemma Vision Perceptual Extraction & Structured JSON Schema
├── validate.py        # Mathematical Trust Gate (Atwater equation, unit conversions, bounds)
├── rules.py           # Squad Evaluation Engine (Sneha, Priya, Rahul, Amit deterministic rules)
├── tricks.py          # Nanny Noir Watchdog: 12 corporate deception & chemical hazard detectors
├── educate.py         # The Ingredient Classroom: 120+ curated ingredient body-impact guides
├── app.py             # Flask Web Server, REST API & Sample Packet Endpoints
├── profiles/          # Friend profiles (sneha.json, priya.json, rahul.json, amit.json)
├── eval/              # Supermarket test packets dataset & benchmark suite
├── static/            # Mobile-first responsive frontend (HTML5, CSS3 tokens, SVG icons, JS)
│   ├── logo-mascot.png  # Cute brand mascot with green shield & headset
│   ├── cover.png        # 1000x420 Dev.to cover banner
│   └── app.js           # Client-side reactivity, camera capture, and collapsible cards
└── render.yaml        # Automated Render Cloud Docker Blueprint
```

---

## How I Built It

Building a reliable food safety companion taught me a foundational lesson: **Never let a probabilistic large language model make medical or dietary decisions on its own.**

LLMs hallucinate numbers, misread tiny tables, and suffer attention drift. If a model hallucinates that sodium caseinate isn't dairy, Sneha suffers an allergic reaction. If it computes sodium wrong, Rahul overshoots his daily blood pressure allowance.

Instead, I designed a **hybrid neuro-symbolic pipeline** where open-weights AI does what it excels at (perceiving the messy physical world), while deterministic, peer-reviewed Python code enforces the safety rules.

```
       [ Packaging Photo / Camera Snap ]
                       │
                       ▼
 ┌───────────────────────────────────────────────┐
 │   LAYER 1: EYES (Google Gemma Vision Open)    │
 │   Perceives warped packaging, curved foil,    │
 │   bilingual text & FSSAI green/red dots       │
 └───────────────────────┬───────────────────────┘
                         │ Structured Raw JSON
                         ▼
 ┌───────────────────────────────────────────────┐
 │   LAYER 2: TRUST GATE (validate.py)           │
 │   Atwater Energy Cross-Check:                 │
 │   Energy = (4 × C) + (4 × P) + (9 × F) + (2 × Fib) │
 │   Catches misprints & table hallucinations    │
 └───────────────────────┬───────────────────────┘
                         │ Sanitized Values
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
 ┌───────────────┐┌───────────────┐┌───────────────┐
 │ LAYER 3:      ││ LAYER 4A:     ││ LAYER 4B:     │
 │ SQUAD RULES   ││ DECEPTION     ││ INGREDIENT    │
 │ (rules.py)    ││ RADAR         ││ CLASSROOM     │
 │ Sneha (Dairy) ││ (tricks.py)   ││ (educate.py)  │
 │ Priya (Sugar) ││ 12 Marketing  ││ 120+ Curated  │
 │ Rahul (Salt)  ││ Loopholes &   ││ Body-Impact   │
 │ Amit (Karma)  ││ Toxins Caught ││ Explanations  │
 └───────┬───────┘└───────┬───────┘└───────┬───────┘
         └───────────────┼───────────────┘
                         ▼
           [ Mobile-First Reactive UI ]
           Instant verdicts in < 15ms
```

### 1. Layer 1: The Eyes (Google Gemma Open-Weights Perceptual Core)
Reading curved, crinkled foil snack bags under grocery store fluorescent lighting is notoriously difficult for classical OCR. 

We utilize Google's **open-weights Gemma family** (`gemma-4-26b-a4b-it` and `gemma-3-4b-it`). The model is prompted with a strict structured JSON schema enforcing nullable numeric fields, serving sizes, multi-table separation (e.g. noodle cakes vs. flavor tastemakers), and allergen declarations.

### 2. Layer 2: The Trust Gate (`validate.py`)
Before any dietary rule executes, the data passes through 9 mathematical sanity checks:
- **Atwater Energy Cross-Check**: Every food label must satisfy thermodynamic reality:
  $$\text{Expected Energy (kcal)} = (4 \times \text{Carbohydrates}) + (4 \times \text{Protein}) + (9 \times \text{Total Fat}) + (2 \times \text{Fiber})$$
  If the stated calories deviate from calculated energy by more than 20%, Nibble Nanny raises a warning flag rather than guessing blindly.
- **Unit Normalization**: Automatically converts kJ to kcal and sodium to salt equivalents ($\text{Salt} = \text{Sodium} \times 2.5$).
- **Impossibility Guardrails**: Flags impossible physical metrics (e.g. sum of macronutrients exceeding 100g per 100g).

### 3. Layer 3: The Squad Evaluation Engine (`rules.py`)
Each friend's profile runs against a deterministic engine:
- **Dairy Nanny**: Evaluates 18 distinct dairy derivatives and checks both ingredient lists and allergen cross-contamination statements (*"May contain traces of milk"*).
- **Sugar Nanny**: Flags total sugars exceeding 10g/serving or 15g/100g, and scans for 32 industrial covert sugar aliases.
- **Salt Nanny**: Calculates whole-pack sodium burdens, alerting Rahul if a single snack exceeds 33% of his daily 1,500mg limit.
- **Karma Nanny**: Enforces strict Jain vegetarian principles, catching animal rennet in cheeses, gelatin (E441), bone-char sugars, and Carmine bug extract (E120).

### 4. Layer 4: The Watchdog & Classroom (`tricks.py` & `educate.py`)
- **Nanny Noir Watchdog**: Exposes 12 deceptive practices including **Sugar Splitting**, **The 0g Trans Fat Loophole**, and dangerous chemical interactions like **The Benzene Risk** (combining Sodium Benzoate E211 with Vitamin C / Ascorbic Acid E300 in acidic solutions).
- **The Ingredient Classroom**: Features a curated local database of 120+ ingredients detailing common usage, health impacts, and safety classifications (Clean Green, Caution Amber, Avoid Red).

---

## Why Does Open Innovation Matter?

Open-source and open-weight AI isn't just a philosophical preference for this project—**it is the architectural foundation that makes Nibble Nanny viable**:

1. **Sensitive Personal Health Privacy**:
   Sneha's lactose allergy, Priya's blood sugar readings, and Rahul's cardiovascular restrictions are sensitive personal medical data. In closed-API architectures, every grocery scan sends personal behavioral and dietary habits to corporate telemetry servers. With open-weight Gemma running locally on-device via Ollama, **zero personal dietary data ever leaves the user's phone**.

2. **Zero Cost Per Scan Forever**:
   My friends scan 5 to 10 snack boxes every shopping trip. Commercial vision APIs charge $0.01 to $0.03 per image. At that rate, an everyday grocery companion becomes cost-prohibitive. Open-weights AI running locally or hosted on standard container runtimes costs **$0 per scan forever**.

3. **Supermarket Basements & Offline Portability**:
   Supermarket aisles and underground grocery stores are notorious dead zones for cellular signal. Closed APIs fail completely with a spinning loader. Because Gemma 3 4B is an open-weight model, it can run locally on an iPhone, Android, or laptop, ensuring complete offline autonomy in the middle of a shopping aisle.

4. **Prompt & Schema Sovereignty**:
   Indian packaged foods frequently feature dual nutrition tables (e.g. Maggi noodles + tastemaker sachet) and statutory regional symbols (FSSAI green/red dietary dots). With open models, we could freely tune our system prompts and JSON extraction schemas in minutes without submitting feature requests to a proprietary vendor.

---

## My Agent Session

Nibble Nanny was architected, developed, and tested using AI-assisted pair programming in **Antigravity** (Google DeepMind's advanced agentic coding environment). 

- **Autonomous Verification**: The agent executed 19 comprehensive unit and integration tests across the Atwater verification math, allergy alias lookups, and corporate deception algorithms to ensure 100% test passing before deployment.
- **Visual Iteration**: Used browser subagent tools to capture live DOM state, iterate on mobile-first responsive viewport layouts, and craft our custom brand mascot and squircle app icon assets.

---

## Prize Categories

### 🌟 Best Use of Gemma ($200)
Nibble Nanny places **Google's Open-Weights Gemma family** at its perceptual core. We utilize `gemma-4-26b-a4b-it` (26B Mixture-of-Experts with Active 4B tokens) and `gemma-3-4b-it` for structured JSON perception from crumpled and reflective food packaging. Open weights give our users total data privacy, offline execution potential, and zero per-scan costs.

### 🚀 Best Use of Render ($200)
Nibble Nanny is deployed live on **Render** as a fully automated Docker web service defined by an Infrastructure-as-Code `render.yaml` blueprint. The service features automated health check endpoints (`/health`), zero-downtime rollouts, and instant branch deployments connected to GitHub.

---

## What My Friends Said (Bonus Points!)

I handed Nibble Nanny over to Sneha, Priya, Rahul, and Amit to test during their weekend grocery runs. Here is what they actually said:

> *"I’ve eaten Parle-G my entire childhood and never knew it contained milk solids. And learning that sodium caseinate is dairy saved me from a painful Sunday morning. Having Dairy Nanny highlight that in red with one photo is incredible."*  
> — **Sneha (Dairy Nanny)**

> *"I always bought that protein bar thinking it was healthy because the front said 'No Added Sugar.' Seeing Nanny Noir call out that maltodextrin was the second ingredient and actually spikes insulin faster than sugar was an absolute eye-opener."*  
> — **Priya (Sugar Nanny)**

> *"I usually give up trying to convert salt grams to sodium milligrams while standing in the aisle. Salt Nanny doing the whole-pack math and telling me instant noodles took up 60% of my daily blood pressure cap made me put the packet down immediately."*  
> — **Rahul (Salt Nanny)**

> *"Finding out that Carmine E120 is made by crushing cochineal insects horrified me. Karma Nanny gives me peace of mind that what I'm feeding my family respects our Jain vegetarian values."*  
> — **Amit (Karma Nanny)**

> *(An honest critique from Amit):*  
> *"On my first attempt, the scanner got confused because my potato chip bag was crinkled and reflecting overhead lights. Once I held the back flat for the camera, it detected everything instantly."*

---

*Built with ❤️ for Sneha, Priya, Rahul, Amit, and everyone who deserves to know the truth behind the label.* 🍪
