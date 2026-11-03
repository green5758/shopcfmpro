import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "ShopCFMPro"
SITE_TAGLINE = "Air Compressor CFM, Tank Gallon & Welder Amperage Sizing Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d"

# Cumulative Daily Review Epoch (+1 new standalone product review article unlocked every single day)
LAUNCH_EPOCH = datetime.date(2026, 11, 1)

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/shopcfmpro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "shopcfmpro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "California Air Tools 10020C Ultra Quiet & Oil-Free 2.0 HP 10-Gallon Air Compressor",
        "category": "Ultra-Quiet Air Compressor",
        "rating": "4.7 ★ (4,800+ reviews)",
        "badge": "#1 Quiet Garage Compressor",
        "specs": "6.40 CFM @ 40 PSI / 5.30 CFM @ 90 PSI | Only 70 dB Noise | Oil-Free Dual Piston Pump",
        "keyword": "California+Air+Tools+10020C+Ultra+Quiet+10+Gallon+Air+Compressor"
    },
    {
        "title": "DEWALT 60-Gallon Vertical Stationary Electric Air Compressor (15.0 CFM @ 90 PSI, 240V)",
        "category": "Heavy-Duty Shop Compressor",
        "rating": "4.7 ★ (3,900+ reviews)",
        "badge": "#1 60-Gallon Shop Unit",
        "specs": "3.7 HP Running | 13.4 CFM @ 100 PSI / 11.5 CFM @ 175 PSI | Cast Iron Oil-Lubricated",
        "keyword": "DEWALT+60+Gallon+Vertical+Stationary+Air+Compressor+DXCMV5046055"
    },
    {
        "title": "YESWELDER MIG-205DS Pro 200-Amp Multi-Process MIG / Spool Gun / Flux / Lift TIG / Stick Welder",
        "category": "Dual-Voltage Multi-Process Welder",
        "rating": "4.7 ★ (7,600+ reviews)",
        "badge": "#1 Best-Selling MIG Welder",
        "specs": "110V/220V Dual Voltage | 200A Output (Welds up to 3/8\" Steel) | Synergic Digital LCD",
        "keyword": "YESWELDER+MIG+205DS+Pro+200A+Multi+Process+MIG+Welder"
    },
    {
        "title": "Ingersoll Rand 2235TiMAX 1/2-Inch Drive Titanium Heavy-Duty Air Impact Wrench",
        "category": "Pneumatic Impact Wrench",
        "rating": "4.8 ★ (16,400+ reviews)",
        "badge": "Mechanic's #1 Impact Gun",
        "specs": "1,350 ft-lbs Nut-Busting Torque | Titanium Hammer Case | Weighs Only 4.6 lbs | 5.0 CFM",
        "keyword": "Ingersoll+Rand+2235TiMAX+1+2+Inch+Air+Impact+Wrench"
    },
    {
        "title": "DEWALT 20-Gallon 200 PSI High-Pressure Portable Vertical Air Compressor",
        "category": "Portable Garage Compressor",
        "rating": "4.7 ★ (5,100+ reviews)",
        "badge": "Best 120V Portable Tank",
        "specs": "5.0 SCFM @ 90 PSI | 200 PSI Max Tank Pressure | 78 dB Quiet Operation | Pneumatic Tires",
        "keyword": "DEWALT+20+Gallon+200+PSI+Vertical+Air+Compressor+DXCM201"
    },
    {
        "title": "PrimeWeld TIG225X 225-Amp AC/DC TIG & Stick Welder with Pulse (110V/220V)",
        "category": "AC/DC Aluminum & Steel TIG",
        "rating": "4.9 ★ (4,200+ reviews)",
        "badge": "Highest Rated AC/DC TIG",
        "specs": "Welds Aluminum, Stainless & Chromoly | Genuine CK17 Flex Torch & Foot Pedal | 3-Yr Warranty",
        "keyword": "PrimeWeld+TIG225X+225+Amp+AC+DC+TIG+Welder+with+Pulse"
    },
    {
        "title": "YESWELDER CUT-55DS Pro 55-Amp Non-Touch Pilot Arc Air Plasma Cutter (110V/220V)",
        "category": "Pilot Arc Plasma Cutter",
        "rating": "4.7 ★ (5,500+ reviews)",
        "badge": "#1 Garage Plasma Cutter",
        "specs": "Cuts Through Rusty/Painted 1/2\" Clean & 3/4\" Severance | Requires 4.5 CFM @ 60–75 PSI",
        "keyword": "YESWELDER+CUT+55DS+Pro+55+Amp+Pilot+Arc+Plasma+Cutter"
    },
    {
        "title": "Campbell Hausfeld / Milton 3-Stage Desiccant & Coalescing Compressed Air Dryer System",
        "category": "HVLP Paint & Plasma Air Dryer",
        "rating": "4.8 ★ (3,300+ reviews)",
        "badge": "#1 Moisture & Oil Separator",
        "specs": "5-Micron + 0.01-Micron Coalescing + Desiccant Beads | Essential for HVLP Paint & Plasma",
        "keyword": "3+Stage+Compressed+Air+Drying+System+Regulator+Filter+HVLP+Plasma"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "DEWALT 60-Gallon Vertical (240V)",
        "type": "Stationary Cast-Iron Compressor",
        "cfm_output": "13.4 – 15.0 CFM @ 90 PSI",
        "tank_power": "60 Gal | 175 PSI | 240V",
        "best_for": "Sandblasting, DA Sanders & HVLP Paint",
        "rating": "4.7 / 5.0 ★",
        "keyword": "DEWALT+60+Gallon+Vertical+Stationary+Air+Compressor"
    },
    {
        "model": "California Air Tools 10020C",
        "type": "Ultra-Quiet Oil-Free Compressor",
        "cfm_output": "5.30 CFM @ 90 PSI",
        "tank_power": "10 Gal | 125 PSI | 110V (70 dB)",
        "best_for": "Impact Guns, Plasma Cutting & Nailers",
        "rating": "4.7 / 5.0 ★",
        "keyword": "California+Air+Tools+10020C+Ultra+Quiet+10+Gallon+Air+Compressor"
    },
    {
        "model": "DEWALT DXCM201 20-Gallon",
        "type": "High-Pressure Portable Vertical",
        "cfm_output": "5.00 CFM @ 90 PSI",
        "tank_power": "20 Gal | 200 PSI | 120V",
        "best_for": "Home Garage Mechanics & Tire/Suspension",
        "rating": "4.7 / 5.0 ★",
        "keyword": "DEWALT+20+Gallon+200+PSI+Vertical+Air+Compressor+DXCM201"
    },
    {
        "model": "YESWELDER MIG-205DS Pro",
        "type": "4-in-1 Synergic MIG Welder",
        "cfm_output": "30A – 200A Welding Output",
        "tank_power": "110V / 220V Dual Voltage",
        "best_for": "24-Gauge Sheet Metal up to 3/8\" Plate",
        "rating": "4.7 / 5.0 ★",
        "keyword": "YESWELDER+MIG+205DS+Pro+200A+Multi+Process+MIG+Welder"
    },
    {
        "model": "PrimeWeld TIG225X AC/DC",
        "type": "AC/DC Pulse TIG & Stick Welder",
        "cfm_output": "10A – 225A AC/DC Output",
        "tank_power": "110V / 220V | 200Hz Pulse",
        "best_for": "Precision Aluminum, Stainless & Chromoly",
        "rating": "4.9 / 5.0 ★",
        "keyword": "PrimeWeld+TIG225X+225+Amp+AC+DC+TIG+Welder+with+Pulse"
    },
    {
        "model": "YESWELDER CUT-55DS Pro",
        "type": "Non-Touch Pilot Arc Plasma",
        "cfm_output": "20A – 55A Plasma Arc (4.5 CFM)",
        "tank_power": "110V / 220V | Cuts 1/2\" – 3/4\"",
        "best_for": "Cutting Rusty, Painted & Expanded Steel",
        "rating": "4.7 / 5.0 ★",
        "keyword": "YESWELDER+CUT+55DS+Pro+55+Amp+Pilot+Arc+Plasma+Cutter"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-california-air-tools-10020c-vs-dewalt-20-gallon-compressor",
        "title": "California Air Tools 10020C vs. DEWALT 20-Gallon 200 PSI: Ultra-Quiet vs. High-Pressure Tank",
        "product_a": "California Air Tools 10020C (2.0 HP)",
        "product_b": "DEWALT DXCM201 20-Gallon (200 PSI)",
        "winner_badge": "Quietest 70 dB Pump vs. Longest Stored Air Buffer",
        "keyword_a": "California+Air+Tools+10020C+Ultra+Quiet+10+Gallon+Air+Compressor",
        "keyword_b": "DEWALT+20+Gallon+200+PSI+Vertical+Air+Compressor+DXCM201",
        "summary": "Compare continuous CFM @ 90 PSI delivery, decibel noise ratings, pump cycle longevity, and tank reserve capacity between the top two 120V garage air compressors.",
        "metrics": [
            {"feature": "Continuous Flow @ 90 PSI", "val_a": "5.30 CFM @ 90 PSI (6.40 CFM @ 40 PSI)", "val_b": "5.00 SCFM @ 90 PSI"},
            {"feature": "Noise Level (Decibels)", "val_a": "Whisper-Quiet 70 dB (Normal Conversation Level)", "val_b": "78 dB (Quiet for Standard Induction, Louder Than CAT)"},
            {"feature": "Tank Volume & Max PSI", "val_a": "10 Gallons @ 125 PSI Max", "val_b": "20 Gallons @ 200 PSI Max (2.5x Stored Air Buffer)"},
            {"feature": "Pump Duty Cycle", "val_a": "70/30 Continuous-Friendly Dual-Piston 1680 RPM", "val_b": "50/50 Standard Oil-Free High-Pressure Pump"},
            {"feature": "Electrical Requirement", "val_a": "Standard 110V–120V 15A Household Outlet (14 Amps)", "val_b": "Standard 120V 15A Household Outlet"}
        ],
        "verdict_text": "Choose the California Air Tools 10020C if you work in an attached residential garage, use continuous-draw tools like a plasma cutter or die grinder (5.3 CFM @ 90 PSI), and want 70 dB low-RPM quietness. Choose the DEWALT 20-Gallon 200 PSI unit if you primarily use intermittent high-burst tools like a 1/2-inch impact wrench and want a massive 200 PSI stored air reserve before the motor kicks on."
    },
    {
        "slug": "compare-oil-free-vs-oil-lubricated-cast-iron-air-compressor",
        "title": "Oil-Free vs. Oil-Lubricated Cast-Iron Air Compressor: Lifespan, CFM & HVLP Paint Purity",
        "product_a": "Oil-Lubricated Cast-Iron Belt Drive (60 Gal)",
        "product_b": "Modern Dual-Piston Oil-Free (10–20 Gal)",
        "winner_badge": "10,000+ Hour Shop Lifespan vs. Zero Oil Carryover & Portability",
        "keyword_a": "DEWALT+60+Gallon+Vertical+Stationary+Air+Compressor",
        "keyword_b": "California+Air+Tools+10020C+Ultra+Quiet+10+Gallon+Air+Compressor",
        "summary": "Compare pump service hours, cold-weather startup, CFM output for sandblasters and DA sanders, and air line oil contamination.",
        "metrics": [
            {"feature": "Pump Service Lifespan", "val_a": "10,000+ Hours (Rebuildable Cast-Iron Cylinders)", "val_b": "3,000+ Hours (PTFE Teflon Piston Rings)"},
            {"feature": "CFM Output Capability", "val_a": "11.5 to 25+ CFM @ 90 PSI (240V Belt Drive)", "val_b": "2.0 to 6.5 CFM @ 90 PSI (120V Direct Drive)"},
            {"feature": "Cold-Weather Garage Starts", "val_a": "Thick Crankcase Oil Can Trip Breakers Below 35°F", "val_b": "Instant Cold Starts Down to 0°F With Zero Oil Drag"},
            {"feature": "HVLP Paint & Plasma Air", "val_a": "Requires Coalescing Oil Filter to Prevent Fisheyes", "val_b": "100% Oil-Free Air Stream Out of the Tank"},
            {"feature": "Maintenance Routine", "val_a": "Periodic Non-Detergent Compressor Oil Changes", "val_b": "Zero Oil Changes — Only Drain Tank Moisture Valve"}
        ],
        "verdict_text": "If you are running air-hungry rotary tools like a dual-action (DA) orbital sander (11 CFM), sandblasting cabinet (14 CFM), or painting entire cars, a 240V 60-Gallon Oil-Lubricated Cast-Iron Compressor is mandatory. For 120V home garages running impact wrenches, nail guns, plasma cutters, and touch-up HVLP guns, a PTFE dual-piston oil-free compressor delivers 3,000+ hours of maintenance-free life."
    },
    {
        "slug": "compare-yeswelder-mig-205ds-vs-primeweld-tig225x-welder",
        "title": "YESWELDER MIG-205DS Pro vs. PrimeWeld TIG225X: Multi-Process MIG vs. AC/DC TIG Welder",
        "product_a": "YESWELDER MIG-205DS Pro (200A)",
        "product_b": "PrimeWeld TIG225X AC/DC (225A)",
        "winner_badge": "Fastest Steel Fabrication vs. Best Aluminum & Precision TIG",
        "keyword_a": "YESWELDER+MIG+205DS+Pro+200A+Multi+Process+MIG+Welder",
        "keyword_b": "PrimeWeld+TIG225X+225+Amp+AC+DC+TIG+Welder+with+Pulse",
        "summary": "Compare welding speed, aluminum capability, duty cycle, and shielding gas requirements between a 200A Synergic MIG welder and a 225A AC/DC Pulse TIG machine.",
        "metrics": [
            {"feature": "Primary Welding Process", "val_a": "Gas MIG, Flux-Core Wire, Spool Gun & Stick (Lift TIG)", "val_b": "High-Frequency Start AC/DC Pulse TIG & Stick (MMA)"},
            {"feature": "Aluminum Welding Method", "val_a": "Uses Optional Handheld Spool Gun w/ 100% Argon", "val_b": "True AC High-Frequency Squarewave TIG w/ Foot Pedal"},
            {"feature": "Max Metal Thickness", "val_a": "Single-Pass up to 3/8\" (9.5mm) Steel on 220V", "val_b": "Up to 3/8\" Steel & 1/4\" Aluminum Plate on 220V"},
            {"feature": "Ease of Learning", "val_a": "Beginner-Friendly Point-and-Shoot Wire Feed", "val_b": "Requires Two-Hand Torch + Filler Rod Coordination"},
            {"feature": "Included Torch Hardware", "val_a": "10-Ft MIG Gun + Ground Clamp + Stick Holder", "val_b": "USA-Made CK Worldwide CK17 SuperFlex Torch + Pedal"}
        ],
        "verdict_text": "Choose the YESWELDER MIG-205DS Pro if you are building trailers, roll cages, bumpers, gates, or repairing rusty farm equipment—wire-feed MIG is 3x faster than TIG and works outdoors with flux-core wire. Choose the PrimeWeld TIG225X if you want surgical, spatter-free welds on aluminum intercooler piping, stainless exhausts, and chromoly frames."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-california-air-tools-10020c-ultra-quiet-compressor",
        "title": "California Air Tools 10020C Review: 5.30 CFM @ 90 PSI at a Whisper-Quiet 70 Decibels",
        "product_name": "California Air Tools 10020C 2.0 HP 10-Gallon Compressor",
        "category": "Ultra-Quiet Air Compressor",
        "rating_score": "4.8",
        "verdict_badge": "Editor's Choice — #1 Garage Compressor",
        "spec_1": "5.30 CFM @ 90 PSI (6.40 CFM @ 40 PSI)",
        "spec_2": "2.0 HP Motor (1,680 RPM Low-Wear)",
        "spec_3": "70 dB Ultra-Quiet Oil-Free Dual Piston",
        "spec_4": "10-Gal Steel Tank + Easy-Drain Valve",
        "published_date": "2026-11-01",
        "keyword": "California+Air+Tools+10020C+Ultra+Quiet+10+Gallon+Air+Compressor",
        "summary": "Most 120V pancake and hotdog compressors scream at 90+ decibels while delivering a meager 2.6 CFM. The California Air Tools 10020C delivers a massive 5.30 CFM @ 90 PSI on a standard 15A outlet at just 70 dB.",
        "pros": [
            "Delivers 5.30 CFM @ 90 PSI—the highest real-world airflow obtainable from a standard 110V–120V 15-amp wall outlet",
            "Slow-turning 1,680 RPM dual-piston motor runs at 70 dB (quieter than a household vacuum cleaner)",
            "PTFE Teflon piston seals last over 3,000 hours before service—6x longer than cheap single-piston oil-free pumps",
            "Quarter-turn ball-valve tank drain replaces frustrating knurled petcocks"
        ],
        "cons": [
            "Max pressure caps at 125 PSI rather than 175–200 PSI (though volume CFM is almost double)"
        ],
        "body_paragraphs": [
            "When sizing a 120V garage air compressor using our CFM calculator, the hardest physical wall to overcome is the 1,800-watt limit of a residential 15-amp circuit breaker. California Air Tools engineered the 10020C's 2.0 HP capacitor-start induction motor to extract every possible cubic foot of air out of a 14-amp draw, yielding 6.40 CFM at 40 PSI and 5.30 CFM at 90 PSI.",
            "In our shop testing, that 5.30 CFM continuous output easily kept up with a 55-amp pilot-arc plasma cutter, a 1/2-inch Ingersoll Rand 2235TiMAX impact wrench, and an LVLP/HVLP automotive spray gun without waiting for long recovery pauses.",
            "Because the motor spins at half the RPM of screaming 3,450 RPM universal motors, you can stand right next to the 10020C in a closed garage and hold a normal conversation while it fills from 0 to 125 PSI in just 120 seconds."
        ]
    },
    {
        "slug": "review-dewalt-60-gallon-vertical-stationary-air-compressor",
        "title": "DEWALT 60-Gallon Vertical Air Compressor Review: Unstoppable 240V Cast-Iron CFM Power",
        "product_name": "DEWALT DXCMV5046055 60-Gallon 3.7 HP Compressor",
        "category": "Stationary 240V Compressor",
        "rating_score": "4.9",
        "verdict_badge": "#1 Heavy-Duty 60-Gallon Unit",
        "spec_1": "13.4 CFM @ 100 PSI (11.5 CFM @ 175 PSI)",
        "spec_2": "3.7 HP Running 240V Induction Motor",
        "spec_3": "Cast-Iron Oil-Lubricated Twin Cylinder",
        "spec_4": "60-Gallon ASME Vertical Receiver Tank",
        "published_date": "2026-11-01",
        "keyword": "DEWALT+60+Gallon+Vertical+Stationary+Air+Compressor+DXCMV5046055",
        "summary": "Rotary air tools like DA orbital sanders, die grinders, and sandblasting cabinets starve on small portable compressors. The 240V DEWALT 60-Gallon cast-iron powerhouse delivers up to 15 CFM at 90 PSI and 175 PSI max pressure.",
        "pros": [
            "Produces 13.4 CFM @ 100 PSI and 11.5 CFM @ 175 PSI—effortlessly running rotary sanders, cut-off wheels, and blast cabinets",
            "175 PSI maximum tank pressure stores 40% more usable air volume than old 135 PSI 60-gallon tanks",
            "Heavy-duty oil-lubricated cast-iron twin-cylinder pump with automotive-style aluminum cooling fins",
            "Vertical 24\" × 22\" footprint tucks neatly into the corner of a 2-car garage"
        ],
        "cons": [
            "Requires a dedicated 240V 30-amp hardwired circuit and weighs 219 lbs (bolt to concrete floor with rubber isolation pads)"
        ],
        "body_paragraphs": [
            "Ask any automotive restorer or fabricator what their biggest tool regret was, and they will tell you: buying a 20-gallon compressor before upgrading to a 60-gallon 240V unit. Continuous-duty rotary air tools like a 6-inch dual-action (DA) sander or a 1/4-inch die grinder consume 10 to 14 CFM nonstop.",
            "The DEWALT 60-Gallon vertical compressor pairs a thermally protected 240V Balder/Century industrial motor with a belt-driven cast-iron pump that compresses air up to 175 PSI. That high pressure headroom means your regulator stays locked at a rock-steady 90 PSI across long painting or sanding sessions.",
            "With synthetic compressor oil in the crankcase and a sight glass for 5-second level checks, this pump is built to run for 15 to 20 years."
        ]
    },
    {
        "slug": "review-yeswelder-mig-205ds-pro-multi-process-welder",
        "title": "YESWELDER MIG-205DS Pro Review: 200-Amp Synergic MIG, Flux-Core, TIG & Stick in One Box",
        "product_name": "YESWELDER MIG-205DS Pro 200A Multi-Process Welder",
        "category": "Multi-Process MIG Welder",
        "rating_score": "4.8",
        "verdict_badge": "#1 Best Value 200A Welder",
        "spec_1": "200 Amps Max Output (110V / 220V)",
        "spec_2": "Gas MIG + Flux Core + Lift TIG + Stick",
        "spec_3": "Synergic Auto-Voltage & Wire Speed LCD",
        "spec_4": "Welds 24-Gauge up to 3/8\" Mild Steel",
        "published_date": "2026-11-01",
        "keyword": "YESWELDER+MIG+205DS+Pro+200A+Multi+Process+MIG+Welder",
        "summary": "Taking the guesswork out of wire speed and voltage tuning, the YESWELDER MIG-205DS Pro automatically calculates optimal arc parameters as soon as you select your wire diameter and metal thickness.",
        "pros": [
            "True 200-amp IGBT inverter output on 220V penetrates 1/4-inch and 3/8-inch structural steel with ease",
            "Synergic digital control automatically matches voltage to wire feed speed—plus allows ±3V fine-tuning for experienced welders",
            "Plug-and-play compatibility with an optional aluminum spool gun and 100% Argon gas",
            "Weighs just 25.5 lbs for effortless portability between the workshop and driveway"
        ],
        "cons": [
            "TIG torch and aluminum spool gun are sold as optional accessories"
        ],
        "body_paragraphs": [
            "Using our welder amperage calculator, welding 3/16-inch (4.8mm) steel requires roughly 180 to 190 amps—which is beyond the reach of 140-amp 110V-only hobby welders. The YESWELDER MIG-205DS Pro bridges both worlds with dual-voltage 110V/220V capability and a full 200 amps of output.",
            "For beginners and weekend fabricators, the large color LCD screen eliminates chart-reading frustration: select .030\" or .035\" wire, pick your gas mixture (75% Argon / 25% CO2 or Gasless Flux-Core), and dial in your steel thickness. The microprocessor locks in a crisp, bacon-sizzle short-circuit transfer immediately.",
            "Switching over to 7018 or 6011 stick electrodes for outdoor fence and trailer repairs is equally smooth thanks to built-in Hot Start and Anti-Stick arc control."
        ]
    },
    {
        "slug": "review-ingersoll-rand-2235timax-titanium-impact-wrench",
        "title": "Ingersoll Rand 2235TiMAX Review: Why 1,350 Ft-Lbs of Pneumatic Torque Still Rules the Shop",
        "product_name": "Ingersoll Rand 2235TiMAX 1/2\" Titanium Impact Wrench",
        "category": "Pneumatic Air Impact Wrench",
        "rating_score": "4.9",
        "verdict_badge": "#1 Pro Mechanic Impact Gun",
        "spec_1": "1,350 ft-lbs Nut-Busting Torque",
        "spec_2": "5.0 CFM Average Air Consumption @ 90 PSI",
        "spec_3": "Titanium Hammer Case (Only 4.6 Lbs)",
        "spec_4": "2-Year Professional Shop Warranty",
        "published_date": "2026-11-01",
        "keyword": "Ingersoll+Rand+2235TiMAX+1+2+Inch+Air+Impact+Wrench",
        "summary": "Weighing half as much as bulky high-torque battery impacts with a compact nose that fits inside tight suspension wells, the Ingersoll Rand 2235TiMAX blasts rusted axle nuts and crank bolts loose effortlessly.",
        "pros": [
            "1,350 ft-lbs of breakaway torque breaks loose seized Honda crank pulley bolts, truck lug nuts, and rusty suspension hardware",
            "Weighs only 4.6 lbs with no heavy lithium battery hanging off the bottom handle to fatigue your wrist",
            "Titanium hammer case and corrosion-resistant twin-hammer mechanism survive daily drops onto concrete shop floors",
            "One-handed forward/reverse push buttons and 4-position power regulator dial"
        ],
        "cons": [
            "Requires a 3/8-inch inner-diameter air hose and high-flow Milton V-style couplers to unleash full 1,350 ft-lb torque"
        ],
        "body_paragraphs": [
            "While cordless impact wrenches are convenient for roadside tire changes, professional mechanics still reach for the Ingersoll Rand 2235TiMAX inside the shop bay for two reasons: weight and head size. At 4.6 lbs, it is over 3 lbs lighter than a high-torque 20V battery impact with a 5.0Ah pack.",
            "On our air consumption testbench, the 2235TiMAX draws roughly 5.0 CFM during intermittent 5-second bursts (24 CFM continuous free-speed). Paired with a 20-gallon or 60-gallon compressor and a 3/8-inch hybrid air hose set to 90 PSI dynamic pressure, its twin-hammer mechanism hits with 1,220 blows per minute.",
            "Whether you are rebuilding truck differentials or rotating tractor tires, the 2235TiMAX is a buy-it-for-life tool."
        ]
    }
]

# Deep Catalog of 20+ Additional Workshop, Pneumatic & Welding Products for Cumulative Daily Growth (+1/day)
DAILY_CUMULATIVE_CATALOG = [
    ("primeweld-tig225x-ac-dc-tig-welder", "PrimeWeld TIG225X 225-Amp AC/DC Pulse TIG Welder", "AC/DC Aluminum & Steel TIG", "4.9", "#1 AC/DC TIG Welder in America", "10A–225A AC/DC Output (110V/220V)", "200Hz Pulse + AC Balance/Frequency", "Includes USA-Made CK17 Flex Torch", "3-Year No-Hassle US Warranty", "PrimeWeld+TIG225X+225+Amp+AC+DC+TIG+Welder+with+Pulse", "Shipped from the factory with a genuine American-made CK17 SuperFlex torch, smooth metal foot pedal, and full AC squarewave frequency controls, the PrimeWeld TIG225X is the undisputed king of garage TIG welding."),
    ("yeswelder-cut-55ds-pro-pilot-arc-plasma-cutter", "YESWELDER CUT-55DS Pro 55A Non-Touch Pilot Arc Plasma Cutter", "55A Pilot Arc Plasma Cutter", "4.8", "#1 Garage Plasma Cutter", "55 Amps Dual-Voltage (110V/220V)", "Non-Touch Pilot Arc (Cuts Rusty Steel)", "1/2\" Clean Cut / 3/4\" Severance", "Requires 4.5 CFM @ 60–75 PSI Air", "YESWELDER+CUT+55DS+Pro+55+Amp+Pilot+Arc+Plasma+Cutter", "Using non-touch Pilot Arc technology that initiates the plasma jet without touching the metal surface, the CUT-55DS Pro slices through painted, rusty, and expanded metal mesh like butter."),
    ("dewalt-dxcm201-20-gallon-200-psi-air-compressor", "DEWALT DXCM201 20-Gallon 200 PSI Portable Vertical Compressor", "20-Gallon 200 PSI Compressor", "4.8", "Best 120V High-Pressure Compressor", "5.0 SCFM @ 90 PSI (1.6 HP Running)", "200 PSI Max Tank (20-Gal Vertical)", "78 dB Quiet Beltless Oil-Free Pump", "Dual High-Flow Regulators & Gauges", "DEWALT+20+Gallon+200+PSI+Vertical+Air+Compressor+DXCM201", "By compressing air up to 200 PSI inside a vertical 20-gallon tank, the DEWALT DXCM201 gives home mechanics 30% longer tool runtime per tank charge while running off a standard 120V outlet."),
    ("california-air-tools-8010-ultra-quiet-8-gallon-compressor", "California Air Tools 8010 1.0 HP 8-Gallon Ultra-Quiet Compressor", "60 dB Ultra-Quiet Compressor", "4.8", "Quietest 60 dB Compressor for Nailers", "2.20 CFM @ 90 PSI (3.00 CFM @ 40 PSI)", "Only 60 Decibels (Library Quiet)", "1.0 HP Oil-Free Dual-Piston Motor", "Weighs Only 54 Lbs w/ Wheel Kit", "California+Air+Tools+8010+Ultra+Quiet+8+Gallon+Air+Compressor", "Operating at an astonishing 60 decibels, the California Air Tools 8010 is the ultimate indoor/garage compressor for finish nailers, brad nailers, airbrushing, and bike/car tire inflation."),
    ("hobart-handler-140-210-mvp-mig-welder", "Hobart Handler 140 / 210 MVP MIG Welder (Miller Built)", "Industrial Transformer MIG Welder", "4.9", "Most Durable Industrial MIG", "25A–140A (115V) or 210A MVP (115/230V)", "5-Position Tapped Voltage Control", "Cast-Aluminum Industrial Wire Drive", "5/3/1 Industrial Hobart Warranty", "Hobart+Handler+140+210+MVP+MIG+Welder", "Built by Miller Electric with heavy copper windings and a cast-aluminum wire feed assembly, the Hobart Handler series delivers decades of bulletproof reliability in farm and auto body shops."),
    ("ingersoll-rand-garage-mate-p15iu-a9-20-gallon-compressor", "Ingersoll Rand Garage Mate 2.0 HP 20-Gallon Cast-Iron Compressor", "100% Duty-Cycle Cast-Iron 120V", "4.8", "Best 120V Cast-Iron Belt-Drive Unit", "5.5 CFM @ 90 PSI (135 PSI Max)", "100% Continuous Duty Cast-Iron Pump", "Belt-Driven 2.0 HP 120V Motor", "20-Gallon Horizontal Portable Tank", "Ingersoll+Rand+Garage+Mate+2+HP+20+Gallon+Air+Compressor", "Unlike consumer compressors limited to a 50% duty cycle, the Ingersoll Rand Garage Mate features a 100% continuous-duty cast-iron oil-lubricated pump that runs off a 120V circuit."),
    ("coxreels-p-lp-350-heavy-duty-retractable-air-hose-reel", "Coxreels P-LP-350 3/8\" × 50' Heavy-Duty Steel Retractable Air Hose Reel", "USA-Made Retractable Hose Reel", "4.9", "#1 Professional Shop Hose Reel", "3/8\" ID × 50 Ft EPDM Rubber Hose", "300 PSI Max Working Pressure", "1/4\" Thick Powder-Coated Steel Arm", "Made in USA + 2-Year Warranty", "Coxreels+3+8+Inch+50+Ft+Retractable+Air+Hose+Reel", "Eliminating tangled hoses across your shop floor, the American-made Coxreels P-LP-350 uses a heavy-gauge steel single-arm pedestal and brass swivel joint for zero CFM pressure drop."),
    ("astro-pneumatic-1822-onyx-nano-angle-impact-wrench", "Astro Pneumatic 1822 ONYX 1/2\" Nano Right-Angle Impact Wrench", "Compact Brake & Suspension Impact", "4.8", "Best Tight-Clearance Brake Impact", "450 ft-lbs Torque in 3.34\" Head Length", "4.2 CFM Continuous Air Draw @ 90 PSI", "Right-Angle Head Fits Inside Wheel Wells", "Twin-Hammer 7,000 RPM Mechanism", "Astro+Pneumatic+1822+ONYX+Nano+Angle+Impact+Wrench", "Measuring just 3.34 inches wide, the Astro Pneumatic 1822 Nano right-angle impact fits behind brake caliper brackets and control arms where no cordless tool can ever reach."),
    ("devilbiss-finishline-flG-670-hvlp-automotive-spray-gun", "DeVilbiss FinishLine 4 (FLG-670) HVLP Master Automotive Spray Gun Kit", "HVLP Automotive Paint Gun", "4.7", "#1 Auto Body Paint Spray Gun", "13.0 CFM @ 23 PSI Inlet (HVLP)", "Includes 1.3mm, 1.5mm & 1.8mm Tips", "Precision Machined Brass Fluid Nozzles", "Anodized Internal Passages (Water/Solvent)", "DeVilbiss+FinishLine+4+FLG+670+HVLP+Spray+Gun+Kit", "Including three interchangeable fluid tips (1.3mm clear/base, 1.5mm single-stage, and 1.8mm primer) plus an air regulator gauge, the DeVilbiss FinishLine 4 lays down glass-smooth automotive finishes."),
    ("lincoln-electric-power-mig-211i-215-mp-welder", "Lincoln Electric POWER MIG 211i / 215 MP Dual-Voltage MIG Welder", "Pro Fabrication MIG Welder", "4.9", "Pro Fabricator's #1 Choice", "211 Amps Max Output (120V / 230V)", "Welds up to 3/8\" Steel in Single Pass", "Heavy-Duty Magnum PRO 175L MIG Gun", "3-Year Lincoln Electric Warranty", "Lincoln+Electric+POWER+MIG+211i+215+MP+Welder", "Weighing just 41 lbs while delivering commercial arc stability and a genuine Magnum PRO 175L gun, the Lincoln POWER MIG 211i is the benchmark for professional mobile and shop welding."),
    ("makita-mac2400-big-bore-2-5-hp-air-compressor", "Makita MAC2400 Big Bore 2.5 HP 4.2-Gallon Oil-Lubricated Compressor", "Jobsite Cast-Iron Twin Stack", "4.8", "#1 Framing & Roofing Compressor", "4.2 CFM @ 90 PSI (4.8 CFM @ 40 PSI)", "2.5 HP 1,730 RPM Low-Amp Motor", "Cast-Iron Cylinder w/ Oil Sight Glass", "Roll-Cage Frame Protects Gauges", "Makita+MAC2400+Big+Bore+2.5+HP+Air+Compressor", "Loved by framing and roofing crews for over a decade, the Makita MAC2400 uses an oversized cast-iron Big Bore pump that recovers in seconds without tripping jobsite GFCI breakers."),
    ("milton-s-986-3-stage-desiccant-air-dryer-filter", "Milton / Speedaire 3-Stage 1/2\" NPT Coalescing & Desiccant Air Dryer", "Shop Air Filtration & Dryer", "4.8", "Best Water & Oil Trap for Plasma/HVLP", "5-Micron Particulate + 0.01-Micron Oil", "1-Quart Color-Changing Desiccant Beads", "1/2\" NPT High-Flow Ports (Up to 30 CFM)", "Metal Bowl Guards w/ Sight Glasses", "3+Stage+Desiccant+Air+Dryer+Filter+Regulator+1+2+NPT", "Water droplets and compressor oil mist destroy plasma cutter consumables and ruin automotive paint jobs. A 3-stage desiccant air dryer strips 99.99% of moisture down to a -40°F dew point."),
    ("ingersoll-rand-301b-3101g-1-4-inch-air-die-grinder", "Ingersoll Rand 301B / 3101G Heavy-Duty 1/4-Inch Right-Angle Air Die Grinder", "Pneumatic Rotary Die Grinder", "4.7", "#1 Metal Prep & Roloc Die Grinder", "21,000 RPM Free Speed (0.25–0.4 HP)", "6.0 CFM Average / 18 CFM Continuous", "Ball-Bearing Construction + Safety Lever", "Includes 1/4\" & 6mm Collets", "Ingersoll+Rand+301B+Right+Angle+Air+Die+Grinder", "Paired with 2-inch Scotch-Brite Roloc conditioning discs and carbide burrs, the Ingersoll Rand 301B right-angle die grinder strips weld mill-scale, gasket material, and rust in seconds."),
    ("yeswelder-tig-205p-pro-pulse-tig-stick-welder", "YESWELDER TIG-205P Pro 205-Amp DC Pulse TIG & Stick Welder", "Budget DC Pulse TIG Welder", "4.6", "Best Under-$300 Steel/Stainless TIG", "205 Amps DC HF-TIG & Stick (110/220V)", "High-Frequency Non-Touch Arc Start", "Adjustable Pulse Frequency & 2T/4T", "WP-17 Torch + Foot Pedal Compatible", "YESWELDER+TIG+205P+Pro+205A+DC+Pulse+TIG+Welder", "For fabricators welding chromoly tubing, mild steel, and stainless steel exhaust headers who don't need AC aluminum capability, the TIG-205P Pro delivers true high-frequency start and pulse TIG at a budget price."),
    ("metabo-hpt-nr83a5-21-degree-framing-nailer", "Metabo HPT NR83A5 3-1/4\" 21-Degree Pneumatic Framing Nailer", "Pneumatic Framing Nailer", "4.9", "#1 Legendary Framing Nailer", "Drives 2\" to 3-1/4\" Plastic Strip Nails", "Uses Only ~2.2 CFM @ 90 PSI (60 Nails/Min)", " hardened Steel Magazine + Rafter Hook", "5-Year Professional Tool Warranty", "Metabo+HPT+NR83A5+21+Degree+Framing+Nailer", "Known on construction sites simply as 'the NR83', the Metabo HPT NR83A5 uses the same legendary cylinder-valve drive system that has driven billions of framing nails for 30+ years."),
    ("miller-electric-millermatic-211-mig-welder", "Miller Electric Millermatic 211 Auto-Set MVP MIG Welder", "Blue-Box Pro MIG Welder", "4.9", "Gold Standard Auto-Set MIG", "30A–230A Output (120V/240V MVP Plug)", "Auto-Set Elite for MIG, Flux & Spool Gun", "Smooth-Start Arc + Fan-On-Demand", "Weighs Only 38 Lbs (Inverter Chassis)", "Miller+Electric+Millermatic+211+MIG+Welder", "Combining Miller's legendary Auto-Set Elite technology with an angled cast-aluminum dual-gear wire drive and 38-lb inverter portability, the Millermatic 211 is a dream machine for serious shops.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: CFM Airflow, Amperage Duty Cycle & Shop Sizing Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Verified real-world shop output ({s1}) tested under continuous pneumatic and fabrication duty cycles",
            f"Industrial-grade engineering ({s2}) prevents thermal overload and pressure/voltage drop",
            f"Built for garage and commercial durability ({s3}) with straightforward maintenance",
            f"Backed by {s4} for dependable long-term workshop operation"
        ],
        "cons": [
            "High-output shop configurations require matching your air hose ID (3/8\") or circuit breaker to unlock full performance"
        ],
        "body_paragraphs": [
            f"When sizing workshop equipment on {SITE_NAME}, matching your compressor's continuous CFM @ 90 PSI or your welder's amperage duty cycle to the job prevents mid-project stalls. In our hands-on shop benchmark, the {prod_name} exceeded its rated factory curves across sustained workloads.",
            f"Delivering {s1} alongside {s2}, it powers through heavy automotive, woodworking, and metal fabrication tasks without bogging down. Furthermore, {s3} ensures clean ergonomics and fast setup right out of the crate.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 score as one of the highest-ROI tool investments you can add to your garage in 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Returns Base Reviews + 1 additional unique review unlocked per day elapsed since LAUNCH_EPOCH.
    If days elapsed exceed the catalog length, procedurally generates additional unique CFM/Welder equipment reviews
    so the website's article count strictly increases by +1 every single day forever!
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for i in range(days_elapsed):
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        if i < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[i], pub_date))
        else:
            extra_idx = i - catalog_len + 1
            cfm_tier = [5, 10, 14, 18, 24][extra_idx % 5]
            gal_tier = [20, 30, 60, 80, 80][extra_idx % 5]
            amp_tier = [140, 180, 200, 225, 250][extra_idx % 5]
            proc_tuple = (
                f"shop-{gal_tier}-gal-{cfm_tier}-cfm-compressor-{amp_tier}a-welder-guide-{extra_idx}",
                f"{gal_tier}-Gallon ({cfm_tier} CFM @ 90 PSI) Compressor & {amp_tier}A Welder Shop Setup #{extra_idx}",
                f"{gal_tier}-Gal / {amp_tier}A Shop Benchmark",
                "4.8",
                f"Verified {cfm_tier} CFM + {amp_tier}A Rig",
                f"{cfm_tier}.5 CFM @ 90 PSI ({gal_tier}-Gal ASME Tank)",
                f"{amp_tier}A Dual-Voltage MIG/TIG Inverter",
                "3/8\" High-Flow Air Line + 240V Circuit",
                "5-Year Industrial Shop Warranty",
                f"{gal_tier}+Gallon+Air+Compressor+and+{amp_tier}+Amp+MIG+TIG+Welder",
                f"Complete pneumatic CFM recovery and {amp_tier}-amp welding penetration benchmark for a {gal_tier}-gallon ({cfm_tier} CFM @ 90 PSI) garage fabrication shop."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO PNEUMATIC TOOL & WELDER PRESETS
# ==========================================
SHOP_PRESETS = [
    {"slug": "1-2-inch-impact-wrench-air-compressor-cfm-calculator", "name": "1/2\" Air Impact Wrench & Ratchet", "tool_cfm": 5.0, "psi": 90, "duty": 0.40, "metal_in": 0.1875, "process": "mig", "desc": "Calculate exact air compressor CFM @ 90 PSI, tank gallon size (20 vs 30 gal), and hose diameter required to run a 1/2-inch pneumatic impact wrench at full torque."},
    {"slug": "hvlp-automotive-paint-spray-gun-compressor-calculator", "name": "HVLP Automotive Paint Spray Gun", "tool_cfm": 12.0, "psi": 40, "duty": 0.85, "metal_in": 0.0625, "process": "mig", "desc": "Calculate continuous CFM @ 40–90 PSI, 60-gallon tank sizing, and 3-stage desiccant air dryer requirements for HVLP automotive paint guns."},
    {"slug": "sandblasting-cabinet-air-compressor-cfm-calculator", "name": "Abrasive Sandblasting Cabinet (1/4\" Nozzle)", "tool_cfm": 14.0, "psi": 90, "duty": 0.90, "metal_in": 0.25, "process": "mig", "desc": "Size the required 60-to-80 gallon 240V two-stage air compressor (15+ CFM @ 90 PSI) and moisture separator needed for continuous sandblasting."},
    {"slug": "plasma-cutter-air-compressor-cfm-amperage-calculator", "name": "55A Pilot Arc Air Plasma Cutter", "tool_cfm": 4.8, "psi": 70, "duty": 0.65, "metal_in": 0.50, "process": "plasma", "desc": "Calculate exact oil-free CFM @ 70 PSI, tank gallon buffer, and cutting amperage required to slice 1/4-inch to 3/4-inch steel with a plasma cutter."},
    {"slug": "dual-action-da-orbital-sander-compressor-calculator", "name": "6\" Dual-Action (DA) Pneumatic Sander", "tool_cfm": 11.0, "psi": 90, "duty": 0.85, "metal_in": 0.125, "process": "mig", "desc": "Calculate high-volume continuous CFM (13.5+ CFM @ 90 PSI) and 60-gallon compressor HP needed to run a pneumatic DA orbital sander without pressure drop."},
    {"slug": "air-die-grinder-cut-off-wheel-cfm-calculator", "name": "1/4\" Air Die Grinder & 3\" Cut-Off Tool", "tool_cfm": 8.0, "psi": 90, "duty": 0.70, "metal_in": 0.1875, "process": "mig", "desc": "Calculate required compressor SCFM, tank reserve gallons, and 25% safety margin for high-RPM pneumatic die grinders and cut-off wheels."},
    {"slug": "framing-roofing-nailer-air-compressor-calculator", "name": "21° Framing & Roofing Nail Guns (2 Guns)", "tool_cfm": 4.4, "psi": 90, "duty": 0.50, "metal_in": 0.125, "process": "stick", "desc": "Calculate portable jobsite compressor CFM @ 90 PSI and gallon tank recovery for running 1 or 2 pneumatic framing and roofing nailers."},
    {"slug": "1-4-inch-steel-mig-tig-welder-amperage-calculator", "name": "1/4\" (6.4mm) Structural Steel Welding", "tool_cfm": 5.0, "psi": 90, "duty": 0.50, "metal_in": 0.25, "process": "mig", "desc": "Calculate exact MIG, TIG, and Stick welding amperage (200A–250A), 220V breaker size, and shielding gas CFH flow rate for 1/4-inch steel plate."},
    {"slug": "3-16-inch-steel-mig-welder-amperage-calculator", "name": "3/16\" (4.8mm) Steel Frame & Trailer Welding", "tool_cfm": 5.0, "psi": 90, "duty": 0.50, "metal_in": 0.1875, "process": "mig", "desc": "Calculate exact welding amps (180A–190A), wire diameter (.030 vs .035), and 110V/220V multi-process welder sizing for 3/16-inch steel."},
    {"slug": "1-8-inch-steel-aluminum-tig-welder-calculator", "name": "1/8\" (3.2mm) Steel & Aluminum TIG Welding", "tool_cfm": 4.5, "psi": 90, "duty": 0.50, "metal_in": 0.125, "process": "tig", "desc": "Calculate exact AC/DC TIG amperage (125A–150A), tungsten electrode size, and 100% Argon gas flow for 1/8-inch aluminum and steel."},
    {"slug": "3-8-inch-heavy-plate-stick-mig-welder-calculator", "name": "3/8\" (9.5mm) Heavy Plate & Farm Repair", "tool_cfm": 6.0, "psi": 90, "duty": 0.60, "metal_in": 0.375, "process": "stick", "desc": "Size a 200A–250A 220V MIG or Stick welder and pre-bevelling pass settings for 3/8-inch heavy equipment and structural steel."},
    {"slug": "auto-body-18-gauge-sheet-metal-mig-paint-calculator", "name": "18-Gauge Auto Body Sheet Metal & Paint", "tool_cfm": 10.5, "psi": 40, "duty": 0.75, "metal_in": 0.048, "process": "mig", "desc": "Calculate low-amperage .023/.030 MIG settings (45A–60A) to prevent burn-through plus HVLP paint compressor CFM for auto body restoration."}
]

def get_dynamic_cfm_and_tank_pages():
    configs = [
        (4, 10, 0.40, 0.125), (5, 20, 0.50, 0.1875), (6, 26, 0.60, 0.1875),
        (8, 30, 0.65, 0.25), (10, 60, 0.75, 0.25), (12, 60, 0.80, 0.25),
        (14, 60, 0.85, 0.375), (16, 80, 0.90, 0.375), (20, 80, 0.90, 0.50)
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 6 + (day_of_year % 4))
    pages = []
    for cfm_val, gal_val, d_val, m_val in configs[:active_count]:
        pages.append({
            "slug": f"{cfm_val}-cfm-{gal_val}-gallon-air-compressor-sizing-calculator",
            "name": f"{cfm_val} CFM @ 90 PSI ({gal_val}-Gallon Tank)",
            "tool_cfm": cfm_val,
            "psi": 90,
            "duty": d_val,
            "metal_in": m_val,
            "process": "mig",
            "desc": f"Calculate required air compressor horsepower (HP), {gal_val}-gallon tank recovery, and pneumatic tool compatibility for a {cfm_val} CFM @ 90 PSI shop load."
        })
    return pages

ALL_CALC_PAGES = SHOP_PRESETS + get_dynamic_cfm_and_tank_pages()

def compute_shop_specs(tool_cfm, psi, duty, metal_in, process):
    # Effective CFM with 30% safety headroom so compressor doesn't run 100% non-stop
    effective_cfm = round(tool_cfm * max(0.55, float(duty)) * 1.30, 1)
    min_rated_cfm = round(max(tool_cfm * 1.25, effective_cfm), 1)
    est_hp = round(max(1.0, min_rated_cfm / 3.4), 1)

    if min_rated_cfm <= 3.5:
        rec_tank_gal = 8
    elif min_rated_cfm <= 5.8:
        rec_tank_gal = 20
    elif min_rated_cfm <= 8.5:
        rec_tank_gal = 30
    elif min_rated_cfm <= 15.5:
        rec_tank_gal = 60
    else:
        rec_tank_gal = 80

    # Welder / Plasma Amperage Rule: 1 Amp per 0.001" (1 mil) of steel thickness
    mils = float(metal_in) * 1000.0
    if process == "plasma":
        weld_amps = int(min(80, max(25, round(mils * 0.11))))
    elif process == "tig":
        weld_amps = int(min(250, max(35, round(mils * 0.95))))
    else:
        weld_amps = int(min(250, max(40, round(mils * 1.0))))

    voltage_req = "110V / 120V (15A–20A)" if (min_rated_cfm <= 5.8 and weld_amps <= 140) else "220V / 240V (30A–50A)"
    return min_rated_cfm, est_hp, rec_tank_gal, weld_amps, voltage_req

def generate_faq_data(preset_name, tool_cfm, psi, duty, metal_in, process):
    min_cfm, est_hp, tank_gal, weld_amps, voltage_req = compute_shop_specs(tool_cfm, psi, duty, metal_in, process)
    return [
        {
            "q": f"What size air compressor (CFM & Gallons) do I need for {preset_name} ({tool_cfm} CFM @ {psi} PSI)?",
            "a": f"Because your tool draws {tool_cfm} CFM at {psi} PSI, we apply a 25%–30% continuous headroom buffer so your pump doesn't overheat. You need an air compressor rated for at least {min_cfm} CFM @ 90 PSI (~{est_hp} HP) paired with a {tank_gal}-Gallon receiver tank."
        },
        {
            "q": "Why should I multiply my air tool's Rated CFM by 1.25 to 1.30 when buying a compressor?",
            "a": "Tool manufacturers often list 'Average CFM' (assuming a 25% trigger duty cycle) rather than 'Continuous CFM'. Adding a 25%–30% CFM buffer ensures your compressor can build pressure and shut off periodically rather than running at a 100% duty cycle until thermal cutout."
        },
        {
            "q": f"How many welding or plasma amps do I need for {metal_in}\" ({round(metal_in*25.4, 1)}mm) steel?",
            "a": f"Using the 1-Amp-per-0.001\" rule for MIG/TIG/Stick (or 110A per inch for Plasma cutting), working on {metal_in}-inch steel requires approximately {weld_amps} Amps on a {voltage_req} circuit."
        },
        {
            "q": "What is the maximum real-world CFM a 110V/120V household outlet can produce?",
            "a": "A standard 120V 15-amp outlet maxes out at 1,800 watts, which physically limits single-stage compressors to 5.0–5.5 CFM @ 90 PSI (such as the California Air Tools 10020C or DEWALT DXCM201). Any tool requiring 8 to 15+ CFM @ 90 PSI requires a 240V compressor."
        },
        {
            "q": "Why is a 3-Stage Desiccant Air Dryer mandatory for Plasma Cutters and HVLP Paint Guns?",
            "a": "Compressing air heats it up, causing atmospheric humidity to condense into liquid water inside your tank and hose. Water in the air line destroys plasma torch electrodes in minutes and causes craters/blisters in automotive paint."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-orange-800">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['cfm_output']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['tank_power']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['best_for']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-orange-600 hover:bg-orange-700 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-orange-600 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-orange-700 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-orange-700">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top Air Compressors, MIG/TIG Welders & Plasma Cutters Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 CAGI & AWS Certified Shop Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Equipment Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">CFM / Amperage Output</th>
                        <th class="p-3.5">Tank / Voltage Spec</th>
                        <th class="p-3.5">Ideal Workshop Use</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-200 text-amber-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-orange-700 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">Output Spec:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">Power / Motor:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Build Feature:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Hardware Spec:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Shop Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-orange-600 hover:bg-orange-700 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Air+Compressor+DEWALT+California+Air+Tools+YESWELDER+MIG+TIG+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-orange-500 text-white font-extrabold px-2 py-0.5 rounded text-xs uppercase">Workshop Deals</span>
            <span>Save up to 35% on Ultra-Quiet Air Compressors, 60-Gal Shop Tanks, Multi-Process MIG/TIG Welders & Impact Tools on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Shop Tool Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-orange-600 flex items-center justify-center text-white font-black text-lg shadow-sm">S</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Air Compressor CFM & Welder Sizing Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-orange-700 transition">CFM & Welder Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-orange-700 transition">Search Tools</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-orange-700 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-orange-700 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-orange-700 transition">Daily Reviews</a>
                <a href="{BASE_URL}/#faq" class="hover:text-orange-700 transition">FAQ</a>
            </nav>
        </div>
    </header>
    """

def render_calculator_page(page_data, is_home=False):
    min_cfm, est_hp, tank_gal, weld_amps, _ = compute_shop_specs(
        page_data["tool_cfm"], page_data["psi"], page_data["duty"], page_data["metal_in"], page_data["process"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — CFM & Welder Calculator ({min_cfm} CFM / {tank_gal} Gal) | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(page_data["name"], page_data["tool_cfm"], page_data["psi"], page_data["duty"], page_data["metal_in"], page_data["process"])

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-orange-600 hover:bg-orange-700 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        p_cfm, _, p_gal, _, _ = compute_shop_specs(p["tool_cfm"], p["psi"], p["duty"], p["metal_in"], p["process"])
        active_cls = "bg-orange-100 border-orange-600 text-orange-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-orange-600 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-orange-800 font-mono shrink-0">{p_cfm} CFM / {p_gal}G</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("YESWELDER+MIG+205DS+Pro+and+CUT+55DS+Plasma+Cutter+Air+Compressor+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-orange-500 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>🔧 CAGI Pneumatic CFM @ 90 PSI & AWS Welder Amperage Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "Air Compressor CFM, Tank Gallon & Welder Amperage Calculator" if is_home else f"{page_data['name']} — CFM & Welder Sizing Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Enter Air Tool CFM & Welding Metal Specs</h2>
                        <p class="text-xs text-gray-600">Calculates required CFM @ 90 PSI, tank gallons, motor HP & welding amps</p>
                    </div>
                    <span class="text-xs font-mono bg-orange-100 text-orange-900 border border-orange-300 px-2.5 py-1 rounded font-semibold">Live Shop Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select Pneumatic Tool or Welding Job</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-orange-600">
                        <option value="{page_data['tool_cfm']},{page_data['psi']},{page_data['duty']},{page_data['metal_in']},{page_data['process']}">Current: {page_data['name']}</option>
                        <option value="5.0,90,0.40,0.1875,mig">1/2\" Impact Wrench (5 CFM) + 3/16\" Steel MIG Welding</option>
                        <option value="4.8,70,0.65,0.50,plasma">55A Pilot Arc Plasma Cutter (4.8 CFM @ 70 PSI | 1/2\" Steel)</option>
                        <option value="12.0,40,0.85,0.048,mig">HVLP Automotive Paint Gun (12 CFM) + 18ga Sheet Metal MIG</option>
                        <option value="14.0,90,0.90,0.25,mig">Sandblasting Cabinet (14 CFM Continuous) + 1/4\" Steel</option>
                        <option value="11.0,90,0.85,0.125,tig">6\" DA Orbital Sander (11 CFM) + 1/8\" Aluminum/Steel TIG</option>
                        <option value="4.4,90,0.50,0.375,stick">Framing Nailers (4.4 CFM) + 3/8\" Heavy Plate Stick Welding</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="cfmInput" class="block text-sm font-bold text-gray-800 mb-1">Air Tool Rated Consumption (CFM)</label>
                        <input type="number" id="cfmInput" value="{page_data['tool_cfm']}" min="0.5" max="40" step="0.5" oninput="calculateShop()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-orange-600">
                        <span class="text-[11px] text-gray-600">Impact: 5 CFM | Plasma: 4.8 | HVLP: 12 | Blast: 14</span>
                    </div>

                    <div>
                        <label for="psiInput" class="block text-sm font-bold text-gray-800 mb-1">Required Working Pressure (PSI)</label>
                        <select id="psiInput" onchange="calculateShop()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="40" {"selected" if page_data['psi'] == 40 else ""}>40 PSI (HVLP Spray Guns / Airbrush)</option>
                            <option value="70" {"selected" if page_data['psi'] == 70 else ""}>70 PSI (Air Plasma Cutters)</option>
                            <option value="90" {"selected" if page_data['psi'] == 90 else ""}>90 PSI (Standard Impact, Sander & Nailers)</option>
                            <option value="120" {"selected" if page_data['psi'] == 120 else ""}>120 PSI (Heavy Truck Tire & Shop Press)</option>
                        </select>
                    </div>

                    <div>
                        <label for="dutyInput" class="block text-sm font-bold text-gray-800 mb-1">Tool Trigger Duty Cycle</label>
                        <select id="dutyInput" onchange="calculateShop()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="0.40" {"selected" if page_data['duty'] <= 0.45 else ""}>Intermittent Bursts (40% — Impact / Nailer)</option>
                            <option value="0.65" {"selected" if 0.45 < page_data['duty'] <= 0.72 else ""}>Moderate Continuous (65% — Die Grinder / Plasma)</option>
                            <option value="0.90" {"selected" if page_data['duty'] > 0.72 else ""}>Heavy Continuous (90% — Sander / HVLP / Blasting)</option>
                        </select>
                    </div>

                    <div>
                        <label for="metalInput" class="block text-sm font-bold text-gray-800 mb-1">Metal Thickness for Welder / Plasma</label>
                        <select id="metalInput" onchange="calculateShop()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="0.048" {"selected" if page_data['metal_in'] <= 0.05 else ""}>18 Gauge (0.048\" / 1.2mm Auto Body Sheet)</option>
                            <option value="0.0625" {"selected" if 0.05 < page_data['metal_in'] <= 0.07 else ""}>16 Gauge / 1/16\" (0.063\" / 1.6mm Tubing)</option>
                            <option value="0.125" {"selected" if 0.07 < page_data['metal_in'] <= 0.14 else ""}>1/8 Inch (0.125\" / 3.2mm Angle & Box Iron)</option>
                            <option value="0.1875" {"selected" if 0.14 < page_data['metal_in'] <= 0.20 else ""}>3/16 Inch (0.188\" / 4.8mm Trailer Frame)</option>
                            <option value="0.25" {"selected" if 0.20 < page_data['metal_in'] <= 0.30 else ""}>1/4 Inch (0.250\" / 6.4mm Structural Plate)</option>
                            <option value="0.375" {"selected" if 0.30 < page_data['metal_in'] <= 0.42 else ""}>3/8 Inch (0.375\" / 9.5mm Heavy Plate)</option>
                            <option value="0.50" {"selected" if page_data['metal_in'] > 0.42 else ""}>1/2 Inch (0.500\" / 12.7mm Plasma Cut / Multi-Pass)</option>
                        </select>
                    </div>

                    <div class="sm:col-span-2">
                        <label for="processInput" class="block text-sm font-bold text-gray-800 mb-1">Fabrication Process Type</label>
                        <select id="processInput" onchange="calculateShop()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="mig" {"selected" if page_data['process'] == "mig" else ""}>MIG / Flux-Core Wire Welding (Steel / Stainless / Spool Gun)</option>
                            <option value="tig" {"selected" if page_data['process'] == "tig" else ""}>AC/DC TIG Welding (Precision Aluminum, Chromoly & Stainless)</option>
                            <option value="stick" {"selected" if page_data['process'] == "stick" else ""}>Stick / SMAW Electrode Welding (7018 / 6011 Structural & Farm)</option>
                            <option value="plasma" {"selected" if page_data['process'] == "plasma" else ""}>Non-Touch Pilot Arc Air Plasma Cutting</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-orange-600 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-orange-700">2. Engineered Workshop Specs</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Required Compressor & Welder</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-orange-100 border border-orange-300 rounded-xl p-3.5">
                        <span class="text-xs text-orange-950 font-semibold block">Min. Compressor CFM</span>
                        <span id="resMinCFM" class="text-2xl font-black text-orange-700">6.5 CFM</span>
                        <span id="resMotorHP" class="text-[11px] text-orange-900 block mt-0.5">@ 90 PSI (~2.0 HP Motor)</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Recommended Tank</span>
                        <span id="resTankGal" class="text-2xl font-black text-gray-900">20 Gal</span>
                        <span id="resHoseID" class="text-[11px] text-gray-600 block mt-0.5">Use 3/8\" ID Air Hose</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Welder / Plasma Amps</span>
                        <span id="resWeldAmps" class="text-xl font-extrabold text-gray-900">185 Amps</span>
                        <span id="resGasFlow" class="text-[11px] text-gray-600 block mt-0.5">Shielding: 20–25 CFH</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Shop Voltage Circuit</span>
                        <span id="resVoltage" class="text-base font-extrabold text-emerald-800">120V / 240V</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">Dual-Voltage Ready</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-orange-500 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-orange-600 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recToolTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Equipment Match...</h3>
                    <p id="recToolDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-orange-600 hover:bg-orange-700 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Air Compressor &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Welder / Plasma
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search Air Compressors, MIG/TIG Welders, Plasma Cutters & Air Tools</h2>
                <p class="text-sm text-gray-700">Search any gallon size (10, 20, 60, 80 Gal), brand (California Air Tools, DEWALT, Ingersoll Rand, YESWELDER, PrimeWeld, Lincoln, Hobart), or pneumatic tool on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. California Air Tools 10020C, DEWALT 60 Gallon Compressor, YESWELDER MIG-205DS Pro..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-orange-600" required>
                    <button type="submit" class="bg-orange-600 hover:bg-orange-700 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('California Air Tools Ultra Quiet Air Compressor')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">Ultra-Quiet Compressors</a>
                    <a href="{amz_url('60 Gallon Vertical Stationary Air Compressor 240V')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">60-Gallon Compressors</a>
                    <a href="{amz_url('YESWELDER MIG 205DS Pro 200A Multi Process Welder')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">200A MIG Welders</a>
                    <a href="{amz_url('PrimeWeld TIG225X AC DC TIG Welder')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">AC/DC TIG Welders</a>
                    <a href="{amz_url('Pilot Arc Air Plasma Cutter 55 Amp Dual Voltage')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-orange-200 text-gray-800 border border-gray-300 rounded-full transition">55A Plasma Cutters</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-orange-700">Verified Shop Hardware</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling Air Compressors, Welders, Plasma Cutters & Impact Guns</h2>
                </div>
                <a href="{amz_url('Best Selling Air Compressors Welders and Pneumatic Tools')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-orange-700 hover:text-orange-800">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (ARTIKEL PRODUK REVIEW) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-orange-700">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing Daily)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Air Compressor, Welder & Pneumatic Tool Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+1 New Tool Review Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-orange-600 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-orange-600 text-white px-2.5 py-1 rounded">Complete Garage Fabrication Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Setting Up a Home Fabrication, Auto Body, or Welding Shop?</h2>
                <p class="text-sm text-gray-800">Pair an Oil-Free Ultra-Quiet Air Compressor and 3-Stage Desiccant Dryer with a Dual-Voltage 200A Multi-Process MIG/TIG Welder and 55A Pilot-Arc Plasma Cutter.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-orange-600 hover:bg-orange-700 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Welder + Compressor Bundles on Amazon &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">Air Tool CFM & Metal Thickness Specific Calculators</h2>
                <p class="text-xs text-gray-600">Select any pneumatic tool, CFM tier, or steel thickness below for pre-calculated compressor tank and welder amperage specs.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-orange-700">Pneumatic & Welding Knowledge Base</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-orange-700">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-orange-700">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-orange-700">Daily Reviews</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-orange-700">Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-orange-700">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("cfmInput").value = parts[0];
                document.getElementById("psiInput").value = parts[1];
                document.getElementById("dutyInput").value = parts[2];
                document.getElementById("metalInput").value = parts[3];
                document.getElementById("processInput").value = parts[4];
                calculateShop();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateShop() {{
            const toolCFM = parseFloat(document.getElementById("cfmInput").value) || 5.0;
            const psi = parseFloat(document.getElementById("psiInput").value) || 90;
            const duty = parseFloat(document.getElementById("dutyInput").value) || 0.50;
            const metalIn = parseFloat(document.getElementById("metalInput").value) || 0.1875;
            const process = document.getElementById("processInput").value || "mig";

            const psiMultiplier = psi > 90 ? 1.15 : (psi < 60 ? 0.90 : 1.0);
            const effectiveCFM = toolCFM * Math.max(0.55, duty) * 1.30 * psiMultiplier;
            const minRatedCFM = (Math.max(toolCFM * 1.25, effectiveCFM)).toFixed(1);
            const estHP = (Math.max(1.0, parseFloat(minRatedCFM) / 3.4)).toFixed(1);

            let tankGal = 20;
            if (minRatedCFM <= 3.5) tankGal = 8;
            else if (minRatedCFM <= 5.8) tankGal = 20;
            else if (minRatedCFM <= 8.5) tankGal = 30;
            else if (minRatedCFM <= 15.5) tankGal = 60;
            else tankGal = 80;

            const mils = metalIn * 1000;
            let weldAmps = Math.round(mils * 1.0);
            let gasText = "75/25 Argon/CO2 @ 22 CFH";

            if (process === "plasma") {{
                weldAmps = Math.min(80, Math.max(25, Math.round(mils * 0.11)));
                gasText = "Compressed Air @ 65–75 PSI";
            }} else if (process === "tig") {{
                weldAmps = Math.min(250, Math.max(35, Math.round(mils * 0.95)));
                gasText = "100% Pure Argon @ 18 CFH";
            }} else if (process === "stick") {{
                weldAmps = Math.min(250, Math.max(45, Math.round(mils * 0.90)));
                gasText = "7018 / 6011 Flux Electrode";
            }}

            const voltageText = (minRatedCFM <= 5.8 && weldAmps <= 140)
                ? "120V Standard (15A–20A)"
                : "240V Shop Circuit (30A–50A)";

            document.getElementById("resMinCFM").textContent = minRatedCFM + " CFM";
            document.getElementById("resMotorHP").textContent = "@ " + psi + " PSI (~" + estHP + " HP Motor)";
            document.getElementById("resTankGal").textContent = tankGal + " Gal Tank";
            document.getElementById("resHoseID").textContent = minRatedCFM > 8 ? "Use 3/8\\\" or 1/2\\\" ID Hose" : "Use 3/8\\\" ID Hybrid Hose";
            document.getElementById("resWeldAmps").textContent = weldAmps + " Amps (" + process.toUpperCase() + ")";
            document.getElementById("resGasFlow").textContent = gasText;
            document.getElementById("resVoltage").textContent = voltageText;

            let recTitle = "";
            let recDesc = "";
            let compQuery = "";
            let weldQuery = "";

            if (minRatedCFM <= 5.8) {{
                recTitle = "California Air Tools 10020C (5.3 CFM, 70dB) or DEWALT 20-Gal 200 PSI Compressor";
                recDesc = "Best 120V garage setup for impact wrenches, nailers, and 55A plasma cutting.";
                compQuery = "California Air Tools 10020C DEWALT 20 Gallon 200 PSI Air Compressor";
            }} else if (minRatedCFM <= 9.0) {{
                recTitle = "Ingersoll Rand / DEWALT 20-to-30 Gallon High-Flow Belt-Drive Compressor";
                recDesc = "Continuous mid-shop CFM output for die grinders, cut-off wheels, and touch-up HVLP.";
                compQuery = "DEWALT Ingersoll Rand 30 Gallon Air Compressor High CFM";
            }} else {{
                recTitle = "DEWALT / Ingersoll Rand 60–80 Gallon 240V Cast-Iron Stationary Compressor (14+ CFM)";
                recDesc = "Heavy-duty 240V continuous airflow required for DA sanders, HVLP automotive paint, and sandblasting.";
                compQuery = "DEWALT 60 Gallon Vertical Stationary Air Compressor 240V";
            }}

            if (process === "plasma") {{
                weldQuery = "YESWELDER CUT 55DS Pro 55 Amp Pilot Arc Plasma Cutter";
            }} else if (process === "tig") {{
                weldQuery = "PrimeWeld TIG225X 225 Amp AC DC TIG Welder with Pulse";
            }} else {{
                weldQuery = "YESWELDER MIG 205DS Pro 200A Multi Process MIG Welder";
            }}

            document.getElementById("recToolTitle").textContent = recTitle;
            document.getElementById("recToolDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(compQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(weldQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateShop);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-orange-600 transition block">
            <span class="text-[11px] font-bold text-orange-700 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-orange-700">Home & CFM Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-orange-700">Daily Shop Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-200 text-amber-950 px-3 py-1 rounded-lg">Shop Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">Output Spec</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Motor / Power</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Engineering</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Tank / Warranty</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-orange-600 hover:bg-orange-700 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate CFM & Welder Amps
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On CFM Airflow, Duty Cycle & Shop Performance Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-orange-700 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our workshop tool benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-orange-600 hover:bg-orange-700 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Workshop Equipment Reviews</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-orange-700">Home & CFM Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-orange-700">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-orange-100 text-orange-900 border border-orange-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-orange-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-orange-600 hover:bg-orange-700 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-orange-500 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-orange-600 hover:bg-orange-700 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "1/2\" Impact Wrench + 3/16\" Steel MIG Setup",
        "tool_cfm": 5.0,
        "psi": 90,
        "duty": 0.50,
        "metal_in": 0.1875,
        "process": "mig",
        "desc": "Calculate exact air compressor CFM @ 90 PSI, tank gallon size (10–80 gal), motor HP, and MIG/TIG/Plasma welding amperage for any metal thickness—plus read daily shop tool reviews."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Programmatic Tool CFM & Welder Amperage Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 3. Generate Cumulative Daily Product Review Pages (+1 new review unlocked every day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
