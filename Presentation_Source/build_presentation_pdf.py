import os
import math
import textwrap
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PIL import Image

PAGE_WIDTH = 1920
PAGE_HEIGHT = 1080

# ==============================================================================
# MODERN EXECUTIVE COLOR PALETTE & DESIGN TOKENS
# ==============================================================================
NAVY_DEEP = colors.HexColor('#071326')        # Deep Midnight Executive Navy
NAVY_PRIMARY = colors.HexColor('#0F2744')     # Primary Dark Header
NAVY_CARD = colors.HexColor('#132F56')        # Elevated Dark Card Fill
NAVY_BORDER = colors.HexColor('#1E3A8A')      # Accent Navy Border

BG_CANVAS = colors.HexColor('#F8FAFC')        # Clean Slate Pearl Canvas
CARD_BG = colors.HexColor('#FFFFFF')          # Pure Crisp White Card
CARD_ALT = colors.HexColor('#F1F5F9')         # Subtle Muted Slate Container
CARD_HOVER = colors.HexColor('#F8FAFC')       # Very Subtle Card Fill
SHADOW_COLOR = colors.HexColor('#E2E8F0')     # Drop Shadow Color
BORDER_LIGHT = colors.HexColor('#E2E8F0')     # Modern Micro Border
BORDER_ACTIVE = colors.HexColor('#CBD5E1')    # Active Outline

CYAN_GLOW = colors.HexColor('#06B6D4')        # Luminous Modern Cyan
TEAL_ACCENT = colors.HexColor('#0D9488')      # Academic Scientific Teal
SKY_BLUE = colors.HexColor('#0284C7')         # High-Contrast Ocean Blue
SKY_LIGHT = colors.HexColor('#E0F2FE')        # Sky Pill Tint
EMERALD_GREEN = colors.HexColor('#10B981')    # Success Emerald
INDIGO_ACCENT = colors.HexColor('#4F46E5')    # Deep Violet/Indigo Accent
AMBER_ACCENT = colors.HexColor('#F59E0B')     # Warning Gold/Amber
ROSE_ACCENT = colors.HexColor('#EF4444')      # Alert Coral/Rose

TEXT_DARK = colors.HexColor('#0F172A')        # Deep Slate Title
TEXT_BODY = colors.HexColor('#334155')        # Charcoal Slate Body
TEXT_MUTED = colors.HexColor('#64748B')       # Secondary Muted Text
TEXT_WHITE = colors.HexColor('#FFFFFF')       # Pure White

ASSET_DIR = r'Presentation_Assets'

def get_asset(filename):
    p = os.path.join(ASSET_DIR, filename)
    if os.path.exists(p):
        return p
    p_alt = os.path.join(r'Assignment/latex_documentation/Overleaf_LaTeX_Upload/output_image', filename)
    if os.path.exists(p_alt):
        return p_alt
    return p

# ==============================================================================
# MODERN UI PRIMITIVES & COMPONENTS
# ==============================================================================
def draw_header(c, page_num, title, subtitle, category="MSc DATA SCIENCE & COMPUTATIONAL INTELLIGENCE | DISSERTATION RESEARCH"):
    # Header dark banner
    c.setFillColor(NAVY_DEEP)
    c.rect(0, PAGE_HEIGHT - 112, PAGE_WIDTH, 112, fill=True, stroke=False)
    
    # Dual-tone luminous gradient glow bar (Cyan to Emerald)
    c.setFillColor(CYAN_GLOW)
    c.rect(0, PAGE_HEIGHT - 6, PAGE_WIDTH * 0.65, 6, fill=True, stroke=False)
    c.setFillColor(EMERALD_GREEN)
    c.rect(PAGE_WIDTH * 0.65, PAGE_HEIGHT - 6, PAGE_WIDTH * 0.35, 6, fill=True, stroke=False)
    
    # Category / Breadcrumb Pill
    draw_badge(c, 45, PAGE_HEIGHT - 32, category.upper(), bg=colors.HexColor('#0E223D'), text_color=CYAN_GLOW, font_size=10, pad_x=12, pad_y=4, border=CYAN_GLOW)
    
    # Main Slide Title
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(TEXT_WHITE)
    c.drawString(45, PAGE_HEIGHT - 66, title)
    
    # Subtitle / Scientific Scope
    c.setFont("Helvetica", 13.5)
    c.setFillColor(colors.HexColor('#94A3B8'))
    c.drawString(45, PAGE_HEIGHT - 92, subtitle)
    
    # Right-hand Metadata Card
    c.setFillColor(colors.HexColor('#0F2744'))
    c.setStrokeColor(NAVY_BORDER)
    c.setLineWidth(1)
    c.roundRect(PAGE_WIDTH - 435, PAGE_HEIGHT - 98, 390, 80, 8, fill=True, stroke=True)
    
    c.setFont("Helvetica-Bold", 12.5)
    c.setFillColor(TEXT_WHITE)
    c.drawRightString(PAGE_WIDTH - 60, PAGE_HEIGHT - 38, "Sadhana Adhikari (ID: 260102 | CUID: 17625409)")
    c.setFont("Helvetica", 11.5)
    c.setFillColor(colors.HexColor('#38BDF8'))
    c.drawRightString(PAGE_WIDTH - 60, PAGE_HEIGHT - 58, "Softwarica College (Coventry University, UK)")
    c.setFont("Helvetica-Bold", 10.5)
    c.setFillColor(colors.HexColor('#94A3B8'))
    c.drawRightString(PAGE_WIDTH - 60, PAGE_HEIGHT - 78, f"SLIDE {page_num} OF 5  •  IEEE CONFERENCE STYLE")

def draw_footer(c, page_num):
    # Bottom dividing line
    c.setFillColor(BORDER_LIGHT)
    c.rect(40, 42, PAGE_WIDTH - 80, 1.5, fill=True, stroke=False)
    
    # Footer metadata
    c.setFont("Helvetica", 10.5)
    c.setFillColor(TEXT_MUTED)
    c.drawString(45, 23, "Research Title: A Machine Learning Framework for Daily Rainfall Classification and Extreme Event Analysis in Kathmandu Watershed, Nepal")
    c.drawRightString(PAGE_WIDTH - 45, 23, "Department of Hydrology & Meteorology (DHM) & NASA GPM IMERG V07 (2016–2025) • Softwarica College")

def draw_card(c, x, y, w, h, bg=CARD_BG, border=BORDER_LIGHT, border_width=1.2, radius=10, shadow=True):
    if shadow:
        c.setFillColor(SHADOW_COLOR)
        c.roundRect(x + 2, y - 2, w, h, radius, fill=True, stroke=False)
    c.setFillColor(bg)
    if border:
        c.setStrokeColor(border)
        c.setLineWidth(border_width)
        c.roundRect(x, y, w, h, radius, fill=True, stroke=True)
    else:
        c.roundRect(x, y, w, h, radius, fill=True, stroke=False)

def draw_card_ribbon(c, x, y, w, h, title, ribbon_h=42, bg=NAVY_PRIMARY, text_color=TEXT_WHITE, font_size=13, radius=10):
    c.setFillColor(bg)
    c.roundRect(x, y + h - ribbon_h, w, ribbon_h, radius, fill=True, stroke=False)
    # square the bottom corners of ribbon
    c.rect(x, y + h - ribbon_h, w, 8, fill=True, stroke=False)
    c.setFont("Helvetica-Bold", font_size)
    c.setFillColor(text_color)
    c.drawString(x + 18, y + h - ribbon_h + (ribbon_h - font_size)/2 + 2, title)

def draw_badge(c, x, y, text, bg=SKY_LIGHT, text_color=SKY_BLUE, font_size=10, pad_x=10, pad_y=4, border=None, radius=5):
    c.setFont("Helvetica-Bold", font_size)
    text_width = c.stringWidth(text, "Helvetica-Bold", font_size)
    w = text_width + pad_x * 2
    h = font_size + pad_y * 2
    c.setFillColor(bg)
    if border:
        c.setStrokeColor(border)
        c.setLineWidth(1)
        c.roundRect(x, y, w, h, radius, fill=True, stroke=True)
    else:
        c.roundRect(x, y, w, h, radius, fill=True, stroke=False)
    c.setFillColor(text_color)
    c.drawString(x + pad_x, y + pad_y + 1, text)
    return w

def draw_metric_card(c, x, y, w, h, val, label, sublabel="", val_color=SKY_BLUE, bg=CARD_BG, border=BORDER_LIGHT):
    draw_card(c, x, y, w, h, bg=bg, border=border, radius=8, shadow=True)
    
    # Left accent indicator bar
    c.setFillColor(val_color)
    c.roundRect(x + 12, y + 14, 4, h - 28, 2, fill=True, stroke=False)
    
    # Metric value
    c.setFont("Helvetica-Bold", 23)
    c.setFillColor(val_color)
    c.drawString(x + 24, y + h - 34, str(val))
    
    # Label
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(TEXT_DARK)
    c.drawString(x + 24, y + h - 54, label)
    
    # Sublabel
    if sublabel:
        c.setFont("Helvetica", 9.5)
        c.setFillColor(TEXT_MUTED)
        c.drawString(x + 24, y + h - 70, sublabel)

def draw_image_fitted(c, img_path, x, y, w, h, border=True, border_color=BORDER_LIGHT, bg=CARD_BG, radius=8):
    if bg:
        c.setFillColor(bg)
        c.roundRect(x, y, w, h, radius, fill=True, stroke=False)
    
    if os.path.exists(img_path):
        try:
            with Image.open(img_path) as im:
                iw, ih = im.size
            aspect = iw / ih
            box_aspect = w / h
            
            if aspect > box_aspect:
                nw = w - 10
                nh = nw / aspect
            else:
                nh = h - 10
                nw = nh * aspect
            
            ix = x + (w - nw) / 2
            iy = y + (h - nh) / 2
            
            c.drawImage(img_path, ix, iy, width=nw, height=nh, preserveAspectRatio=True)
        except Exception as e:
            c.setFont("Helvetica", 11)
            c.setFillColor(TEXT_MUTED)
            c.drawCentredString(x + w/2, y + h/2, f"Image Load Error: {os.path.basename(img_path)}")
    else:
        c.setFont("Helvetica", 11)
        c.setFillColor(TEXT_MUTED)
        c.drawCentredString(x + w/2, y + h/2, f"Image not found: {os.path.basename(img_path)}")

    if border:
        c.setStrokeColor(border_color)
        c.setLineWidth(1.2)
        c.roundRect(x, y, w, h, radius, fill=False, stroke=True)

# ==============================================================================
# SLIDE 1: RESEARCH OVERVIEW & PROJECT INTRODUCTION
# ==============================================================================
def draw_slide_1(c):
    c.setFillColor(BG_CANVAS)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)
    
    draw_header(c, 1, 
                "A MACHINE LEARNING FRAMEWORK FOR DAILY RAINFALL CLASSIFICATION & EXTREME EVENT ANALYSIS", 
                "10-Year Multi-Source Ground-Satellite Synthesis (2016–2025) in the Kathmandu Watershed, Nepal",
                "RESEARCH OVERVIEW & PROJECT INTRODUCTION")
    
    # 6 Top Metric Cards
    metrics = [
        ("10 Years", "Temporal Coverage", "2016–2025 Complete Daily Data", SKY_BLUE),
        ("19 Stations", "Terrestrial Network", "Screened DHM Rain Gauges", TEAL_ACCENT),
        ("69,407", "Observation Records", "Station-Day Ground Points", NAVY_PRIMARY),
        ("~650 km²", "Watershed Domain", "1,280 m to 2,150+ masl Relief", INDIGO_ACCENT),
        ("5 Classes", "Intensity Schemes", "Standard WMO / DHM Tiers", AMBER_ACCENT),
        ("0.1° × 0.1°", "Satellite Ingestion", "NASA GPM IMERG V07 Gridded", EMERALD_GREEN)
    ]
    card_w = (PAGE_WIDTH - 90 - 5 * 16) / 6
    for i, (v, l, sl, clr) in enumerate(metrics):
        cx = 45 + i * (card_w + 16)
        draw_metric_card(c, cx, PAGE_HEIGHT - 200, card_w, 80, v, l, sl, val_color=clr)
        
    # Main Content Columns
    col_y = 55
    col_h = PAGE_HEIGHT - 270
    
    # Left Column: Research Background, Core Aim & Objectives (W: 1045)
    lw = 1045
    draw_card(c, 45, col_y, lw, col_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, 45, col_y, lw, col_h, "RESEARCH BACKGROUND, PROBLEM CONTEXT & OBJECTIVES", ribbon_h=42, bg=NAVY_PRIMARY, font_size=14)
    
    # Block 1: Motivation & Hazard Vulnerability Box
    bx = 65
    by = col_y + col_h - 60
    b_w = lw - 40
    
    draw_card(c, bx, by - 95, b_w, 95, bg=colors.HexColor('#FFFBEB'), border=colors.HexColor('#FDE68A'), radius=8, shadow=False)
    draw_badge(c, bx + 14, by - 24, "MOTIVATION & HAZARD VULNERABILITY", bg=colors.HexColor('#FEF3C7'), text_color=colors.HexColor('#B45309'), font_size=10)
    
    c.setFont("Helvetica", 11.5)
    c.setFillColor(TEXT_BODY)
    c.drawString(bx + 16, by - 46, "• Steep Himalayan Orography & Rapid Urbanization: Kathmandu Valley hosts >2.5 million residents in a complex, bowl-shaped basin.")
    c.drawString(bx + 16, by - 66, "• Severe Monsoon Flood Risk: >80% of precipitation falls during June–September; constrained river corridors cause catastrophic flash floods.")
    c.drawString(bx + 16, by - 86, "• Climate Hazard Vulnerability: Devastating cloudburst disasters (e.g. September 2024 flood) highlight the critical need for localized warnings.")
    
    # Block 2: Core Research Aim
    by2 = by - 110
    draw_card(c, bx, by2 - 75, b_w, 75, bg=colors.HexColor('#F0FDFA'), border=colors.HexColor('#CCFBF1'), radius=8, shadow=False)
    draw_badge(c, bx + 14, by2 - 24, "CORE RESEARCH AIM", bg=colors.HexColor('#CCFBF1'), text_color=colors.HexColor('#0F766E'), font_size=10)
    
    c.setFont("Helvetica-Bold", 12.5)
    c.setFillColor(NAVY_PRIMARY)
    c.drawString(bx + 16, by2 - 46, "Develop an operational Machine Learning classification framework for daily rainfall patterns and extreme storms")
    c.setFont("Helvetica", 11.8)
    c.setFillColor(TEXT_BODY)
    c.drawString(bx + 16, by2 - 66, "using 10 years of synchronous DHM ground observations and NASA GPM IMERG V07 satellite data to empower municipal disaster resilience.")
    
    # Block 3: 3 Specific Objectives (Modern Visual Cards)
    by3 = by2 - 90
    draw_badge(c, bx, by3, "SPECIFIC RESEARCH OBJECTIVES", bg=SKY_LIGHT, text_color=SKY_BLUE, font_size=10.5)
    
    objs = [
        ("01", "Spatial Microclimatic Patterns & Topographic Regimes:", 
         "Delineate microclimatic rainfall regimes across the watershed using Principal Component Analysis (PCA) and K-Means clustering, quantifying elevation lapse rate dependencies (+62.9 mm/100m).", SKY_BLUE),
        ("02", "Supervised ML Classification Under Extreme Class Imbalance:", 
         "Develop, optimize, and benchmark Random Forest, XGBoost, and Support Vector Machines (Linear & RBF) across five intensity categories under severe class imbalance, interpreted via SHAP.", TEAL_ACCENT),
        ("03", "Decadal Non-Parametric Climate Trend Detection (2016–2025):", 
         "Assess decadal changes in annual totals, seasonal concentration, rainy-day frequency, and extreme events using Mann–Kendall and Sen's slope methods under rigorous statistical significance.", INDIGO_ACCENT)
    ]
    
    card_oy = by3 - 15
    for num, o_title, o_desc, acc_c in objs:
        obj_h = 70
        draw_card(c, bx, card_oy - obj_h, b_w, obj_h, bg=CARD_ALT, border=BORDER_LIGHT, radius=6, shadow=False)
        
        # Number badge
        draw_badge(c, bx + 10, card_oy - 30, num, bg=acc_c, text_color=TEXT_WHITE, font_size=11, pad_x=8, pad_y=4, radius=4)
        
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(NAVY_PRIMARY)
        c.drawString(bx + 54, card_oy - 22, o_title)
        
        c.setFont("Helvetica", 11)
        c.setFillColor(TEXT_BODY)
        desc_lines = textwrap.wrap(o_desc, width=102)
        for d_idx, d_line in enumerate(desc_lines):
            c.drawString(bx + 54, card_oy - 42 - d_idx * 16, d_line)
        card_oy -= (obj_h + 10)
        
    # Block 4: Target Impact
    by4 = card_oy - 5
    draw_card(c, bx, by4 - 55, b_w, 55, bg=colors.HexColor('#F5F3FF'), border=colors.HexColor('#DDD6FE'), radius=6, shadow=False)
    draw_badge(c, bx + 12, by4 - 22, "DECISION-SUPPORT IMPACT", bg=colors.HexColor('#EDE9FE'), text_color=colors.HexColor('#6D28D9'), font_size=9.5)
    c.setFont("Helvetica", 11)
    c.setFillColor(TEXT_BODY)
    c.drawString(bx + 14, by4 - 42, "• Multi-Agency Utility: Directly serves Department of Hydrology & Meteorology (DHM), National Disaster Risk Reduction Authority,")
    c.drawString(bx + 14, by4 - 56, "  and Kathmandu Metropolitan City flood response units via an operational interactive Streamlit decision dashboard.")

    # Right Column: Study Domain Map & Topographic Stats (W: 765)
    rx = 1110
    rw = PAGE_WIDTH - 45 - rx
    draw_card(c, rx, col_y, rw, col_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, rx, col_y, rw, col_h, "STUDY DOMAIN: KATHMANDU WATERSHED & DHM NETWORK", ribbon_h=42, bg=NAVY_PRIMARY, font_size=13.5)
    
    # Study Area Map
    map_h = 425
    map_y = col_y + col_h - 42 - map_h - 12
    draw_image_fitted(c, get_asset('fig1_study_area_map.png'), rx + 12, map_y, rw - 24, map_h, border=True, border_color=BORDER_LIGHT)
    
    # Bottom info box on topography
    info_y = col_y + 12
    info_h = map_y - col_y - 20
    draw_card(c, rx + 12, info_y, rw - 24, info_h, bg=CARD_ALT, border=BORDER_LIGHT, radius=8, shadow=False)
    
    # Header tag
    draw_badge(c, rx + 24, info_y + info_h - 26, "GEOGRAPHICAL & OROGRAPHIC CHARACTERISTICS", bg=SKY_LIGHT, text_color=SKY_BLUE, font_size=9.5)
    
    topo_bullets = [
        ("Watershed Extent:", "Latitudes 27.55°N–27.85°N, Longitudes 85.20°E–85.55°E; Drainage Area: ~650 km²."),
        ("Elevation Profile:", "1,280 masl (Valley floor plain) to 2,147 masl (Nagarkot eastern ridge crest)."),
        ("Network Density:", "19 screened DHM stations: Kathmandu (10), Lalitpur (6), Bhaktapur (3)."),
        ("Rainfall Contrast:", "Annual mean ranges from 1,000.5 mm (Tikathali) to 2,341.0 mm (Sundarijal Mulkharka).")
    ]
    ty = info_y + info_h - 48
    for label, val in topo_bullets:
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(NAVY_PRIMARY)
        c.drawString(rx + 24, ty, "• " + label)
        c.setFont("Helvetica", 10.5)
        c.setFillColor(TEXT_BODY)
        c.drawString(rx + 140, ty, val)
        ty -= 20

    draw_footer(c, 1)

# ==============================================================================
# SLIDE 2: RESEARCH CHALLENGES, LITERATURE GAPS & PROPOSED METHODOLOGY
# ==============================================================================
def draw_slide_2(c):
    c.setFillColor(BG_CANVAS)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)
    
    draw_header(c, 2, 
                "RESEARCH CHALLENGES, IDENTIFIED GAPS & PROPOSED METHODOLOGY", 
                "Addressing Satellite Uncertainty, Severe Class Imbalance, and Orographic Microclimates",
                "PROBLEM FORMULATION & METHODOLOGICAL FRAMEWORK")
    
    col_w = (PAGE_WIDTH - 90 - 32) / 3
    
    # Top Row: The 3 Core Research Challenges (Y: 720 to 950, H: 230)
    top_y = 720
    top_h = 230
    
    ch_cards = [
        ("01", "CHALLENGE 1: SATELLITE UNCERTAINTY", colors.HexColor('#FEF2F2'), ROSE_ACCENT, [
            ("Overestimation Bias:", "Systematic positive bias of +2.78 mm/day (+46.12%) over Himalayan ridges."),
            ("High False Alarm Rate:", "False Alarm Ratio (FAR) = 46.12%; satellite flags light rain when gauges are dry."),
            ("Ridge Cloudburst Error:", "Coarse 0.1° (~11 km) gridded pixels miss localized high-intensity cloudburst cells.")
        ]),
        ("02", "CHALLENGE 2: SEVERE CLASS IMBALANCE", colors.HexColor('#FFFBEB'), AMBER_ACCENT, [
            ("Light Rain Dominance:", "Class 0 (<10 mm/d) represents 86.11% of all records (59,768 station-days)."),
            ("Extreme Event Rarity:", "Very Heavy (0.10%) and Extreme (0.013%) combined comprise only 0.11% (75 days)."),
            ("Standard Model Failure:", "Default loss functions maximize majority class accuracy, completely missing hazard events.")
        ]),
        ("03", "CHALLENGE 3: SPATIO-TEMPORAL COMPLEXITY", colors.HexColor('#F0FDFA'), TEAL_ACCENT, [
            ("Steep Orographic Relief:", "Elevation gradient from 1,280 to 2,150+ masl drives intense localized microclimates."),
            ("Monsoon Concentration:", ">80% of total annual precipitation is concentrated within 120 days (June–September)."),
            ("Shifting Decadal Baseline:", "Non-parametric trend detection needed to decouple climate shifts from seasonal noise.")
        ])
    ]
    
    for i, (num, title, bg_c, acc_c, bullets) in enumerate(ch_cards):
        cx = 45 + i * (col_w + 16)
        draw_card(c, cx, top_y, col_w, top_h, bg=CARD_BG, border=acc_c, border_width=1.5, radius=10, shadow=True)
        draw_card_ribbon(c, cx, top_y, col_w, top_h, f"{num}  {title}", ribbon_h=38, bg=acc_c, font_size=12.5)
        
        by = top_y + top_h - 58
        for b_title, b_desc in bullets:
            c.setFont("Helvetica-Bold", 11)
            c.setFillColor(NAVY_PRIMARY)
            c.drawString(cx + 16, by, "• " + b_title)
            c.setFont("Helvetica", 10.5)
            c.setFillColor(TEXT_BODY)
            lines = textwrap.wrap(b_desc, width=54)
            for l_idx, line in enumerate(lines):
                c.drawString(cx + 26, by - 16 - l_idx * 15, line)
            by -= (len(lines) * 15 + 20)
            
    # Middle Row: Literature Gaps & Innovations (Y: 535 to 705, H: 170)
    mid_y = 535
    mid_h = 170
    gaps = [
        ("GAP 1: LACK OF POINT-TO-GRID CALIBRATION",
         "Sharma et al. (2020) evaluated IMERG across Nepal but aggregated regionally, smoothing localized valley-ridge contrasts.",
         "Our Framework: Integrates station elevation and coordinates to calibrate satellite bias at specific gauge locations across steep terrain.", SKY_BLUE),
        ("GAP 2: ISOLATED TRENDS WITHOUT PREDICTION",
         "Khanal et al. (2024) analyzed decadal trends as retrospective statistics without connecting them to predictive classification.",
         "Our Framework: Unifies historical non-parametric trend modeling (Mann–Kendall/Sen) with multi-class forward-looking storm forecasting.", AMBER_ACCENT),
        ("GAP 3: BLACK-BOX ML LACKING EXPLAINABILITY",
         "Lei et al. (2025) benchmarked ML downscaling but treated models as black boxes without hydrological validation.",
         "Our Framework: Couples unsupervised spatial clustering (PCA/K-Means) with SHAP attribution to explain antecedent rainfall memory.", TEAL_ACCENT)
    ]
    for i, (g_title, g_prior, g_innov, acc_c) in enumerate(gaps):
        cx = 45 + i * (col_w + 16)
        draw_card(c, cx, mid_y, col_w, mid_h, bg=CARD_BG, border=BORDER_LIGHT, radius=8, shadow=True)
        
        draw_badge(c, cx + 14, mid_y + mid_h - 26, g_title, bg=CARD_ALT, text_color=acc_c, font_size=9.5)
        
        # Prior work
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(TEXT_MUTED)
        c.drawString(cx + 14, mid_y + mid_h - 43, "Prior Literature Limitation:")
        c.setFont("Helvetica", 9.5)
        c.setFillColor(TEXT_BODY)
        p_lines = textwrap.wrap(g_prior, width=74)
        py = mid_y + mid_h - 57
        for line in p_lines[:2]:
            c.drawString(cx + 14, py, line)
            py -= 13
            
        # Our innovation
        draw_badge(c, cx + 14, py - 4, "OUR NOVEL ADVANCEMENT ➔", bg=colors.HexColor('#F0FDFA'), text_color=TEAL_ACCENT, font_size=8.5)
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(NAVY_PRIMARY)
        i_lines = textwrap.wrap(g_innov.replace("Our Framework: ", ""), width=74)
        iy = py - 20
        for line in i_lines[:2]:
            c.drawString(cx + 14, iy, line)
            iy -= 13
        
    # Bottom Row: Visual Models (Y: 55 to 520, H: 465)
    bot_y = 55
    bot_h = 465
    w_p = 540
    w_w = 750
    w_m = PAGE_WIDTH - 90 - w_p - w_w - 32
    
    # 1. Problem Statement Conceptual Architecture
    draw_card(c, 45, bot_y, w_p, bot_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, 45, bot_y, w_p, bot_h, "Problem Statement Conceptual Architecture:", ribbon_h=34, bg=NAVY_PRIMARY, font_size=11.5)
    draw_image_fitted(c, get_asset('problem_statement_diagram.png'), 55, bot_y + 12, w_p - 20, bot_h - 48, border=False)
    
    # 2. Integrated ML Pipeline Infographic
    cx2 = 45 + w_p + 16
    draw_card(c, cx2, bot_y, w_w, bot_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, cx2, bot_y, w_w, bot_h, "Integrated 7-Stage Machine Learning Computational Pipeline:", ribbon_h=34, bg=NAVY_PRIMARY, font_size=11.5)
    draw_image_fitted(c, get_asset('Rainfall_Analysis_Workflow_Infographic.png'), cx2 + 10, bot_y + 12, w_w - 20, bot_h - 48, border=False)
    
    # 3. Monthly Precipitation Chart
    cx3 = cx2 + w_w + 16
    draw_card(c, cx3, bot_y, w_m, bot_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, cx3, bot_y, w_m, bot_h, "Monsoon Seasonality (2016–2025):", ribbon_h=34, bg=NAVY_PRIMARY, font_size=11.5)
    draw_image_fitted(c, get_asset('fig6_monthly_precipitation.png'), cx3 + 10, bot_y + 12, w_m - 20, bot_h - 48, border=False)
    
    draw_footer(c, 2)

# ==============================================================================
# SLIDE 3: DATASET ENGINEERING, MICROCLIMATIC CLUSTERING & ML ARCHITECTURE
# ==============================================================================
def draw_slide_3(c):
    c.setFillColor(BG_CANVAS)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)
    
    draw_header(c, 3, 
                "DATASET ENGINEERING, MICROCLIMATIC CLUSTERING & ML ARCHITECTURE", 
                "Spatio-Temporal Feature Structuring, 5-Tier Intensity Partitioning, and Unsupervised Topographic Regimes",
                "DATASET & METHODOLOGY SPECIFICATIONS")
    
    col_w = (PAGE_WIDTH - 90 - 32) / 3
    col_y = 55
    col_h = PAGE_HEIGHT - 180
    
    # --- Column 1: Screening, Tiers & Chronological Partitioning ---
    c1_x = 45
    draw_card(c, c1_x, col_y, col_w, col_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, c1_x, col_y, col_w, col_h, "1. DATASET SCREENING & 5 INTENSITY TIERS", ribbon_h=42, bg=NAVY_PRIMARY, font_size=13.5)
    
    # Screening bullets
    tx_y = col_y + col_h - 55
    draw_badge(c, c1_x + 16, tx_y, "TERRESTRIAL & SATELLITE HARMONIZATION", bg=CARD_ALT, text_color=NAVY_PRIMARY, font_size=9.5)
    
    bullets = [
        "• 21 Stations Screened: Tarebhir (100% missing) & Thankot (92.5%) dropped.",
        "• 19 Valid Gauges Retained: 3,694 missing observations linearly imputed.",
        "• NASA GPM IMERG V07: Synchronously matched at station coordinates (2016–2025)."
    ]
    sy = tx_y - 20
    for b in bullets:
        c.setFont("Helvetica", 10.5)
        c.setFillColor(TEXT_BODY)
        c.drawString(c1_x + 16, sy, b)
        sy -= 18
        
    # Table of 5 Tiers with Modern Styling & Visual Share Bars
    tbl_y = sy - 15
    draw_badge(c, c1_x + 16, tbl_y, "OPERATIONAL RAINFALL INTENSITY TIERS & SAMPLE DISTRIBUTION", bg=SKY_LIGHT, text_color=SKY_BLUE, font_size=9.5)
    
    table_top = tbl_y - 12
    t_cols = [135, 105, 95, 145, 100]
    headers = ["Class / Category", "Threshold", "Samples (N)", "Share (%) & Proportion", "Hazard Level"]
    
    # Header row
    hx = c1_x + 14
    c.setFillColor(NAVY_PRIMARY)
    c.roundRect(hx, table_top - 24, col_w - 28, 24, 4, fill=True, stroke=False)
    
    cur_x = hx
    for idx, (h_title, w) in enumerate(zip(headers, t_cols)):
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(TEXT_WHITE)
        if idx in [1, 2, 4]:
            c.drawCentredString(cur_x + w/2, table_top - 17, h_title)
        else:
            c.drawString(cur_x + 8, table_top - 17, h_title)
        cur_x += w
        
    rows = [
        ("Class 0: Light", "< 10 mm/d", "59,768", "86.11%", 86.11, "Routine", EMERALD_GREEN),
        ("Class 1: Moderate", "10–50 mm/d", "8,820", "12.71%", 12.71, "Advisory", SKY_BLUE),
        ("Class 2: Heavy", "50–100 mm/d", "744", "1.07%", 1.07, "Watch", AMBER_ACCENT),
        ("Class 3: Very Heavy", "100–200 mm/d", "66", "0.10%", 0.10, "Warning", ROSE_ACCENT),
        ("Class 4: Extreme", "≥ 200 mm/d", "9", "0.013%", 0.013, "Emergency", colors.HexColor('#991B1B'))
    ]
    
    ry = table_top - 24
    for r_idx, (c_name, thres, n_samp, share_s, share_pct, hazard, haz_c) in enumerate(rows):
        row_h = 28
        row_bg = CARD_ALT if r_idx % 2 == 1 else CARD_BG
        c.setFillColor(row_bg)
        c.rect(hx, ry - row_h, col_w - 28, row_h, fill=True, stroke=False)
        
        cur_x = hx
        # Col 0: Class Name
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(TEXT_DARK)
        c.drawString(cur_x + 8, ry - 19, c_name)
        cur_x += t_cols[0]
        
        # Col 1: Threshold
        c.setFont("Helvetica", 9.5)
        c.setFillColor(TEXT_BODY)
        c.drawCentredString(cur_x + t_cols[1]/2, ry - 19, thres)
        cur_x += t_cols[1]
        
        # Col 2: Samples
        c.drawCentredString(cur_x + t_cols[2]/2, ry - 19, n_samp)
        cur_x += t_cols[2]
        
        # Col 3: Share + Mini Visual Bar
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(TEXT_DARK)
        c.drawString(cur_x + 6, ry - 19, share_s)
        # Visual horizontal mini-bar
        bar_max_w = 75
        bar_w = max(2, (share_pct / 100.0) * bar_max_w)
        c.setFillColor(colors.HexColor('#CBD5E1'))
        c.roundRect(cur_x + 55, ry - 19, bar_max_w, 6, 2, fill=True, stroke=False)
        c.setFillColor(haz_c)
        c.roundRect(cur_x + 55, ry - 19, bar_w, 6, 2, fill=True, stroke=False)
        cur_x += t_cols[3]
        
        # Col 4: Hazard Badge
        draw_badge(c, cur_x + 10, ry - 22, hazard, bg=CARD_BG, text_color=haz_c, font_size=8.5, pad_x=8, pad_y=3, border=haz_c)
        
        ry -= row_h
        
    # Chronological Dataset Split Box
    sp_y = col_y + 15
    sp_h = ry - col_y - 25
    draw_card(c, c1_x + 14, sp_y, col_w - 28, sp_h, bg=CARD_ALT, border=BORDER_LIGHT, radius=8, shadow=False)
    draw_badge(c, c1_x + 24, sp_y + sp_h - 26, "CHRONOLOGICAL DATASET PARTITIONING (LEAK-FREE)", bg=CARD_BG, text_color=NAVY_PRIMARY, font_size=9.5)
    
    splits = [
        ("Training Set (70.0%):", "2016–2022 (7 Years) | N = 48,583 samples", "Full annual cycles establishing base parameters without future awareness.", SKY_BLUE),
        ("Validation Set (20.0%):", "2023–2024 (2 Years) | N = 13,889 samples", "Hyperparameter optimization, probability threshold calibration & regularization.", AMBER_ACCENT),
        ("Independent Test (10.0%):", "2025 Holdout (1 Year) | N = 6,935 samples", "Strict forward temporal generalization benchmark simulating real deployment.", EMERALD_GREEN)
    ]
    cur_sy = sp_y + sp_h - 48
    for s_title, s_span, s_desc, acc_c in splits:
        draw_badge(c, c1_x + 24, cur_sy - 12, s_title, bg=CARD_BG, text_color=acc_c, font_size=9, pad_x=6, pad_y=2, border=acc_c)
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(TEXT_DARK)
        c.drawString(c1_x + 160, cur_sy - 8, s_span)
        c.setFont("Helvetica", 9.5)
        c.setFillColor(TEXT_MUTED)
        c.drawString(c1_x + 24, cur_sy - 26, s_desc)
        cur_sy -= 44
        
    draw_badge(c, c1_x + 24, sp_y + 10, "SPATIAL VALIDATION: Leave-One-District-Out (LODO) across KTM, LLT, BKT", bg=colors.HexColor('#CCFBF1'), text_color=TEAL_ACCENT, font_size=9)

    # --- Column 2: Unsupervised Microclimatic Clustering ---
    c2_x = c1_x + col_w + 16
    draw_card(c, c2_x, col_y, col_w, col_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, c2_x, col_y, col_w, col_h, "2. UNSUPERVISED MICROCLIMATIC CLUSTERING", ribbon_h=42, bg=NAVY_PRIMARY, font_size=13.5)
    
    img_h1 = 225
    img_y1 = col_y + col_h - 42 - img_h1 - 10
    draw_image_fitted(c, get_asset('kmeans_optimal_k.png'), c2_x + 16, img_y1, col_w - 32, img_h1, border=True)
    
    c.setFont("Helvetica", 9.5)
    c.setFillColor(TEXT_MUTED)
    c.drawCentredString(c2_x + col_w/2, img_y1 - 14, "Elbow & Silhouette Score: Confirms K=3 as optimal regime partition (Silhouette = 0.584)")
    
    img_h2 = 220
    img_y2 = img_y1 - 20 - img_h2 - 10
    draw_image_fitted(c, get_asset('fig8_pca_clusters_3d.png'), c2_x + 16, img_y2, col_w - 32, img_h2, border=True)
    
    c.setFont("Helvetica", 9.5)
    c.setFillColor(TEXT_MUTED)
    c.drawCentredString(c2_x + col_w/2, img_y2 - 14, "PCA Cluster Space: Visualizes clear geometric separation driven by elevation gradients")
    
    # Regimes Box
    reg_y = col_y + 15
    reg_h = img_y2 - 25 - reg_y
    draw_card(c, c2_x + 16, reg_y, col_w - 32, reg_h, bg=CARD_ALT, border=BORDER_LIGHT, radius=8, shadow=False)
    draw_badge(c, c2_x + 24, reg_y + reg_h - 26, "THREE DELINEATED MICROCLIMATIC RAINFALL REGIMES", bg=CARD_BG, text_color=NAVY_PRIMARY, font_size=9.5)
    
    regimes = [
        ("Regime 0 (Valley Floor):", "1,300–1,400 masl (10 stations: Airport, Khumaltar); 1,350–1,500 mm/year.", SKY_BLUE),
        ("Regime 1 (Mid-Slopes):", "1,400–1,600 masl (6 stations: Godavari, Lele, Chapagaun); 1,600–1,850 mm/year.", TEAL_ACCENT),
        ("Regime 2 (Ridge-Tops):", ">1,600 masl (3 stations: Nagarkot, Sundarijal Mulkharka); >2,000 mm/year.", INDIGO_ACCENT)
    ]
    ry = reg_y + reg_h - 50
    for r_title, r_desc, acc_c in regimes:
        draw_badge(c, c2_x + 24, ry - 10, r_title, bg=CARD_BG, text_color=acc_c, font_size=9, pad_x=6, pad_y=2, border=acc_c)
        c.setFont("Helvetica", 10)
        c.setFillColor(TEXT_BODY)
        c.drawString(c2_x + 175, ry - 6, r_desc)
        ry -= 30

    # --- Column 3: Isohyet Lapse Rate & Model Architecture ---
    c3_x = c2_x + col_w + 16
    draw_card(c, c3_x, col_y, col_w, col_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, c3_x, col_y, col_w, col_h, "3. ISOHYET LAPSE RATE & MODEL SUITE", ribbon_h=42, bg=NAVY_PRIMARY, font_size=13.5)
    
    iso_h = 330
    iso_y = col_y + col_h - 42 - iso_h - 10
    draw_image_fitted(c, get_asset('isohyet_map_and_elevation_chart.png'), c3_x + 16, iso_y, col_w - 32, iso_h, border=True)
    
    c.setFont("Helvetica", 10)
    c.setFillColor(TEXT_MUTED)
    c.drawCentredString(c3_x + col_w/2, iso_y - 14, "Isohyetal Map & Lapse Rate: Physical increase of +62.9 mm rain per 100 m elevation rise")
    
    # Model Suite Cards
    ms_y = col_y + 15
    ms_h = iso_y - 25 - col_y - 15
    draw_card(c, c3_x + 16, ms_y, col_w - 32, ms_h, bg=CARD_ALT, border=BORDER_LIGHT, radius=8, shadow=False)
    draw_badge(c, c3_x + 24, ms_y + ms_h - 26, "EVALUATED SUPERVISED MACHINE LEARNING SUITE", bg=CARD_BG, text_color=NAVY_PRIMARY, font_size=9.5)
    
    models = [
        ("Random Forest (RF):", "Ensemble of 15 trees, max depth 3, balanced class weights.", "High variance reduction, resilient to feature noise, preserves rare storm classes.", EMERALD_GREEN),
        ("XGBoost Classifier:", "50 boosted trees, max depth 3, lr 0.01, multi:softprob.", "Regularized objective function minimizes over-fitting on minority storm classes.", AMBER_ACCENT),
        ("Linear SVM (Scaled):", "Linear Kernel Support Vector Classifier, C = 0.1, balanced.", "Maximizes geometric margin between classes in standardized feature space.", SKY_BLUE),
        ("RBF SVM (Scaled):", "Radial Basis Kernel Support Vector Classifier, C = 1.0, gamma = scale.", "Projects inputs into non-linear Hilbert space to form complex decision boundaries.", INDIGO_ACCENT)
    ]
    my = ms_y + ms_h - 48
    for m_title, m_spec, m_desc, acc_c in models:
        draw_badge(c, c3_x + 24, my - 10, m_title, bg=CARD_BG, text_color=acc_c, font_size=9, pad_x=6, pad_y=2, border=acc_c)
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(NAVY_PRIMARY)
        c.drawString(c3_x + 160, my - 6, m_spec)
        c.setFont("Helvetica", 9.5)
        c.setFillColor(TEXT_MUTED)
        c.drawString(c3_x + 24, my - 24, m_desc)
        my -= 42
        
    draw_footer(c, 3)

# ==============================================================================
# SLIDE 4: EXPERIMENTAL RESULTS, MODEL BENCHMARKING & EXPLAINABLE AI (XAI)
# ==============================================================================
def draw_slide_4(c):
    c.setFillColor(BG_CANVAS)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)
    
    draw_header(c, 4, 
                "EXPERIMENTAL RESULTS, MODEL BENCHMARKING & EXPLAINABLE AI (XAI)", 
                "Comparative Evaluation on Independent 2025 Test Set (N = 6,935) & SHAP Hydrological Attribution",
                "EXPERIMENTAL BENCHMARK & EVALUATION")
    
    top_y = 730
    top_h = 220
    top_lw = 1080
    top_rw = PAGE_WIDTH - 90 - top_lw - 16
    
    # Left: Evaluation Benchmark Table Card
    draw_card(c, 45, top_y, top_lw, top_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, 45, top_y, top_lw, top_h, "INDEPENDENT 2025 TEST SET BENCHMARK RESULTS (N = 6,935 STATION-DAYS, 19 DHM STATIONS)", ribbon_h=38, bg=NAVY_PRIMARY, font_size=12)
    
    # Benchmark Leaderboard Table
    tbl_top = top_y + top_h - 48
    cols_w = [210, 115, 130, 125, 125, 125, 115, 115]
    h_bench = ["Evaluated Classifier", "Accuracy", "Balanced Acc.", "Weighted Prec.", "Weighted Rec.", "Weighted F1", "Macro F1", "Macro ROC-AUC"]
    
    # Header row
    c.setFillColor(NAVY_PRIMARY)
    c.roundRect(55, tbl_top - 24, top_lw - 20, 24, 4, fill=True, stroke=False)
    
    cur_x = 55
    for idx, (h_title, w) in enumerate(zip(h_bench, cols_w)):
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(TEXT_WHITE)
        if idx > 0:
            c.drawCentredString(cur_x + w/2, tbl_top - 17, h_title)
        else:
            c.drawString(cur_x + 10, tbl_top - 17, h_title)
        cur_x += w
        
    rows_bench = [
        ("Random Forest", "69.46%", "59.80% (Best)", "87.20%", "69.46%", "75.51%", "0.3446", "0.87", False, True, False),
        ("XGBoost Classifier", "70.48%", "45.00%", "86.53%", "70.48%", "76.37%", "0.3310", "0.88 (Best)", False, False, True),
        ("Linear SVM (Scaled)", "74.72% (Best)", "59.54%", "85.88%", "74.72% (Best)", "78.92% (Best)", "0.3682 (Best)", "0.84", True, False, False),
        ("RBF SVM (Scaled)", "70.22%", "42.62%", "87.19%", "70.22%", "76.26%", "0.3226", "0.80", False, False, False)
    ]
    
    ry = tbl_top - 24
    for r_idx, (m_name, acc, b_acc, w_pr, w_rec, w_f1, m_f1, m_auc, is_lin, is_rf, is_xgb) in enumerate(rows_bench):
        row_h = 29
        row_bg = colors.HexColor('#F8FAFC') if r_idx % 2 == 1 else CARD_BG
        if is_lin:
            row_bg = colors.HexColor('#F0FDF4') # Subtle highlight for overall winner
        c.setFillColor(row_bg)
        c.rect(55, ry - row_h, top_lw - 20, row_h, fill=True, stroke=False)
        
        cur_x = 55
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(NAVY_PRIMARY)
        c.drawString(cur_x + 10, ry - 19, m_name)
        cur_x += cols_w[0]
        
        vals = [acc, b_acc, w_pr, w_rec, w_f1, m_f1, m_auc]
        for v_idx, val in enumerate(vals):
            w = cols_w[v_idx + 1]
            if "(Best)" in val:
                c.setFont("Helvetica-Bold", 10)
                c.setFillColor(EMERALD_GREEN)
            else:
                c.setFont("Helvetica", 10)
                c.setFillColor(TEXT_BODY)
            c.drawCentredString(cur_x + w/2, ry - 19, val)
            cur_x += w
        ry -= row_h
        
    # Right: Operational Selection Logic Card
    cx_r = 45 + top_lw + 16
    draw_card(c, cx_r, top_y, top_rw, top_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, cx_r, top_y, top_rw, top_h, "OPERATIONAL TRADE-OFFS & SELECTION LOGIC", ribbon_h=38, bg=NAVY_PRIMARY, font_size=12)
    
    logic_bullets = [
        ("Linear SVM (Operational Winner):", "Highest accuracy (74.72%) and weighted F1 (78.92%) with instant sub-millisecond inference, optimal for routine municipal daily forecasts.", SKY_BLUE),
        ("Random Forest (Life-Safety Winner):", "Highest balanced accuracy (59.80%) and captured 80.00% (8/10) of Class 3 Very Heavy Storms, critical for flash flood mitigation.", EMERALD_GREEN),
        ("XGBoost (Discriminative Power):", "Delivered highest Macro ROC-AUC (0.88) and best Heavy Rain recall (42.65%), providing smooth calibrated risk probabilities.", AMBER_ACCENT),
        ("Key Deployment Synthesis:", "No single algorithm dominates all metrics; an operational ensemble or threshold-switched deployment balances precision with extreme event recall.", NAVY_PRIMARY)
    ]
    by = top_y + top_h - 48
    for b_title, b_desc, acc_c in logic_bullets:
        draw_badge(c, cx_r + 14, by - 4, b_title, bg=CARD_ALT, text_color=acc_c, font_size=8.8, pad_x=6, pad_y=2, border=acc_c)
        c.setFont("Helvetica", 9)
        c.setFillColor(TEXT_BODY)
        lines = textwrap.wrap(b_desc, width=88)
        for l_idx, line in enumerate(lines):
            c.drawString(cx_r + 16, by - 18 - l_idx * 12, line)
        by -= (len(lines) * 12 + 22)
        
    # Bottom 3 Evaluation Diagnostic Columns
    bot_y = 55
    bot_h = 660
    b_col_w = (PAGE_WIDTH - 90 - 32) / 3
    
    # 1. Confusion Matrix & ROC Curves
    bc1_x = 45
    draw_card(c, bc1_x, bot_y, b_col_w, bot_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, bc1_x, bot_y, b_col_w, bot_h, "Multi-Model Evaluation Diagnostics (2025 Test):", ribbon_h=34, bg=NAVY_PRIMARY, font_size=11.5)
    
    h_sub = (bot_h - 60) / 2
    draw_image_fitted(c, get_asset('confusion_matrices.png'), bc1_x + 12, bot_y + h_sub + 20, b_col_w - 24, h_sub - 10, border=True)
    draw_image_fitted(c, get_asset('roc_curves.png'), bc1_x + 12, bot_y + 20, b_col_w - 24, h_sub - 10, border=True)
    
    # 2. Per-Class Accuracy & Satellite Scatter
    bc2_x = bc1_x + b_col_w + 16
    draw_card(c, bc2_x, bot_y, b_col_w, bot_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, bc2_x, bot_y, b_col_w, bot_h, "Per-Class Accuracy & Satellite Baseline Validation:", ribbon_h=34, bg=NAVY_PRIMARY, font_size=11.5)
    
    draw_image_fitted(c, get_asset('per_class_metrics_barchart.png'), bc2_x + 12, bot_y + h_sub + 20, b_col_w - 24, h_sub - 10, border=True)
    draw_image_fitted(c, get_asset('dhm_vs_gpm_scatter.png'), bc2_x + 12, bot_y + 20, b_col_w - 24, h_sub - 10, border=True)
    
    # 3. Explainable AI & Feature Importance
    bc3_x = bc2_x + b_col_w + 16
    draw_card(c, bc3_x, bot_y, b_col_w, bot_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, bc3_x, bot_y, b_col_w, bot_h, "Explainable AI (XAI) & Antecedent Rainfall Memory:", ribbon_h=34, bg=NAVY_PRIMARY, font_size=11.5)
    
    shap_h = 240
    shap_y = bot_y + bot_h - 35 - shap_h - 5
    draw_image_fitted(c, get_asset('shap_summary.png'), bc3_x + 12, shap_y, b_col_w - 24, shap_h, border=True)
    
    feat_h = 210
    feat_y = shap_y - feat_h - 15
    draw_image_fitted(c, get_asset('feature_importance.png'), bc3_x + 12, feat_y, b_col_w - 24, feat_h, border=True)
    
    # Insights box
    ins_y = bot_y + 15
    ins_h = feat_y - bot_y - 25
    draw_card(c, bc3_x + 12, ins_y, b_col_w - 24, ins_h, bg=CARD_ALT, border=BORDER_LIGHT, radius=8, shadow=False)
    draw_badge(c, bc3_x + 22, ins_y + ins_h - 26, "PHYSICAL HYDROLOGICAL INSIGHTS FROM SHAP", bg=CARD_BG, text_color=NAVY_PRIMARY, font_size=9.5)
    
    xai_points = [
        ("Dominant Memory:", "1-Day Lag (P_t-1) accounts for 74.47% relative feature gain."),
        ("Multi-Day Persistence:", "3-Day Lag (P_t-3) provides 9.47%; concurrent satellite = 6.30%."),
        ("Physical Catchment Priming:", "Prior rain saturates the mountain basin, primes soil moisture and humidity, triggering catastrophic high-velocity runoff.")
    ]
    py = ins_y + ins_h - 46
    for p_title, p_desc in xai_points:
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(NAVY_PRIMARY)
        c.drawString(bc3_x + 24, py, "• " + p_title)
        c.setFont("Helvetica", 9.5)
        c.setFillColor(TEXT_BODY)
        lines = textwrap.wrap(p_desc, width=64)
        for l_idx, line in enumerate(lines):
            c.drawString(bc3_x + 34, py - 14 - l_idx * 13, line)
        py -= (len(lines) * 13 + 18)
        
    draw_footer(c, 4)

# ==============================================================================
# SLIDE 5: DECADAL CLIMATE TRENDS, OPERATIONAL DASHBOARD & FUTURE WORK
# ==============================================================================
def draw_slide_5(c):
    c.setFillColor(BG_CANVAS)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)
    
    draw_header(c, 5, 
                "DECADAL CLIMATE TRENDS, OPERATIONAL DASHBOARD & FUTURE WORK", 
                "Mann–Kendall Trend Verification (2016–2025), Streamlit Decision Support, and Scientific Conclusions",
                "CLIMATOLOGICAL TRENDS & OPERATIONAL DEPLOYMENT")
    
    # Top Section: Trend Detection & Attribution Rigor (Y: 695 to 945, H: 250)
    top_y = 695
    top_h = 250
    t_lw = 1080
    t_rw = PAGE_WIDTH - 90 - t_lw - 16
    
    # Left Card: Trend Table
    draw_card(c, 45, top_y, t_lw, top_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, 45, top_y, t_lw, top_h, "DECADAL CLIMATE TREND DETECTION ACROSS KATHMANDU WATERSHED (2016–2025)", ribbon_h=38, bg=NAVY_PRIMARY, font_size=12)
    
    tbl_top = top_y + top_h - 48
    t_cols = [240, 140, 140, 180, 180, 180]
    h_trend = ["Climatological Metric", "Kendall's Tau (τ)", "p-Value", "Sen's Slope (Q)", "Statistical Trend Result", "Climatological Significance"]
    
    c.setFillColor(NAVY_PRIMARY)
    c.roundRect(55, tbl_top - 24, t_lw - 20, 24, 4, fill=True, stroke=False)
    
    cur_x = 55
    for idx, (h_title, w) in enumerate(zip(h_trend, t_cols)):
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(TEXT_WHITE)
        if idx > 0:
            c.drawCentredString(cur_x + w/2, tbl_top - 17, h_title)
        else:
            c.drawString(cur_x + 10, tbl_top - 17, h_title)
        cur_x += w
        
    rows_trend = [
        ("Annual Mean Rainfall", "+0.5111", "0.0491*", "+0.2012 mm/year", "Statistically Increasing", "Significant at 95% Conf (p < 0.05)", True),
        ("Maximum Daily Rainfall", "+0.3556", "0.1780", "+2.4800 mm/year", "Positive Upward Slope", "Intensifying Peaks (Not Stat. Sig.)", False),
        ("Rainy Days (> 1 mm/day)", "+0.3778", "0.1524", "+40.1667 days/year", "Positive Upward Slope", "Extended Wet Spells (Not Stat. Sig.)", False),
        ("Extreme Storms (> 100 mm/day)", "+0.3778", "0.1491", "+0.8889 events/year", "Positive Upward Slope", "Frequent Cloudbursts (Not Stat. Sig.)", False)
    ]
    
    ry = tbl_top - 24
    for r_idx, (m_name, tau, p_val, slope, res, sig, is_sig) in enumerate(rows_trend):
        row_h = 32
        row_bg = colors.HexColor('#F0FDF4') if is_sig else (colors.HexColor('#F8FAFC') if r_idx % 2 == 1 else CARD_BG)
        c.setFillColor(row_bg)
        c.rect(55, ry - row_h, t_lw - 20, row_h, fill=True, stroke=False)
        
        cur_x = 55
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(NAVY_PRIMARY)
        c.drawString(cur_x + 10, ry - 21, m_name)
        cur_x += t_cols[0]
        
        vals = [tau, p_val, slope, res, sig]
        for v_idx, val in enumerate(vals):
            w = t_cols[v_idx + 1]
            if is_sig:
                c.setFont("Helvetica-Bold", 10)
                c.setFillColor(EMERALD_GREEN)
            else:
                c.setFont("Helvetica", 10)
                c.setFillColor(TEXT_BODY)
            c.drawCentredString(cur_x + w/2, ry - 21, val)
            cur_x += w
        ry -= row_h
        
    # Right Card: Rigor & Attribution Box
    cx_r = 45 + t_lw + 16
    draw_card(c, cx_r, top_y, t_rw, top_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, cx_r, top_y, t_rw, top_h, "SCIENTIFIC RIGOR & ATTRIBUTION NOTICE", ribbon_h=38, bg=NAVY_PRIMARY, font_size=12)
    
    rig_y = top_y + top_h - 52
    draw_badge(c, cx_r + 14, rig_y - 6, "ACADEMIC HONESTY & CLIMATOLOGICAL BOUNDARY", bg=colors.HexColor('#FEF3C7'), text_color=AMBER_ACCENT, font_size=9)
    
    rig_bullets = [
        ("Statistical Significance:", "Only Annual Mean Rainfall reached statistical significance (p = 0.0491 < 0.05). Maximum daily peaks and extreme events showed strong positive slopes (+2.48 mm/yr, +0.89 events/yr) but remained p > 0.05."),
        ("Attribution Boundary:", "A 10-year observational series (2016–2025) reliably documents localized decadal climate variability and current hazard risk. Formal anthropogenic attribution requires multi-decadal records (≥30 years) and global coupled climate simulations.")
    ]
    by = rig_y - 32
    for b_title, b_desc in rig_bullets:
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(NAVY_PRIMARY)
        c.drawString(cx_r + 16, by, "• " + b_title)
        c.setFont("Helvetica", 9.5)
        c.setFillColor(TEXT_BODY)
        lines = textwrap.wrap(b_desc, width=64)
        for l_idx, line in enumerate(lines):
            c.drawString(cx_r + 26, by - 14 - l_idx * 13, line)
        by -= (len(lines) * 13 + 20)
        
    # Middle Section: Operational Dashboard (Y: 345 to 680, H: 335)
    mid_y = 345
    mid_h = 335
    draw_card(c, 45, mid_y, PAGE_WIDTH - 90, mid_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, 45, mid_y, PAGE_WIDTH - 90, mid_h, "OPERATIONAL RESEARCH DASHBOARD: INTERACTIVE DECISION-SUPPORT APPLICATION (dashboard.py)", ribbon_h=38, bg=NAVY_PRIMARY, font_size=12.5)
    
    draw_badge(c, PAGE_WIDTH - 45 - 340, mid_y + mid_h - 30, "LOCALHOST DEPLOYED @ STREAMLIT ENGINE", bg=colors.HexColor('#0E223D'), text_color=CYAN_GLOW, font_size=9, pad_x=10, pad_y=3, border=CYAN_GLOW)
    
    dashboards = [
        ("dashboard_sec1_overview.png", "1. Overview & EDA", "3D animated metric cards"),
        ("dashboard_sec2_spatial_bias.png", "2. Spatial Bias", "Geospatial error heatmap"),
        ("dashboard_sec3_clustering_pca.png", "3. PCA Regimes", "Interactive 3D scatter"),
        ("dashboard_sec4_model_eval.png", "4. Model Benchmarks", "Confusion matrix & ROC"),
        ("dashboard_sec5_trend_analysis.png", "5. Decadal Trends", "Time series & OLS slider"),
        ("dashboard_sec6_live_prediction.png", "6. Live Inference", "Real-time rainfall slider")
    ]
    d_w = (PAGE_WIDTH - 90 - 30 - 5 * 12) / 6
    d_h = mid_h - 55 - 45
    d_y = mid_y + 15
    for i, (fn, title_s, sub_s) in enumerate(dashboards):
        dx = 60 + i * (d_w + 12)
        draw_image_fitted(c, get_asset(fn), dx, d_y + 35, d_w, d_h, border=True, border_color=BORDER_LIGHT)
        
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(NAVY_PRIMARY)
        c.drawCentredString(dx + d_w/2, d_y + 20, title_s)
        c.setFont("Helvetica", 9)
        c.setFillColor(TEXT_MUTED)
        c.drawCentredString(dx + d_w/2, d_y + 6, sub_s)

    # Bottom Section: Conclusions & Future Work (Y: 55 to 330, H: 275)
    bot_y = 55
    bot_h = 275
    b_lw = 930
    b_rw = PAGE_WIDTH - 90 - b_lw - 16
    
    # Left Card: Contributions
    draw_card(c, 45, bot_y, b_lw, bot_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, 45, bot_y, b_lw, bot_h, "KEY RESEARCH CONTRIBUTIONS & SCIENTIFIC FINDINGS", ribbon_h=38, bg=NAVY_PRIMARY, font_size=12.5)
    
    contributions = [
        ("Integrated 10-Year Multi-Source Dataset:", "Harmonized 69,407 station-days from 19 DHM gauges with NASA GPM IMERG V07 satellite.", SKY_BLUE),
        ("Satellite Bias Profiling:", "Proven that raw satellite systematically overestimates light rain (MB = +2.78 mm/d, FAR = 46.12%).", ROSE_ACCENT),
        ("Topographic Microclimates:", "Delineated 3 elevation rainfall regimes via PCA & K-Means (Silhouette = 0.584, lapse rate = +62.9 mm/100m).", TEAL_ACCENT),
        ("Machine Learning Under Imbalance:", "Linear SVM achieved 74.72% accuracy; Random Forest captured 80.00% of very heavy storms.", EMERALD_GREEN),
        ("Hydrologic Explainability:", "SHAP attribution revealed prior 1–3 day rainfall memory accounts for 83.94% of total predictive gain.", INDIGO_ACCENT),
        ("Operational Software Delivery:", "Built an interactive Streamlit decision-support web dashboard for real-time hazard evaluation.", AMBER_ACCENT)
    ]
    cy = bot_y + bot_h - 52
    for c_title, c_desc, acc_c in contributions:
        draw_badge(c, 60, cy - 8, c_title, bg=CARD_ALT, text_color=acc_c, font_size=9, pad_x=6, pad_y=2, border=acc_c)
        c.setFont("Helvetica", 9.8)
        c.setFillColor(TEXT_BODY)
        c.drawString(60 + 265, cy - 4, c_desc)
        cy -= 34

    # Right Card: Future Horizons & Vision
    cx_rw = 45 + b_lw + 16
    draw_card(c, cx_rw, bot_y, b_rw, bot_h, bg=CARD_BG, border=BORDER_LIGHT, radius=10, shadow=True)
    draw_card_ribbon(c, cx_rw, bot_y, b_rw, bot_h, "FUTURE HORIZONS & STRATEGIC ROADMAP", ribbon_h=38, bg=NAVY_PRIMARY, font_size=12.5)
    
    futures = [
        ("High-Resolution Radar Assimilation:", "Integrate X-band dual-polarization weather radar for micro-scale convective tracking."),
        ("Deep Recurrent Architectures:", "Evaluate LSTM and Temporal Convolutional Networks (TCN) for sub-daily hourly flash flood forecasts."),
        ("High-Altitude Ridge Monitoring:", "Deploy solar-powered IoT tipping-bucket rain gauges across unmonitored ridgelines (>2,200 masl)."),
        ("Municipal Early Warning Integration:", "Connect ML model inference API directly into Kathmandu Metropolitan disaster dispatch.")
    ]
    fy = bot_y + bot_h - 52
    for f_title, f_desc in futures:
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(NAVY_PRIMARY)
        c.drawString(cx_rw + 16, fy, "• " + f_title)
        c.setFont("Helvetica", 9.5)
        c.setFillColor(TEXT_BODY)
        c.drawString(cx_rw + 26, fy - 14, f_desc)
        fy -= 32
        
    # Closing Vision Banner
    v_y = bot_y + 12
    v_h = fy - bot_y - 12
    draw_card(c, cx_rw + 14, v_y, b_rw - 28, v_h, bg=NAVY_DEEP, border=CYAN_GLOW, border_width=1.5, radius=8, shadow=False)
    
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(CYAN_GLOW)
    c.drawCentredString(cx_rw + b_rw/2, v_y + v_h - 22, "CLOSING RESEARCH VISION")
    
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(TEXT_WHITE)
    c.drawCentredString(cx_rw + b_rw/2, v_y + v_h - 42, '"Towards Explainable, Data-Driven and Spatially Aware Rainfall Intelligence')
    c.drawCentredString(cx_rw + b_rw/2, v_y + v_h - 58, 'for Climate-Resilient Kathmandu."')

    draw_footer(c, 5)

# ==============================================================================
# MASTER BUILD ROUTINE
# ==============================================================================
def build_presentation_pdf(output_filename):
    print(f"Building 5-Page Presentation PDF: {output_filename}...")
    c = canvas.Canvas(output_filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    print("Rendering Slide 1: Introduction & Research Overview...")
    draw_slide_1(c)
    c.showPage()
    
    print("Rendering Slide 2: Problem Statement & Literature Gap...")
    draw_slide_2(c)
    c.showPage()
    
    print("Rendering Slide 3: Dataset, Methodology & ML Architecture...")
    draw_slide_3(c)
    c.showPage()
    
    print("Rendering Slide 4: Experimental Results & Explainable AI...")
    draw_slide_4(c)
    c.showPage()
    
    print("Rendering Slide 5: Climate Trends, Dashboard & Future Work...")
    draw_slide_5(c)
    c.showPage()
    
    c.save()
    print(f"Successfully generated: {output_filename} ({os.path.getsize(output_filename)} bytes)")

if __name__ == '__main__':
    out_pdf = 'Kathmandu_Rainfall_ML_Research_Presentation_Vector.pdf'
    build_presentation_pdf(out_pdf)
