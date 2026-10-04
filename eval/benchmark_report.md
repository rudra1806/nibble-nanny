# 🍪 Nibble Nanny — Benchmark & Evaluation Matrix

> **Hacktoberfest Weekend Challenge: Build for a Friend**  
> Total Packets Evaluated: **6** · Pipeline Execution Time: **0.03s**

---

## 1. The Squad Verdict Matrix

| # | Product Name | Category | 🥛 Dairy (Sneha) | 🍬 Sugar (Priya) | 🧂 Salt (Rahul) | 🌱 Karma (Amit) | 🕵️‍♀️ Tricks | Latency |
|---|---|---|---|---|---|---|---|---|
| 1 | **Parle-G Glucose Biscuits** | Biscuits / Cookies | ❌ SKIP | ❌ SKIP | ✅ OK | ✅ OK | 1 flagged | 12.12ms |
| 2 | **Maggi 2-Minute Masala Noodles** | Instant Noodles | ❌ SKIP | ⚠️ CAREFUL | ❌ SKIP | ❌ SKIP | 0 flagged | 6.97ms |
| 3 | **Choco Crunch 'High Protein' Bar** | Sports Nutrition / Protein | ❌ SKIP | ❌ SKIP | ✅ OK | ⚠️ CAREFUL | 2 flagged | 2.53ms |
| 4 | **Citrus Splash Orange Beverage** | Beverages | ✅ OK | ❌ SKIP | ⚠️ CAREFUL | ✅ OK | 3 flagged | 3.14ms |
| 5 | **Golden Premium Toast Rusk** | Bakery / Toast | ✅ OK | ❌ SKIP | ✅ OK | ✅ OK | 2 flagged | 3.55ms |
| 6 | **Berry Blast Gummy Chews** | Confectionery / Candy | ✅ OK | ❌ SKIP | ✅ OK | ❌ SKIP | 3 flagged | 2.89ms |

---

## 2. Detailed Deception & Chemical Watchdog Highlights

### 📦 Parle-G Glucose Biscuits
- ⚠️ **SUGAR IS A PRIMARY INGREDIENT**

### 📦 Choco Crunch 'High Protein' Bar
- ⚠️ **SUGAR SPLITTING DETECTED**
- ⚠️ **PROTEIN HALO vs SUGAR REALITY**

### 📦 Citrus Splash Orange Beverage
- ⚠️ **DANGEROUS COCKTAIL: BENZENE RISK**
- ⚠️ **SUGAR IS A PRIMARY INGREDIENT**
- ⚠️ **HEALTH-HALO MARKETING BUZZWORDS**

### 📦 Golden Premium Toast Rusk
- ⚠️ **THE '0g TRANS FAT' REGULATORY LOOPHOLE**
- ⚠️ **SUGAR IS A PRIMARY INGREDIENT**

### 📦 Berry Blast Gummy Chews
- ⚠️ **SUGAR SPLITTING DETECTED**
- ⚠️ **SUGAR IS A PRIMARY INGREDIENT**
- ⚠️ **'NO ADDED SUGAR' NATURAL SUGAR TRAP**

---

## 3. Honest Failure Analysis & Production Constraints

| Failure Mode | Frequency | Mitigation / Engineering Resolution |
|---|---|---|
| **Curved Bottle Surface Glare** | 2 / 15 test photos | Prompt instructs Gemma to return `confidence_notes` with lighting flags; trust gate rejects corrupted values. |
| **Missing Fiber in Nutrition Table** | 4 / 15 packets | Atwater cross-check formula defaults missing fiber to 0g, which under-calculates stated calories (the safer direction). |
| **Decimal Point OCR Drift (0.5g -> 5g)** | 1 / 15 tests | Flagged automatically by Atwater energy equation check ($4C+4P+9F \approx \text{stated kcal}$), triggering trust-gate rejection. |
| **Multi-Table Labels (Masala + Noodle)** | 1 / 15 packets | Handled via `multiple_tables: true` flag in extraction schema, using combined 'as sold' values. |

---
*Benchmark generated automatically by `eval/eval_runner.py`.*