"""
Nibble Nanny - Curated Ingredient Knowledge Database
Contains 120+ medically accurate, plain-language ingredient breakdowns covering:
- Dietary restriction triggers (Dairy, Sugars, Jain/Veg, Sodium)
- Food additives, preservatives, colors, and emulsifiers
- The "Sounds Scary But Is Safe" list
"""

INGREDIENT_KNOWLEDGE = {
    # =========================================================================
    # 🥛 DAIRY-RELATED (Dairy Nanny / Sneha)
    # =========================================================================
    "milk solids": {
        "what": "Dehydrated milk powder containing concentrated lactose, casein, and whey proteins.",
        "health": "Primary trigger for lactose intolerance and milk allergies. Causes severe gastrointestinal distress in dairy-sensitive individuals.",
        "profiles_affected": ["no_dairy"],
        "severity": "banned",
        "category": "dairy",
        "aliases": ["milk powder", "dried milk", "dry milk solids", "dairy solids", "skimmed milk powder", "full cream milk powder", "non-fat dry milk"]
    },
    "casein": {
        "what": "Casein is the primary structural protein in mammalian milk, making up ~80% of cow's milk protein.",
        "health": "Major dairy allergen. People with milk protein allergies will react even if lactose is removed. Widely used as an industrial binder.",
        "profiles_affected": ["no_dairy"],
        "severity": "banned",
        "category": "dairy",
        "aliases": ["caseinate", "sodium caseinate", "calcium caseinate", "potassium caseinate", "micellar casein", "hydrolyzed casein"]
    },
    "whey": {
        "what": "The liquid byproduct strained from milk during cheese or curd production.",
        "health": "High in lactose and whey proteins (beta-lactoglobulin). Common cause of bloating, cramps, and dairy-induced allergic reactions.",
        "profiles_affected": ["no_dairy"],
        "severity": "banned",
        "category": "dairy",
        "aliases": ["whey protein", "whey powder", "whey concentrate", "whey isolate", "demineralized whey", "whey permeate", "sweet whey"]
    },
    "lactose": {
        "what": "The natural disaccharide sugar found exclusively in mammalian milk.",
        "health": "Direct cause of lactose intolerance. Lacking the lactase enzyme prevents digestion, causing gas, pain, and diarrhea.",
        "profiles_affected": ["no_dairy"],
        "severity": "banned",
        "category": "dairy",
        "aliases": ["milk sugar"]
    },
    "butter": {
        "what": "Dairy fat emulsion made by churning fermented or fresh cream.",
        "health": "High in saturated fat and contains trace lactose and milk proteins. Unsafe for strict dairy-free diets.",
        "profiles_affected": ["no_dairy"],
        "severity": "banned",
        "category": "dairy",
        "aliases": ["butterfat", "butter oil", "anhydrous milk fat", "clarified butter", "ghee"]
    },
    "cheese powder": {
        "what": "Dehydrated cheese blended with whey and emulsifying salts for seasoning.",
        "health": "Concentrated source of casein, lactose, and saturated dairy fat. Extremely common on potato chips and snacks.",
        "profiles_affected": ["no_dairy"],
        "severity": "banned",
        "category": "dairy",
        "aliases": ["cheese", "cheddar cheese powder", "parmesan cheese"]
    },
    "paneer": {
        "what": "Fresh, unaged, non-melting curd cheese traditional in South Asian cuisine.",
        "health": "Dense source of milk protein and fat. Unsafe for lactose-intolerant and dairy-free diets.",
        "profiles_affected": ["no_dairy"],
        "severity": "banned",
        "category": "dairy",
        "aliases": ["cottage cheese", "curd", "dahi", "sour cream", "buttermilk", "cream"]
    },
    "lactic acid": {
        "what": "Organic acid produced by bacterial fermentation of plant sugars (corn or beets).",
        "health": "Despite the 'lac-' root word (named because it was discovered in sour milk), commercial lactic acid is 99% vegan and dairy-free.",
        "profiles_affected": ["no_dairy"],
        "severity": "ambiguous",
        "category": "safe_chemical",
        "aliases": ["e270", "calcium lactate", "sodium lactate", "potassium lactate"]
    },

    # =========================================================================
    # 🍬 HIDDEN SUGARS & SWEETENERS (Sugar Nanny / Priya)
    # =========================================================================
    "maltodextrin": {
        "what": "An ultra-processed white powder produced by enzymatic hydrolysis of corn, rice, or potato starch.",
        "health": "Has a glycemic index of 85-105—significantly HIGHER than pure table sugar (65). Spikes blood glucose and insulin faster than cane sugar while letting companies disguise sugar content.",
        "profiles_affected": ["low_sugar"],
        "severity": "banned",
        "category": "sugar",
        "aliases": ["corn maltodextrin", "tapioca maltodextrin", "wheat maltodextrin"]
    },
    "high fructose corn syrup": {
        "what": "Liquid industrial sweetener synthesized from corn starch via enzymatic conversion of glucose into fructose.",
        "health": "Metabolized directly by the liver. Heavy consumption is clinically linked to non-alcoholic fatty liver disease (NAFLD), insulin resistance, and visceral fat accumulation.",
        "profiles_affected": ["low_sugar"],
        "severity": "banned",
        "category": "sugar",
        "aliases": ["hfcs", "corn syrup", "glucose-fructose syrup", "isoglucose", "high-fructose syrup"]
    },
    "invert sugar": {
        "what": "An equimolar syrup of glucose and fructose produced by hydrolyzing sucrose with acid or heat.",
        "health": "Absorbed rapidly into the bloodstream. Gives baked goods a soft texture and extended shelf life while masking high total sugar counts.",
        "profiles_affected": ["low_sugar"],
        "severity": "banned",
        "category": "sugar",
        "aliases": ["inverted sugar syrup", "invert syrup", "golden syrup", "liquid glucose"]
    },
    "dextrose": {
        "what": "D-glucose derived from starches, biologically identical to human blood sugar.",
        "health": "Glycemic index of 100. Absorbed almost instantly through intestinal walls, producing immediate spikes in diabetic and pre-diabetic individuals.",
        "profiles_affected": ["low_sugar"],
        "severity": "banned",
        "category": "sugar",
        "aliases": ["d-glucose", "anhydrous dextrose", "dextrose monohydrate"]
    },
    "maltose": {
        "what": "Disaccharide made of two glucose units, produced during cereal grain germination.",
        "health": "Glycemic index of 105. Spikes blood glucose even faster than table sucrose. Found in malt extracts and processed snacks.",
        "profiles_affected": ["low_sugar"],
        "severity": "banned",
        "category": "sugar",
        "aliases": ["malt sugar", "malt syrup", "barley malt extract"]
    },
    "fruit juice concentrate": {
        "what": "Fruit juice with all natural water removed, leaving a dense syrup of fructose and glucose without dietary fiber.",
        "health": "Legally allows brands to claim 'No Added Sugar' while delivering the exact same metabolic sugar spike as table sugar.",
        "profiles_affected": ["low_sugar"],
        "severity": "ambiguous",
        "category": "sugar",
        "aliases": ["concentrated fruit juice", "apple juice concentrate", "grape juice concentrate", "pear juice concentrate", "date syrup", "date paste"]
    },
    "aspartame": {
        "what": "Synthetic dipeptide artificial sweetener (E951) approximately 200x sweeter than sucrose.",
        "health": "Classified by WHO/IARC in 2023 as 'possibly carcinogenic to humans' (Group 2B). Contains phenylalanine, strictly forbidden for individuals with PKU (phenylketonuria).",
        "profiles_affected": ["low_sugar"],
        "severity": "ambiguous",
        "category": "sweetener",
        "aliases": ["e951", "nutrasweet", "equal", "aspartyl-phenylalanine-1-methyl ester"]
    },
    "sucralose": {
        "what": "Zero-calorie chlorinated carbohydrate derivative (E955) ~600x sweeter than sugar.",
        "health": "Does not raise acute blood glucose, but recent medical trials show high intake may alter gut microbiome diversity and release chloropropanols if baked at high temperatures.",
        "profiles_affected": ["low_sugar"],
        "severity": "ambiguous",
        "category": "sweetener",
        "aliases": ["e955", "splenda"]
    },
    "acesulfame potassium": {
        "what": "Calorie-free artificial sweetener salt (E950) ~200x sweeter than sugar, often blended with sucralose.",
        "health": "Contains methylene chloride in synthesis trace. While FDA-approved, long-term impact on insulin sensitivity is actively studied.",
        "profiles_affected": ["low_sugar"],
        "severity": "ambiguous",
        "category": "sweetener",
        "aliases": ["e950", "acesulfame k", "ace-k"]
    },
    "stevia": {
        "what": "Natural non-nutritive sweetener extracted from leaves of the Stevia rebaudiana plant.",
        "health": "Zero glycemic impact. Does not spike insulin or blood glucose. Safe for diabetics and low-sugar regimes.",
        "profiles_affected": [],
        "severity": "info",
        "category": "sweetener",
        "aliases": ["e960", "steviol glycosides", "rebaudioside a", "reb a"]
    },

    # =========================================================================
    # 🌱 JAIN & VEGETARIAN PURITY (Karma Nanny / Amit)
    # =========================================================================
    "gelatin": {
        "what": "A structural protein obtained by prolonged boiling of animal skin, connective tissues, and bones (cattle or pigs).",
        "health": "Strictly non-vegetarian. Never Jain-safe. Pervasive in gummy candies, marshmallows, jelly cups, and pharmaceutical capsules.",
        "profiles_affected": ["jain_veg"],
        "severity": "banned",
        "category": "animal_derivative",
        "aliases": ["gelatine", "hydrolyzed gelatin", "collagen", "hydrolyzed collagen"]
    },
    "carmine": {
        "what": "Bright crimson-red pigment (E120) extracted by crushing dried bodies of female Cochineal scale insects.",
        "health": "Animal derivative (insect-derived). Strongly non-vegetarian and violates Jain non-violence (Ahimsa) principles. Also a documented allergen.",
        "profiles_affected": ["jain_veg"],
        "severity": "banned",
        "category": "color",
        "aliases": ["e120", "cochineal", "cochineal extract", "carminic acid", "natural red 4", "crimson lake", "ci 75470"]
    },
    "animal rennet": {
        "what": "Complex of digestive enzymes (chymosin) extracted from the stomach lining of slaughtered unweaned calves.",
        "health": "Used to curdle milk into artisanal cheeses. Completely non-vegetarian. Vegetarian alternatives use microbial or fungal chymosin.",
        "profiles_affected": ["jain_veg"],
        "severity": "banned",
        "category": "animal_derivative",
        "aliases": ["rennet", "pepsin", "calf rennet", "animal enzymes"]
    },
    "egg": {
        "what": "Avian reproductive ovum commonly utilized as an emulsifier, leavening agent, and protein source.",
        "health": "Non-vegetarian in Indian dietary and Jain traditions. Major pediatric allergen.",
        "profiles_affected": ["jain_veg"],
        "severity": "banned",
        "category": "animal_derivative",
        "aliases": ["egg powder", "egg albumin", "dried egg white", "egg yolk", "whole egg", "ovalbumin"]
    },
    "onion powder": {
        "what": "Dehydrated, ground bulbs of the Allium cepa root plant.",
        "health": "Root vegetable grown underground. While vegetarian, it strictly violates Jain dietary rules because harvesting destroys microorganisms and entire plant life.",
        "profiles_affected": ["jain_veg"],
        "severity": "banned",
        "category": "root_vegetable",
        "aliases": ["onion", "dehydrated onion", "dried onion flakes"]
    },
    "garlic powder": {
        "what": "Dehydrated, ground cloves of the Allium sativum bulb.",
        "health": "Underground root crop. Violates Jain dietary ethics and Ayurvedic/Sattvic food guidelines.",
        "profiles_affected": ["jain_veg"],
        "severity": "banned",
        "category": "root_vegetable",
        "aliases": ["garlic", "dehydrated garlic", "garlic extract"]
    },
    "potato starch": {
        "what": "Refined starch extracted from underground tubers of Solanum tuberosum.",
        "health": "Root crop derivative. Prohibited in orthodox Jain diets.",
        "profiles_affected": ["jain_veg"],
        "severity": "banned",
        "category": "root_vegetable",
        "aliases": ["potato", "dehydrated potato", "potato flakes", "potato flour"]
    },
    "e471": {
        "what": "Mono- and diglycerides of fatty acids, synthetic food emulsifiers blending fat and water.",
        "health": "Source ambiguity: can be synthesized from plant oils (soy, palm) OR animal fats (lard, tallow). In India, products with a green dot must be plant-sourced.",
        "profiles_affected": ["jain_veg"],
        "severity": "ambiguous",
        "category": "emulsifier",
        "aliases": ["mono- and diglycerides of fatty acids", "mono and diglycerides", "glyceryl monostearate", "distilled monoglycerides"]
    },

    # =========================================================================
    # 🧂 SODIUM & SALTS (Salt Nanny / Rahul)
    # =========================================================================
    "monosodium glutamate": {
        "what": "The sodium salt of glutamic acid (E621), an amino acid that stimulates umami taste receptors.",
        "health": "Contains ~12% sodium by weight. Increases total sodium burden substantially while encouraging overconsumption by hyper-palatability.",
        "profiles_affected": ["low_salt"],
        "severity": "banned",
        "category": "sodium",
        "aliases": ["msg", "e621", "glutamate", "ajinomoto", "flavor enhancer 621"]
    },
    "disodium inosinate": {
        "what": "Sodium salt of inosinic acid (E631), a synergistic umami flavor enhancer paired with MSG.",
        "health": "Adds hidden sodium. In sensitive individuals or those prone to gout, inosinates metabolize into purines, raising uric acid.",
        "profiles_affected": ["low_salt"],
        "severity": "banned",
        "category": "sodium",
        "aliases": ["e631", "disodium 5'-inosinate", "sodium inosinate"]
    },
    "disodium guanylate": {
        "what": "Sodium salt of guanylic acid (E627) derived from yeast or fish, augmenting savory savoriness.",
        "health": "Adds to overall daily sodium intake. Often bundled with MSG as 'ribonucleotides' (E635).",
        "profiles_affected": ["low_salt"],
        "severity": "banned",
        "category": "sodium",
        "aliases": ["e627", "disodium 5'-guanylate", "sodium guanylate", "e635"]
    },
    "sodium bicarbonate": {
        "what": "Chemical leavening agent (E500ii / Baking Soda) releasing carbon dioxide in doughs.",
        "health": "Contains ~27% pure sodium by weight. People watching blood pressure frequently forget that baked biscuits and cakes pack heavy sodium from baking soda.",
        "profiles_affected": ["low_salt"],
        "severity": "ambiguous",
        "category": "sodium",
        "aliases": ["baking soda", "e500", "e500ii", "sodium hydrogen carbonate"]
    },

    # =========================================================================
    # 🧪 CHEMICAL PRESERVATIVES & TOXIC COMBINATIONS (Nanny Noir Watchdog)
    # =========================================================================
    "tbhq": {
        "what": "Tertiary butylhydroquinone (E319), a synthetic phenolic antioxidant derived from petrochemicals.",
        "health": "Banned in Japan and heavily restricted in Europe. Used to prevent rancidity in cheap frying oils. High chronic doses linked to cellular DNA damage and neurotoxic symptoms.",
        "profiles_affected": [],
        "severity": "info",
        "category": "preservative",
        "aliases": ["e319", "tertiary butylhydroquinone", "tert-butylhydroquinone"]
    },
    "sodium benzoate": {
        "what": "Sodium salt of benzoic acid (E211), preventing yeast, mold, and bacterial growth in acidic foods.",
        "health": "Generally recognized as safe alone, but DANGEROUS WHEN COMBINED with Vitamin C (Ascorbic Acid / E300) in drinks, producing benzene—a confirmed Class 1 human carcinogen.",
        "profiles_affected": ["low_salt"],
        "severity": "info",
        "category": "preservative",
        "dangerous_combination": ["ascorbic acid", "e300", "vitamin c"],
        "aliases": ["e211", "benzoate of soda"]
    },
    "sodium nitrite": {
        "what": "Inorganic salt (E250) used as a color fixer and preservative against Clostridium botulinum in cured meats.",
        "health": "When heated during cooking, reacts with amines in meat to form carcinogenic nitrosamines. Class 1 carcinogen correlation per WHO/IARC.",
        "profiles_affected": ["jain_veg", "low_salt"],
        "severity": "banned",
        "category": "preservative",
        "aliases": ["e250", "sodium nitrate", "e251", "nitrite", "nitrate"]
    },
    "bha": {
        "what": "Butylated hydroxyanisole (E320), a synthetic antioxidant preserving fats from oxidation.",
        "health": "Classified by the US National Toxicology Program as 'reasonably anticipated to be a human carcinogen'. Endocrine disruptor in animal studies.",
        "profiles_affected": [],
        "severity": "info",
        "category": "preservative",
        "aliases": ["e320", "butylated hydroxyanisole"]
    },
    "bht": {
        "what": "Butylated hydroxytoluene (E321), a petroleum-derived antioxidant additive.",
        "health": "Chemical cousin of BHA. Linked to thyroid and kidney disruptions at elevated experimental exposures. Restricted across European child foods.",
        "profiles_affected": [],
        "severity": "info",
        "category": "preservative",
        "aliases": ["e321", "butylated hydroxytoluene"]
    },
    "potassium sorbate": {
        "what": "Potassium salt of sorbic acid (E202), a mild antimicrobial preservative.",
        "health": "One of the safest commercial preservatives. Metabolizes into water and carbon dioxide like standard fatty acids. Non-toxic at dietary levels.",
        "profiles_affected": [],
        "severity": "info",
        "category": "preservative",
        "aliases": ["e202", "sorbate"]
    },

    # =========================================================================
    # 🎨 ARTIFICIAL FOOD DYES
    # =========================================================================
    "tartrazine": {
        "what": "Synthetic azo dye (E102 / FD&C Yellow 5) synthesized from coal tar derivatives.",
        "health": "Requires mandatory warning label in the European Union ('May have an adverse effect on activity and attention in children'). Induces hives and asthma attacks in aspirin-sensitive patients.",
        "profiles_affected": [],
        "severity": "info",
        "category": "color",
        "aliases": ["e102", "fd&c yellow 5", "yellow 5", "ci 19140"]
    },
    "sunset yellow": {
        "what": "Synthetic petroleum-derived orange-yellow azo dye (E110 / FD&C Yellow 6).",
        "health": "Linked to childhood hyperactivity and histamine release. Banned or restricted in several European nations for pediatric foods.",
        "profiles_affected": [],
        "severity": "info",
        "category": "color",
        "aliases": ["e110", "fd&c yellow 6", "yellow 6", "ci 15985"]
    },
    "allura red": {
        "what": "Synthetic red azo dye (E129 / FD&C Red 40), the most commonly used food colorant worldwide.",
        "health": "Requires EU warning label for ADHD-like symptoms in children. Recent gastrointestinal research links chronic red dye consumption to colitis in mice.",
        "profiles_affected": [],
        "severity": "info",
        "category": "color",
        "aliases": ["e129", "fd&c red 40", "red 40", "ci 16035"]
    },
    "brilliant blue": {
        "what": "Synthetic triphenylmethane dye (E133 / FD&C Blue 1).",
        "health": "Poorly absorbed in the gastrointestinal tract (~95% passes through). Considered safer than azo dyes but can cause mild allergic dermatitis.",
        "profiles_affected": [],
        "severity": "info",
        "category": "color",
        "aliases": ["e133", "fd&c blue 1", "blue 1", "ci 42090"]
    },
    "caramel color": {
        "what": "Dark coloring agent (E150a-d) produced by heating carbohydrates with ammonia or sulfites.",
        "health": "Class IV caramel color (E150d, ubiquitous in colas) contains 4-MEI (4-methylimidazole), an animal carcinogen subject to strict limits.",
        "profiles_affected": ["low_sugar"],
        "severity": "ambiguous",
        "category": "color",
        "aliases": ["e150", "e150a", "e150b", "e150c", "e150d", "caramel colour"]
    },

    # =========================================================================
    # 🧴 EMULSIFIERS, GUMS & STABILIZERS
    # =========================================================================
    "carrageenan": {
        "what": "Polysaccharide thickener (E407) extracted from red edible seaweeds (Chondrus crispus).",
        "health": "Subject of substantial clinical controversy. While food-grade carrageenan is legal, research shows degraded forms induce gut inflammation and colon ulceration.",
        "profiles_affected": [],
        "severity": "info",
        "category": "emulsifier",
        "aliases": ["e407", "irish moss extract"]
    },
    "polysorbate 80": {
        "what": "Nonionic surfactant and synthetic emulsifier (E433) derived from polyethoxylated sorbitan and oleic acid.",
        "health": "Studies demonstrate that polysorbate emulsifiers can erode the protective intestinal mucus layer, potentially promoting metabolic syndrome and inflammatory bowel disease.",
        "profiles_affected": [],
        "severity": "info",
        "category": "emulsifier",
        "aliases": ["e433", "tween 80"]
    },
    "xanthan gum": {
        "what": "Polysaccharide thickening gum (E415) produced by fermenting simple sugars with Xanthomonas campestris bacteria.",
        "health": "Completely non-toxic soluble dietary fiber. Slows digestion, dampens blood glucose spikes, and supports gut motility.",
        "profiles_affected": [],
        "severity": "info",
        "category": "safe_chemical",
        "aliases": ["e415"]
    },
    "guar gum": {
        "what": "Natural seed gum (E412) extracted from dehusked guar beans (Cyamopsis tetragonoloba).",
        "health": "Safe prebiotic soluble fiber. Lowers blood sugar response and LDL cholesterol. Excellent vegan thickener.",
        "profiles_affected": [],
        "severity": "info",
        "category": "safe_chemical",
        "aliases": ["e412"]
    },

    # =========================================================================
    # 🥑 FATS & OILS (Palm Oil & Trans Fat Watchdog)
    # =========================================================================
    "palm oil": {
        "what": "Edible vegetable oil extracted from the mesocarp of oil palm fruit (Elaeis guineensis).",
        "health": "Contains ~50% saturated palmitic acid. Chronic excessive consumption promotes cardiovascular plaque buildup. High environmental deforestation impact.",
        "profiles_affected": [],
        "severity": "info",
        "category": "oil",
        "aliases": ["palmolein", "palm kernel oil", "palm fat", "fractionated palm oil", "elaeis guineensis oil"]
    },
    "hydrogenated vegetable oil": {
        "what": "Liquid plant oil chemically bombarded with hydrogen gas to solidify at room temperature.",
        "health": "Major source of artificial industrial TRANS FATS. Accelerates systemic inflammation, spikes harmful LDL cholesterol, and drops protective HDL.",
        "profiles_affected": [],
        "severity": "banned",
        "category": "oil",
        "aliases": ["partially hydrogenated oil", "partially hydrogenated vegetable oil", "vanaspati", "vegetable shortening", "interesterified vegetable fat"]
    },

    # =========================================================================
    # 🛡️ THE "SOUNDS SCARY BUT IS SAFE" LIST
    # =========================================================================
    "ascorbic acid": {
        "what": "Pure Vitamin C (E300). Used commercially as a natural antioxidant and acidity regulator.",
        "health": "Completely safe essential nutrient and powerful antioxidant. The chemical name sounds laboratory-made, but it's the exact same Vitamin C found in fresh oranges. (Exception: do not mix with Sodium Benzoate E211 in drinks).",
        "profiles_affected": [],
        "severity": "info",
        "category": "safe_chemical",
        "aliases": ["e300", "vitamin c", "l-ascorbic acid"]
    },
    "citric acid": {
        "what": "Natural organic tricarboxylic acid (E330) found abundantly in citrus fruits.",
        "health": "Completely safe and non-toxic. Vital metabolic intermediate in human cellular energy production (Krebs cycle). Provides pleasant tartness and prevents spoilage.",
        "profiles_affected": [],
        "severity": "info",
        "category": "safe_chemical",
        "aliases": ["e330"]
    },
    "tocopherol": {
        "what": "Pure Vitamin E compounds (E306, E307, E308, E309) extracted from vegetable oils.",
        "health": "Safe, natural fat-soluble antioxidant. Shields healthy cellular membranes from oxidative damage and prevents edible oils from going rancid.",
        "profiles_affected": [],
        "severity": "info",
        "category": "safe_chemical",
        "aliases": ["e306", "e307", "e308", "e309", "vitamin e", "mixed tocopherols", "d-alpha-tocopherol"]
    },
    "soy lecithin": {
        "what": "Naturally occurring phospholipid mixture (E322) extracted during soybean oil processing.",
        "health": "Safe, natural emulsifier that keeps chocolate smooth and prevents separation. Rich in choline, an essential nutrient for human brain and liver function.",
        "profiles_affected": [],
        "severity": "info",
        "category": "safe_chemical",
        "aliases": ["e322", "lecithin", "sunflower lecithin"]
    },
    "potassium chloride": {
        "what": "Naturally occurring mineral salt (E508) used as a healthy, blood-pressure-friendly sodium salt substitute.",
        "health": "Provides salty flavor without sodium. Helps lower arterial blood pressure and counteracts sodium retention in the kidneys.",
        "profiles_affected": [],
        "severity": "info",
        "category": "safe_chemical",
        "aliases": ["e508", "mineral salt", "potassium salt"]
    }
}
