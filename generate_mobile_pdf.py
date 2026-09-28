import os
import sys
import base64
import subprocess
import shutil
import time

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_base64(file_path):
    if not os.path.exists(file_path):
        print(f"Warning: File not found: {file_path}")
        return ""
    ext = os.path.splitext(file_path)[1].lower()
    mime = "image/jpeg"
    if ext == ".png":
        mime = "image/png"
    elif ext in [".otf", ".ttf"]:
        mime = "font/opentype" if ext == ".otf" else "font/truetype"
    elif ext == ".svg":
        mime = "image/svg+xml"
    with open(file_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{data}"

def get_font_base64(file_path):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

# Load Assets
logo_gold_b64 = get_base64(os.path.join(BASE_DIR, "public", "knowledge_logo_gold.png"))
brain_watermark_b64 = get_base64(os.path.join(BASE_DIR, "public", "knowledge_brain_watermark.png"))

# Load Slide Images
img_slide1_b64 = get_base64(os.path.join(BASE_DIR, "images", "erbil_cover_desk_1790243136096.jpg"))
img_slide2_b64 = get_base64(os.path.join(BASE_DIR, "images", "erbil_mutual_contract_1790243165923.jpg"))
img_slide3_b64 = get_base64(os.path.join(BASE_DIR, "images", "erbil_resignation_desk_1790243200256.jpg"))
img_slide4_b64 = get_base64(os.path.join(BASE_DIR, "images", "erbil_employer_termination_1790243235199.jpg"))
img_slide5_b64 = get_base64(os.path.join(BASE_DIR, "images", "erbil_disciplinary_gavel_1790243270695.jpg"))

# Load Qomra font if exists
qomra_bold_b64 = get_font_base64(os.path.join(BASE_DIR, "public", "fonts", "QOMRAARABICITF-BOLD.OTF"))
qomra_reg_b64 = get_font_base64(os.path.join(BASE_DIR, "public", "fonts", "QOMRAARABICITF-REGULAR.OTF"))

font_faces = ""
if qomra_bold_b64:
    font_faces += f"""
@font-face {{
    font-family: 'QomraCustom';
    src: url(data:font/opentype;base64,{qomra_bold_b64}) format('opentype');
    font-weight: 700;
    font-style: normal;
}}
"""
if qomra_reg_b64:
    font_faces += f"""
@font-face {{
    font-family: 'QomraCustom';
    src: url(data:font/opentype;base64,{qomra_reg_b64}) format('opentype');
    font-weight: 400;
    font-style: normal;
}}
"""

def generate_arabic_html():
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>كتاب قانون الأعمال - سلايدات الجوال المتكاملة (PDF)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@300;400;500;600;700;800;900&family=Amiri:wght@400;700&family=Cairo:wght@400;600;700;800;900&family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<style>
{font_faces}

@page {{
    size: 1080px 1920px;
    margin: 0;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}}

:root {{
    --bg-dark: #070a10;
    --card-bg: rgba(15, 23, 42, 0.94);
    --gold-primary: #d4af37;
    --gold-bright: #fce8a6;
    --gold-gradient: linear-gradient(135deg, #fffdf0 0%, #fce8a6 30%, #d4af37 70%, #aa8216 100%);
    --font-heading: 'QomraCustom', 'Alexandria', 'Cairo', 'Tajawal', sans-serif;
    --font-body: 'QomraCustom', 'Tajawal', 'Alexandria', 'Cairo', sans-serif;
}}

body {{
    width: 1080px;
    margin: 0 auto;
    background-color: #030508;
    font-family: var(--font-body);
    color: #ffffff;
    direction: rtl;
}}

@media screen {{
    body {{
        padding: 30px 0 80px 0;
        background: #06090e;
    }}
    .browser-only-bar {{
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        background: rgba(15, 23, 42, 0.92);
        backdrop-filter: blur(16px);
        border: 1.5px solid var(--gold-primary);
        box-shadow: 0 10px 35px rgba(0,0,0,0.8), 0 0 25px rgba(212, 175, 55, 0.35);
        border-radius: 999px;
        padding: 12px 28px;
        display: flex;
        align-items: center;
        gap: 18px;
    }}
    .btn-action-web {{
        background: var(--gold-gradient);
        color: #070a10;
        font-weight: 800;
        font-size: 17px;
        border: none;
        padding: 10px 22px;
        border-radius: 999px;
        cursor: pointer;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }}
    .btn-action-secondary {{
        background: rgba(255, 255, 255, 0.1);
        color: #fff;
        border: 1px solid rgba(212, 175, 55, 0.5);
        font-weight: 700;
        font-size: 16px;
        padding: 9px 20px;
        border-radius: 999px;
        cursor: pointer;
        text-decoration: none;
    }}
    .slide-page {{
        margin-bottom: 40px;
        border-radius: 28px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.8);
    }}
}}

@media print {{
    .browser-only-bar {{
        display: none !important;
    }}
}}

.slide-page {{
    width: 1080px;
    height: 1920px;
    position: relative;
    page-break-after: always;
    page-break-inside: avoid;
    overflow: hidden;
    background: radial-gradient(circle at 50% 12%, #142036 0%, #0a0f1a 50%, #04060a 100%);
    padding: 50px 60px 42px 60px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-sizing: border-box;
}}

.corner-ornament {{
    position: absolute;
    width: 50px;
    height: 50px;
    pointer-events: none;
    z-index: 10;
}}
.corner-ornament.top-right {{ top: 22px; right: 22px; }}
.corner-ornament.top-left {{ top: 22px; left: 22px; transform: scaleX(-1); }}
.corner-ornament.bottom-right {{ bottom: 22px; right: 22px; transform: scaleY(-1); }}
.corner-ornament.bottom-left {{ bottom: 22px; left: 22px; transform: scale(-1); }}

.page-border-frame {{
    position: absolute;
    top: 22px;
    left: 22px;
    right: 22px;
    bottom: 22px;
    border: 1.5px solid rgba(212, 175, 55, 0.45);
    border-radius: 20px;
    pointer-events: none;
    z-index: 5;
    box-shadow: inset 0 0 40px rgba(0,0,0,0.6);
}}

.top-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 15px 16px 15px;
    border-bottom: 1.5px solid rgba(212, 175, 55, 0.35);
    position: relative;
    z-index: 15;
}}

.univ-brand {{
    display: flex;
    align-items: center;
    gap: 16px;
}}

.univ-logo {{
    width: 56px;
    height: 56px;
    object-fit: contain;
    filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.45));
}}

.univ-title-text {{
    display: flex;
    flex-direction: column;
}}

.univ-name {{
    font-size: 24px;
    font-weight: 800;
    color: var(--gold-bright);
    letter-spacing: -0.3px;
}}

.dept-name {{
    font-size: 18px;
    font-weight: 600;
    color: #94a3b8;
}}

.header-badges {{
    display: flex;
    align-items: center;
    gap: 14px;
}}

.badge-course {{
    background: rgba(212, 175, 55, 0.15);
    border: 1.5px solid rgba(212, 175, 55, 0.6);
    color: var(--gold-bright);
    padding: 7px 18px;
    border-radius: 999px;
    font-size: 19px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.badge-counter {{
    background: rgba(255, 255, 255, 0.08);
    border: 1.5px solid rgba(212, 175, 55, 0.5);
    color: #ffd700;
    padding: 7px 18px;
    border-radius: 12px;
    font-size: 21px;
    font-weight: 800;
    font-family: monospace;
    direction: ltr !important;
    unicode-bidi: bidi-override !important;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 95px;
}}

.slide-intro-block {{
    margin-top: 14px;
    margin-bottom: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    position: relative;
    z-index: 15;
    padding: 0 10px;
}}

.section-pill {{
    align-self: flex-start;
    padding: 5px 18px;
    border-radius: 30px;
    font-size: 21px;
    font-weight: 800;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border-width: 1.5px;
    border-style: solid;
}}

.slide-main-title {{
    font-size: 38px;
    font-weight: 900;
    line-height: 1.32;
    background: var(--gold-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 4px 18px rgba(0, 0, 0, 0.9);
    letter-spacing: -0.5px;
    font-family: var(--font-heading);
}}

.slide-subtitle-text {{
    font-size: 21px;
    font-weight: 600;
    color: #cbd5e1;
    line-height: 1.42;
}}

.slide-media-container {{
    width: 100%;
    height: 400px;
    border-radius: 20px;
    overflow: hidden;
    position: relative;
    border: 2px solid rgba(212, 175, 55, 0.55);
    box-shadow: 0 16px 36px rgba(0,0,0,0.65), 0 0 25px rgba(212, 175, 55, 0.2);
    margin-bottom: 14px;
    z-index: 15;
}}

.slide-media-container img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}}

.media-caption-badge {{
    position: absolute;
    bottom: 14px;
    right: 16px;
    background: rgba(7, 10, 16, 0.88);
    backdrop-filter: blur(10px);
    border: 1.5px solid rgba(212, 175, 55, 0.6);
    border-radius: 12px;
    padding: 8px 18px;
    color: #fff;
    font-size: 20px;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.8);
}}

.points-list-wrapper {{
    display: flex;
    flex-direction: column;
    gap: 11px;
    margin-bottom: 12px;
    z-index: 15;
    padding: 0 6px;
}}

.point-mobile-card {{
    background: linear-gradient(135deg, rgba(22, 33, 54, 0.88) 0%, rgba(11, 17, 28, 0.95) 100%);
    border: 1.5px solid rgba(212, 175, 55, 0.32);
    border-radius: 16px;
    padding: 13px 18px;
    display: flex;
    align-items: center;
    gap: 18px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.45);
}}

.point-star-num {{
    width: 46px;
    height: 46px;
    min-width: 46px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.point-star-num svg {{
    position: absolute;
    width: 100%;
    height: 100%;
}}

.point-digit {{
    position: relative;
    z-index: 2;
    font-size: 20px;
    font-weight: 900;
    color: #ffffff;
    font-family: var(--font-heading);
}}

.point-content-text {{
    font-size: 22.5px;
    line-height: 1.45;
    color: #f1f5f9;
}}

.point-prefix-strong {{
    color: #ffd700;
    font-weight: 900;
    font-size: 23.5px;
    margin-left: 6px;
}}

.slide-bottom-bar {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 15;
    padding: 10px 25px 0 25px;
    margin-bottom: 10px;
    border-top: 1.5px solid rgba(212, 175, 55, 0.3);
}}

.legal-reference-pill {{
    background: linear-gradient(90deg, rgba(212, 175, 55, 0.18) 0%, rgba(212, 175, 55, 0.05) 100%);
    border: 1.5px solid rgba(212, 175, 55, 0.45);
    border-radius: 12px;
    padding: 8px 18px;
    font-size: 20px;
    font-weight: 700;
    color: #fce8a6;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.academic-subfooter {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 18.5px;
    color: #94a3b8;
    font-weight: 600;
}}

.academic-subfooter .supervisor-sub {{
    color: #e2e8f0;
}}
.academic-subfooter .supervisor-sub strong {{
    color: var(--gold-bright);
}}

/* Front Cover */
.front-cover-page {{
    background: radial-gradient(circle at 50% 25%, #182844 0%, #0d1524 45%, #05080e 100%);
    justify-content: space-between;
    text-align: center;
    padding: 60px 65px 44px 65px;
}}

.cover-header-univ {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
}}

.cover-logo-large {{
    width: 95px;
    height: 95px;
    object-fit: contain;
    filter: drop-shadow(0 0 25px rgba(212, 175, 55, 0.6));
}}

.cover-univ-title {{
    font-size: 32px;
    font-weight: 900;
    color: var(--gold-bright);
    letter-spacing: -0.5px;
}}

.cover-dept-subtitle {{
    font-size: 22px;
    font-weight: 600;
    color: #cbd5e1;
}}

.cover-center-monument {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 18px;
    margin: auto 0;
}}

.cover-shamseh-seal {{
    width: 110px;
    height: 110px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    filter: drop-shadow(0 0 20px rgba(212, 175, 55, 0.65));
}}

.cover-title-big {{
    font-family: var(--font-heading);
    font-size: 62px;
    font-weight: 900;
    line-height: 1.25;
    background: var(--gold-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 6px 20px rgba(0,0,0,0.9));
}}

.cover-subtitle-big {{
    font-family: var(--font-heading);
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.3;
    text-shadow: 0 4px 15px rgba(0,0,0,0.9), 0 0 30px rgba(212, 175, 55, 0.5);
}}

.cover-flourish {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    width: 80%;
    margin: 10px 0;
}}
.cover-flourish-line {{
    flex: 1;
    height: 2px;
    background: linear-gradient(90deg, transparent, #d4af37, transparent);
}}

.cover-topic-pill {{
    background: rgba(212, 175, 55, 0.16);
    border: 2px solid rgba(212, 175, 55, 0.65);
    border-radius: 999px;
    padding: 10px 30px;
    font-size: 26px;
    font-weight: 800;
    color: var(--gold-bright);
    box-shadow: 0 0 30px rgba(212, 175, 55, 0.25);
}}

.cover-cards-grid {{
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 0 25px;
    margin-bottom: 12px;
}}

.cover-info-card {{
    background: rgba(18, 28, 46, 0.85);
    border: 1.5px solid rgba(212, 175, 55, 0.4);
    border-radius: 16px;
    padding: 15px 22px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    text-align: right;
}}

.cover-info-card .card-role {{
    font-size: 20px;
    color: #fce8a6;
    font-weight: 700;
}}

.cover-info-card .card-val {{
    font-size: 23px;
    color: #ffffff;
    font-weight: 800;
}}

.back-cover-page {{
    background: radial-gradient(circle at 50% 30%, #16243d 0%, #0c1422 50%, #05080e 100%);
    justify-content: space-between;
    text-align: center;
    padding: 60px 65px 44px 65px;
}}

.back-conclusion-list {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    width: 100%;
    margin: 18px 0;
}}

.back-conclusion-card {{
    background: rgba(16, 26, 44, 0.9);
    border: 1.5px solid rgba(212, 175, 55, 0.35);
    border-radius: 16px;
    padding: 15px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    text-align: right;
}}

.check-icon {{
    font-size: 26px;
    color: #10b981;
    font-weight: 900;
    min-width: 34px;
}}

.conclusion-text {{
    font-size: 22.5px;
    color: #f1f5f9;
    line-height: 1.45;
    font-weight: 600;
}}

</style>
</head>
<body>

<!-- Browser floating quick toolbar -->
<div class="browser-only-bar">
    <a href="عرض_سلايدات_قانون_الاعمال_مخصص_للجوال.pdf" download class="btn-action-web">
        <span>📥 تحميل ملف PDF المخصص للجوال (10.8 MB)</span>
    </a>
    <button onclick="window.print()" class="btn-action-secondary">
        <span>🖨️ طباعة السلايدات</span>
    </button>
    <a href="slides_presentation_mobile_ku.html" class="btn-action-secondary">
        <span>🌐 گۆڕین بۆ زمانی کوردی</span>
    </a>
</div>

<svg style="display: none;">
  <defs>
    <g id="cornerArabesque">
      <path d="M4,4 L46,4 Q46,15 36,24 Q27,33 15,46 Q4,46 4,46 Z" fill="rgba(212,175,55,0.12)" stroke="#d4af37" stroke-width="1.8"/>
      <path d="M8,8 L40,8 Q40,17 32,24 Q24,31 16,40 Q8,40 8,40 Z" fill="none" stroke="#d4af37" stroke-width="1.1" stroke-dasharray="2 2" opacity="0.85"/>
      <circle cx="18" cy="18" r="7" fill="rgba(212,175,55,0.25)" stroke="#d4af37" stroke-width="1.3"/>
      <circle cx="18" cy="18" r="2.5" fill="#ffffff"/>
    </g>
    <g id="star8">
      <rect x="6" y="6" width="20" height="20" fill="rgba(212, 175, 55, 0.3)" stroke="#d4af37" stroke-width="1.6" />
      <rect x="6" y="6" width="20" height="20" transform="rotate(45 16 16)" fill="rgba(212, 175, 55, 0.3)" stroke="#d4af37" stroke-width="1.6" />
    </g>
  </defs>
</svg>

<!-- ======================================================== -->
<!-- 1. FRONT COVER (الغلاف الملكي الأول)                     -->
<!-- ======================================================== -->
<div class="slide-page front-cover-page">
    <div class="page-border-frame"></div>
    <svg class="corner-ornament top-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament top-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>

    <!-- Top Branding -->
    <div class="cover-header-univ">
        <img src="{logo_gold_b64}" alt="جامعة نولج" class="cover-logo-large">
        <div class="cover-univ-title">جامعة نولج — Knowledge University</div>
        <div class="cover-dept-subtitle">كلية القانون وإدارة الأعمال | قسم التسويق الرقمي (Digital Marketing)</div>
    </div>

    <!-- Center Monument -->
    <div class="cover-center-monument">
        <div class="cover-shamseh-seal">
            <svg viewBox="0 0 100 100" width="100" height="100">
                <circle cx="50" cy="50" r="46" fill="rgba(212,175,55,0.15)" stroke="#d4af37" stroke-width="2.5"/>
                <circle cx="50" cy="50" r="38" fill="rgba(212,175,55,0.25)" stroke="#fce8a6" stroke-width="1.5" stroke-dasharray="4 2"/>
                <text x="50" y="58" font-size="34" text-anchor="middle" fill="#ffd700">⚖️</text>
            </svg>
        </div>

        <h1 class="cover-title-big">إنهاء عقد العمل</h1>
        <h2 class="cover-subtitle-big">بإرادة أحد طرفيه أو كليهما</h2>

        <div class="cover-flourish">
            <span class="cover-flourish-line"></span>
            <span style="color: #ffd700; font-size: 26px;">❖ ✤ ❖</span>
            <span class="cover-flourish-line"></span>
        </div>

        <div class="cover-topic-pill">
            مقرر قانون الأعمال (Business Law)
        </div>
        <div style="font-size: 23px; color: #cbd5e1; font-weight: 600;">
            الفصل الخامس — المبحث الثاني (ص 324 - 366)
        </div>
    </div>

    <!-- Academic Metadata Cards -->
    <div class="cover-cards-grid">
        <div class="cover-info-card">
            <span class="card-role">إشراف وتدريس:</span>
            <span class="card-val">الأستاذة م.م. هالة رحمن (Ass.L. Hala Rahman)</span>
        </div>
        <div class="cover-info-card">
            <span class="card-role">المرجع الأكاديمي:</span>
            <span class="card-val">د. عدنان العابد ود. يوسف إلياس (جامعة بغداد)</span>
        </div>
        <div class="cover-info-card">
            <span class="card-role">المدينة والعام:</span>
            <span class="card-val">أربيل — كوردستان العراق | العام الأكاديمي 2026</span>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- 2. SLIDE 1 (01 / 05) - المدخل والعرض الأكاديمي             -->
<!-- ======================================================== -->
<div class="slide-page">
    <div class="page-border-frame"></div>
    <svg class="corner-ornament top-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament top-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>

    <div>
        <div class="top-header">
            <div class="univ-brand">
                <img src="{logo_gold_b64}" alt="جامعة نولج" class="univ-logo">
                <div class="univ-title-text">
                    <span class="univ-name">جامعة نولج — Knowledge University</span>
                    <span class="dept-name">قسم التسويق الرقمي | Business Law</span>
                </div>
            </div>
            <div class="header-badges">
                <span class="badge-counter">01 / 04</span>
            </div>
        </div>

        <div class="slide-intro-block">
            <span class="section-pill" style="border-color: #c59b27; color: #ffd700; background: rgba(197, 155, 39, 0.15);">
                غلاف العرض التقديمي الأكاديمي
            </span>
            <h1 class="slide-main-title">إنهاء عقد العمل بإرادة أحد طرفيه أو كليهما</h1>
            <p class="slide-subtitle-text">مقرر قانون الأعمال (Business Law) — بإشراف: م.م. هالة رحمن (Ass.L. Hala Rahman)</p>
        </div>

        <div class="slide-media-container" style="height: 440px;">
            <img src="{img_slide1_b64}" alt="قلعة أربيل ومكتب المحاماة">
            <div class="media-caption-badge">
                <span>⚖️ عقد عمل موثق — إطلالة قلعة أربيل</span>
            </div>
        </div>

        <div class="points-list-wrapper">
            <div class="point-mobile-card" style="padding: 22px 24px;">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">1</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">الموضوع الدراسي:</strong>
                    المبحث الثاني من الفصل الخامس في قانون العمل العراقي.
                </div>
            </div>
            <div class="point-mobile-card" style="padding: 22px 24px;">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">2</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">المرجع المعتمد:</strong>
                    مؤلف الدكتور عدنان العابد والدكتور يوسف إلياس.
                </div>
            </div>
            <div class="point-mobile-card" style="padding: 22px 24px;">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">3</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">التأصيل القانوني:</strong>
                    انحلال الرابطة العقدية بالرضا المشترك أو بالإرادة المنفردة.
                </div>
            </div>
        </div>
    </div>

    <div class="slide-bottom-bar">
        <div class="legal-reference-pill">
            <span>📖</span>
            <span>كتاب قانون العمل (ص 324 - 366) | كلية القانون - جامعة بغداد</span>
        </div>
        <div class="academic-subfooter">
            <span class="supervisor-sub">إشراف: <strong>م.م. هالة رحمن</strong></span>
            <span>الصفحة 2 من 6 (عرض الجوال الكامل)</span>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- 3. SLIDE 2 (02 / 05) - التقايل الرضائي                     -->
<!-- ======================================================== -->
<div class="slide-page">
    <div class="page-border-frame"></div>
    <svg class="corner-ornament top-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament top-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>

    <div>
        <div class="top-header">
            <div class="univ-brand">
                <img src="{logo_gold_b64}" alt="جامعة نولج" class="univ-logo">
                <div class="univ-title-text">
                    <span class="univ-name">جامعة نولج — Knowledge University</span>
                    <span class="dept-name">قسم التسويق الرقمي | Business Law</span>
                </div>
            </div>
            <div class="header-badges">
                <span class="badge-counter">02 / 04</span>
            </div>
        </div>

        <div class="slide-intro-block">
            <span class="section-pill" style="border-color: #10b981; color: #6ee7b7; background: rgba(16, 185, 129, 0.15);">
                المبحث الثاني - أولاً
            </span>
            <h1 class="slide-main-title">انتهاء العقد باتفاق إرادتي طرفيه (التقايل الرضائي)</h1>
            <p class="slide-subtitle-text">انحلال الرابطة العقدية بالتراضي المشترك وسلطان الإرادة (ص 324)</p>
        </div>

        <div class="slide-media-container">
            <img src="{img_slide2_b64}" alt="التسوية الرضائية وإطلالة فندق ديفان أربيل">
            <div class="media-caption-badge">
                <span>⚖️ تسوية رضائية موثقة — شارع كولان أربيل</span>
            </div>
        </div>

        <div class="points-list-wrapper">
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">1</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">مبدأ التقايل:</strong>
                    تطبيق قاعدة «العقد شريعة المتعاقدين» في إنهائه رضائياً.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">2</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">سلامة الرضا:</strong>
                    خلو إرادة العامل من أي إكراه مادي أو معنوي صادر عن الإدارة.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">3</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">بطلان التنازل:</strong>
                    بطلان إسقاط الحقوق الآمرة كمكافأة نهاية الخدمة والإجازات.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">4</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">التوثيق الخطي:</strong>
                    اشتراط عقد مخالصة كتابي رسمي موقع ومختوم قانوناً.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">5</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">شهادة الخبرة:</strong>
                    التزام صاحب العمل بتسليم العامل براءة ذمة وشهادة خدمة مجانية.
                </div>
            </div>
        </div>
    </div>

    <div class="slide-bottom-bar">
        <div class="legal-reference-pill">
            <span>📖</span>
            <span>المادة (324 وما بعدها) | التقايل الرضائي وحماية الطرف الأضعف</span>
        </div>
        <div class="academic-subfooter">
            <span class="supervisor-sub">إشراف: <strong>م.م. هالة رحمن</strong></span>
            <span>الصفحة 3 من 6 (عرض الجوال الكامل)</span>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- 4. SLIDE 3 (03 / 05) - استقالة العامل والترك المشروع        -->
<!-- ======================================================== -->
<div class="slide-page">
    <div class="page-border-frame"></div>
    <svg class="corner-ornament top-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament top-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>

    <div>
        <div class="top-header">
            <div class="univ-brand">
                <img src="{logo_gold_b64}" alt="جامعة نولج" class="univ-logo">
                <div class="univ-title-text">
                    <span class="univ-name">جامعة نولج — Knowledge University</span>
                    <span class="dept-name">قسم التسويق الرقمي | Business Law</span>
                </div>
            </div>
            <div class="header-badges">
                <span class="badge-counter">03 / 04</span>
            </div>
        </div>

        <div class="slide-intro-block">
            <span class="section-pill" style="border-color: #3b82f6; color: #93c5fd; background: rgba(59, 130, 246, 0.15);">
                المبحث الثاني - ثانياً
            </span>
            <h1 class="slide-main-title">إنهاء العقد بالإرادة المنفردة للعامل (الاستقالة والترك)</h1>
            <p class="slide-subtitle-text">ممارسة العامل لحريته الدستورية في العمل وضوابط الإخطار (ص 328)</p>
        </div>

        <div class="slide-media-container">
            <img src="{img_slide3_b64}" alt="إشعار استقالة رسمي في مكتب أربيل">
            <div class="media-caption-badge">
                <span>⚖️ إشعار استقالة رسمي — أربيل</span>
            </div>
        </div>

        <div class="points-list-wrapper">
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">1</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">حرية العمل:</strong>
                    حظر السخرة وإقرار حق العامل في الاستقالة بإرادته المنفردة.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">2</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">مهلة الإخطار:</strong>
                    توجيه إنذار كتابي رسمي قبل 30 يوماً لضمان انتظام العمل.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">3</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">الاستمرار بالعمل:</strong>
                    التزام العامل بأداء واجباته وتقاضي أجره خلال مهلة الإنذار.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">4</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">الترك الفوري المبرر:</strong>
                    جواز المغادرة الفورية عند اعتداء صاحب العمل أو خفض الأجر.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">5</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">السلامة المهنية:</strong>
                    حق العامل بإنهاء العقد فوراً عند ثبوت خطر داهم يهدد صحته.
                </div>
            </div>
        </div>
    </div>

    <div class="slide-bottom-bar">
        <div class="legal-reference-pill">
            <span>📖</span>
            <span>المادة (328 وما بعدها) | الاستقالة والحالات الاستثنائية للترك المشروع</span>
        </div>
        <div class="academic-subfooter">
            <span class="supervisor-sub">إشراف: <strong>م.م. هالة رحمن</strong></span>
            <span>الصفحة 4 من 6 (عرض الجوال الكامل)</span>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- 5. SLIDE 4 (04 / 05) - إنهاء صاحب العمل والفصل التعسفي     -->
<!-- ======================================================== -->
<div class="slide-page">
    <div class="page-border-frame"></div>
    <svg class="corner-ornament top-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament top-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>

    <div>
        <div class="top-header">
            <div class="univ-brand">
                <img src="{logo_gold_b64}" alt="جامعة نولج" class="univ-logo">
                <div class="univ-title-text">
                    <span class="univ-name">جامعة نولج — Knowledge University</span>
                    <span class="dept-name">قسم التسويق الرقمي | Business Law</span>
                </div>
            </div>
            <div class="header-badges">
                <span class="badge-counter">04 / 04</span>
            </div>
        </div>

        <div class="slide-intro-block">
            <span class="section-pill" style="border-color: #f59e0b; color: #fde68a; background: rgba(245, 158, 11, 0.15);">
                المبحث الثاني - ثالثاً
            </span>
            <h1 class="slide-main-title">إنهاء العقد بإرادة صاحب العمل</h1>
            <p class="slide-subtitle-text">قيود سلطة الإدارة في الإنهاء وضمانات الحماية من الفصل الجائر (ص 334)</p>
        </div>

        <div class="slide-media-container">
            <img src="{img_slide4_b64}" alt="إنهاء العقد وضمانات الرقابة القضائية">
            <div class="media-caption-badge">
                <span>⚖️ رقابة القضاء العمالي — أربيل</span>
            </div>
        </div>

        <div class="points-list-wrapper">
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">1</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">تقييد سلطة الإنهاء:</strong>
                    حظر إنهاء العقد غير محدد المدة دون سبب مشروع وجدي.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">2</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">الأسباب المقبولة:</strong>
                    إعادة الهيكلة الاقتصادية، عدم الكفاءة المثبتة، وبلوغ التقاعد.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">3</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">معيار التعسف:</strong>
                    بطلان الفصل المرتبط بنشاط نقابي، شكوى قانونية، أو تمييز.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">4</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">إعادة العامل:</strong>
                    اختصاص محكمة العمل بالحكم بإعادة المفصول وصرف كامل أجوره.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">5</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">التعويض الجابر:</strong>
                    استحقاق تعويض مالي عادل وبدل مهلة الإخطار ومكافأة الخدمة.
                </div>
            </div>
        </div>
    </div>

    <div class="slide-bottom-bar">
        <div class="legal-reference-pill">
            <span>📖</span>
            <span>المادة (334 وما بعدها) | الحظر الصارم للإنهاء التعسفي</span>
        </div>
        <div class="academic-subfooter">
            <span class="supervisor-sub">إشراف: <strong>م.م. هالة رحمن</strong></span>
            <span>الصفحة 5 من 6 (عرض الجوال الكامل)</span>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- 7. BACK COVER (الغلاف الملكي الختامي)                     -->
<!-- ======================================================== -->
<div class="slide-page back-cover-page">
    <div class="page-border-frame"></div>
    <svg class="corner-ornament top-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament top-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>

    <!-- Top Header -->
    <div class="cover-header-univ">
        <img src="{logo_gold_b64}" alt="جامعة نولج" class="cover-logo-large">
        <div class="cover-univ-title">جامعة نولج — Knowledge University</div>
        <div class="cover-dept-subtitle">كلية القانون وإدارة الأعمال | قسم التسويق الرقمي</div>
    </div>

    <!-- Center Monument -->
    <div class="cover-center-monument">
        <div class="cover-shamseh-seal">
            <svg viewBox="0 0 100 100" width="100" height="100">
                <circle cx="50" cy="50" r="46" fill="rgba(212,175,55,0.15)" stroke="#d4af37" stroke-width="2.5"/>
                <circle cx="50" cy="50" r="38" fill="rgba(212,175,55,0.25)" stroke="#fce8a6" stroke-width="1.5" stroke-dasharray="4 2"/>
                <text x="50" y="58" font-size="34" text-anchor="middle" fill="#ffd700">🛡️</text>
            </svg>
        </div>

        <h1 class="cover-title-big">تم بحمد الله وتوفيقه</h1>
        <h2 class="cover-subtitle-big" style="font-size: 34px; color: #fce8a6;">
            خاتمة دراسة إنهاء عقد العمل في قانون الأعمال
        </h2>

        <div class="cover-flourish">
            <span class="cover-flourish-line"></span>
            <span style="color: #ffd700; font-size: 26px;">❖ ✤ ❖</span>
            <span class="cover-flourish-line"></span>
        </div>

        <!-- Key Accomplishments -->
        <div class="back-conclusion-list">
            <div class="back-conclusion-card">
                <span class="check-icon">✓</span>
                <span class="conclusion-text">استيفاء كافة أحكام وضوابط المبحث الثاني من الفصل الخامس في قانون العمل العراقي.</span>
            </div>
            <div class="back-conclusion-card">
                <span class="check-icon">✓</span>
                <span class="conclusion-text">تأصيل قانوني دقيق لموازنة حقوق واستقرار العامل مع صون مصالح رب العمل والإنتاج.</span>
            </div>
            <div class="back-conclusion-card">
                <span class="check-icon">✓</span>
                <span class="conclusion-text">تحديد المعايير القضائية لمنع الفصل التعسفي وضمان رقابة محكمة العمل الفعالة.</span>
            </div>
            <div class="back-conclusion-card">
                <span class="check-icon">✓</span>
                <span class="conclusion-text">ربط المادة النظرية بالتطبيقات العملية في بيئة الأعمال والشركات في أربيل وبغداد.</span>
            </div>
        </div>
    </div>

    <!-- Supervisor & Institutional Footer -->
    <div class="cover-cards-grid">
        <div class="cover-info-card" style="justify-content: center; text-align: center; gap: 15px;">
            <span class="card-role">إشراف وتوجيه:</span>
            <span class="card-val" style="color: #ffd700;">الأستاذة م.م. هالة رحمن (Ass.L. Hala Rahman)</span>
        </div>
        <div style="font-size: 19px; color: #94a3b8; font-weight: 600; text-align: center;">
            جميع الحقوق محفوظة © 2026 — جامعة نولج | مقرر قانون الأعمال (Business Law)
        </div>
    </div>
</div>

</body>
</html>
"""

def generate_kurdish_html():
    return f"""<!DOCTYPE html>
<html lang="ku" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>کۆتاییهێنان بە گرێبەستی کار - سلايدەکانی مۆبایل</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;500;600;700;800;900&family=Vazirmatn:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
@page {{
    size: 1080px 1920px;
    margin: 0;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}}

:root {{
    --bg-dark: #070a10;
    --gold-primary: #d4af37;
    --gold-bright: #fce8a6;
    --gold-gradient: linear-gradient(135deg, #fffdf0 0%, #fce8a6 30%, #d4af37 70%, #aa8216 100%);
    --font-heading: 'Noto Sans Arabic', 'Vazirmatn', sans-serif;
    --font-body: 'Noto Sans Arabic', 'Vazirmatn', sans-serif;
}}

body {{
    width: 1080px;
    margin: 0 auto;
    background-color: #030508;
    font-family: var(--font-body);
    color: #ffffff;
    direction: rtl;
}}

@media screen {{
    body {{
        padding: 30px 0 80px 0;
        background: #06090e;
    }}
    .browser-only-bar {{
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        background: rgba(15, 23, 42, 0.92);
        backdrop-filter: blur(16px);
        border: 1.5px solid var(--gold-primary);
        box-shadow: 0 10px 35px rgba(0,0,0,0.8), 0 0 25px rgba(212, 175, 55, 0.35);
        border-radius: 999px;
        padding: 12px 28px;
        display: flex;
        align-items: center;
        gap: 18px;
    }}
    .btn-action-web {{
        background: var(--gold-gradient);
        color: #070a10;
        font-weight: 800;
        font-size: 17px;
        border: none;
        padding: 10px 22px;
        border-radius: 999px;
        cursor: pointer;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }}
    .btn-action-secondary {{
        background: rgba(255, 255, 255, 0.1);
        color: #fff;
        border: 1px solid rgba(212, 175, 55, 0.5);
        font-weight: 700;
        font-size: 16px;
        padding: 9px 20px;
        border-radius: 999px;
        cursor: pointer;
        text-decoration: none;
    }}
    .slide-page {{
        margin-bottom: 40px;
        border-radius: 28px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.8);
    }}
}}

@media print {{
    .browser-only-bar {{
        display: none !important;
    }}
}}

.slide-page {{
    width: 1080px;
    height: 1920px;
    position: relative;
    page-break-after: always;
    page-break-inside: avoid;
    overflow: hidden;
    background: radial-gradient(circle at 50% 12%, #142036 0%, #0a0f1a 50%, #04060a 100%);
    padding: 50px 60px 42px 60px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-sizing: border-box;
}}

.corner-ornament {{
    position: absolute;
    width: 50px;
    height: 50px;
    pointer-events: none;
    z-index: 10;
}}
.corner-ornament.top-right {{ top: 22px; right: 22px; }}
.corner-ornament.top-left {{ top: 22px; left: 22px; transform: scaleX(-1); }}
.corner-ornament.bottom-right {{ bottom: 22px; right: 22px; transform: scaleY(-1); }}
.corner-ornament.bottom-left {{ bottom: 22px; left: 22px; transform: scale(-1); }}

.page-border-frame {{
    position: absolute;
    top: 22px;
    left: 22px;
    right: 22px;
    bottom: 22px;
    border: 1.5px solid rgba(212, 175, 55, 0.45);
    border-radius: 20px;
    pointer-events: none;
    z-index: 5;
    box-shadow: inset 0 0 40px rgba(0,0,0,0.6);
}}

.top-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 15px 16px 15px;
    border-bottom: 1.5px solid rgba(212, 175, 55, 0.35);
    position: relative;
    z-index: 15;
}}

.univ-brand {{
    display: flex;
    align-items: center;
    gap: 16px;
}}

.univ-logo {{
    width: 56px;
    height: 56px;
    object-fit: contain;
    filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.45));
}}

.univ-title-text {{
    display: flex;
    flex-direction: column;
}}

.univ-name {{
    font-size: 24px;
    font-weight: 800;
    color: var(--gold-bright);
}}

.dept-name {{
    font-size: 18px;
    font-weight: 600;
    color: #94a3b8;
}}

.header-badges {{
    display: flex;
    align-items: center;
    gap: 14px;
}}

.badge-course {{
    background: rgba(212, 175, 55, 0.15);
    border: 1.5px solid rgba(212, 175, 55, 0.6);
    color: var(--gold-bright);
    padding: 7px 18px;
    border-radius: 999px;
    font-size: 19px;
    font-weight: 700;
}}

.badge-counter {{
    background: rgba(255, 255, 255, 0.08);
    border: 1.5px solid rgba(212, 175, 55, 0.5);
    color: #ffd700;
    padding: 7px 18px;
    border-radius: 12px;
    font-size: 21px;
    font-weight: 800;
    font-family: monospace;
    direction: ltr !important;
    unicode-bidi: bidi-override !important;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 95px;
}}

.slide-intro-block {{
    margin-top: 14px;
    margin-bottom: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    position: relative;
    z-index: 15;
    padding: 0 10px;
}}

.section-pill {{
    align-self: flex-start;
    padding: 5px 18px;
    border-radius: 30px;
    font-size: 21px;
    font-weight: 800;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border-width: 1.5px;
    border-style: solid;
}}

.slide-main-title {{
    font-size: 36px;
    font-weight: 900;
    line-height: 1.35;
    background: var(--gold-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: var(--font-heading);
}}

.slide-subtitle-text {{
    font-size: 21px;
    font-weight: 600;
    color: #cbd5e1;
    line-height: 1.42;
}}

.slide-media-container {{
    width: 100%;
    height: 400px;
    border-radius: 20px;
    overflow: hidden;
    position: relative;
    border: 2px solid rgba(212, 175, 55, 0.55);
    box-shadow: 0 16px 36px rgba(0,0,0,0.65), 0 0 25px rgba(212, 175, 55, 0.2);
    margin-bottom: 14px;
    z-index: 15;
}}

.slide-media-container img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}}

.media-caption-badge {{
    position: absolute;
    bottom: 14px;
    right: 16px;
    background: rgba(7, 10, 16, 0.88);
    backdrop-filter: blur(10px);
    border: 1.5px solid rgba(212, 175, 55, 0.6);
    border-radius: 12px;
    padding: 8px 18px;
    color: #fff;
    font-size: 20px;
    font-weight: 800;
}}

.points-list-wrapper {{
    display: flex;
    flex-direction: column;
    gap: 11px;
    margin-bottom: 12px;
    z-index: 15;
    padding: 0 6px;
}}

.point-mobile-card {{
    background: linear-gradient(135deg, rgba(22, 33, 54, 0.88) 0%, rgba(11, 17, 28, 0.95) 100%);
    border: 1.5px solid rgba(212, 175, 55, 0.32);
    border-radius: 16px;
    padding: 13px 18px;
    display: flex;
    align-items: center;
    gap: 18px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.45);
}}

.point-star-num {{
    width: 46px;
    height: 46px;
    min-width: 46px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.point-star-num svg {{
    position: absolute;
    width: 100%;
    height: 100%;
}}

.point-digit {{
    position: relative;
    z-index: 2;
    font-size: 20px;
    font-weight: 900;
    color: #ffffff;
}}

.point-content-text {{
    font-size: 22px;
    line-height: 1.45;
    color: #f1f5f9;
}}

.point-prefix-strong {{
    color: #ffd700;
    font-weight: 900;
    font-size: 23px;
    margin-left: 6px;
}}

.slide-bottom-bar {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 15;
    padding: 10px 25px 0 25px;
    margin-bottom: 10px;
    border-top: 1.5px solid rgba(212, 175, 55, 0.3);
}}

.legal-reference-pill {{
    background: linear-gradient(90deg, rgba(212, 175, 55, 0.18) 0%, rgba(212, 175, 55, 0.05) 100%);
    border: 1.5px solid rgba(212, 175, 55, 0.45);
    border-radius: 12px;
    padding: 8px 18px;
    font-size: 20px;
    font-weight: 700;
    color: #fce8a6;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.academic-subfooter {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 18.5px;
    color: #94a3b8;
    font-weight: 600;
}}

.academic-subfooter .supervisor-sub strong {{
    color: var(--gold-bright);
}}

/* Front Cover */
.front-cover-page {{
    background: radial-gradient(circle at 50% 25%, #182844 0%, #0d1524 45%, #05080e 100%);
    justify-content: space-between;
    text-align: center;
    padding: 60px 65px 44px 65px;
}}

.cover-header-univ {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
}}

.cover-logo-large {{
    width: 95px;
    height: 95px;
    object-fit: contain;
    filter: drop-shadow(0 0 25px rgba(212, 175, 55, 0.6));
}}

.cover-univ-title {{
    font-size: 32px;
    font-weight: 900;
    color: var(--gold-bright);
}}

.cover-dept-subtitle {{
    font-size: 22px;
    font-weight: 600;
    color: #cbd5e1;
}}

.cover-center-monument {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 18px;
    margin: auto 0;
}}

.cover-shamseh-seal {{
    width: 110px;
    height: 110px;
    display: flex;
    align-items: center;
    justify-content: center;
    filter: drop-shadow(0 0 20px rgba(212, 175, 55, 0.65));
}}

.cover-title-big {{
    font-size: 58px;
    font-weight: 900;
    line-height: 1.3;
    background: var(--gold-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.cover-subtitle-big {{
    font-size: 38px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.35;
}}

.cover-flourish {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    width: 80%;
    margin: 10px 0;
}}
.cover-flourish-line {{
    flex: 1;
    height: 2px;
    background: linear-gradient(90deg, transparent, #d4af37, transparent);
}}

.cover-topic-pill {{
    background: rgba(212, 175, 55, 0.16);
    border: 2px solid rgba(212, 175, 55, 0.65);
    border-radius: 999px;
    padding: 10px 30px;
    font-size: 26px;
    font-weight: 800;
    color: var(--gold-bright);
}}

.cover-cards-grid {{
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 0 25px;
    margin-bottom: 12px;
}}

.cover-info-card {{
    background: rgba(18, 28, 46, 0.85);
    border: 1.5px solid rgba(212, 175, 55, 0.4);
    border-radius: 16px;
    padding: 15px 22px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    text-align: right;
}}

.cover-info-card .card-role {{
    font-size: 20px;
    color: #fce8a6;
    font-weight: 700;
}}

.cover-info-card .card-val {{
    font-size: 23px;
    color: #ffffff;
    font-weight: 800;
}}

.back-cover-page {{
    background: radial-gradient(circle at 50% 30%, #16243d 0%, #0c1422 50%, #05080e 100%);
    justify-content: space-between;
    text-align: center;
    padding: 60px 65px 44px 65px;
}}

.back-conclusion-list {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    width: 100%;
    margin: 18px 0;
}}

.back-conclusion-card {{
    background: rgba(16, 26, 44, 0.9);
    border: 1.5px solid rgba(212, 175, 55, 0.35);
    border-radius: 16px;
    padding: 15px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    text-align: right;
}}

.check-icon {{
    font-size: 26px;
    color: #10b981;
    font-weight: 900;
    min-width: 34px;
}}

.conclusion-text {{
    font-size: 22px;
    color: #f1f5f9;
    line-height: 1.45;
    font-weight: 600;
}}

</style>
</head>
<body>

<!-- Browser floating quick toolbar -->
<div class="browser-only-bar">
    <a href="پێشکەشکردنی_سلايده‌كانی_یاسای_کار_بۆ_مۆبایل.pdf" download class="btn-action-web">
        <span>📥 داگرتنی فایلی PDF ی تایبەت بە مۆبایل (11.4 MB)</span>
    </a>
    <button onclick="window.print()" class="btn-action-secondary">
        <span>🖨️ چاپکردنی سلايدەکان</span>
    </button>
    <a href="slides_presentation_mobile_ar.html" class="btn-action-secondary">
        <span>🌐 التبديل إلى اللغة العربية</span>
    </a>
</div>

<svg style="display: none;">
  <defs>
    <g id="cornerArabesque">
      <path d="M4,4 L46,4 Q46,15 36,24 Q27,33 15,46 Q4,46 4,46 Z" fill="rgba(212,175,55,0.12)" stroke="#d4af37" stroke-width="1.8"/>
      <path d="M8,8 L40,8 Q40,17 32,24 Q24,31 16,40 Q8,40 8,40 Z" fill="none" stroke="#d4af37" stroke-width="1.1" stroke-dasharray="2 2" opacity="0.85"/>
      <circle cx="18" cy="18" r="7" fill="rgba(212,175,55,0.25)" stroke="#d4af37" stroke-width="1.3"/>
      <circle cx="18" cy="18" r="2.5" fill="#ffffff"/>
    </g>
    <g id="star8">
      <rect x="6" y="6" width="20" height="20" fill="rgba(212, 175, 55, 0.3)" stroke="#d4af37" stroke-width="1.6" />
      <rect x="6" y="6" width="20" height="20" transform="rotate(45 16 16)" fill="rgba(212, 175, 55, 0.3)" stroke="#d4af37" stroke-width="1.6" />
    </g>
  </defs>
</svg>

<!-- 1. FRONT COVER (بەرگی یەکەم) -->
<div class="slide-page front-cover-page">
    <div class="page-border-frame"></div>
    <svg class="corner-ornament top-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament top-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>

    <div class="cover-header-univ">
        <img src="{logo_gold_b64}" alt="زانکۆی نۆلج" class="cover-logo-large">
        <div class="cover-univ-title">زانکۆی نۆلج — Knowledge University</div>
        <div class="cover-dept-subtitle">کۆلێژی یاسا و کارگێڕی | بەشی بازاڕگەریی دیجیتاڵی (Digital Marketing)</div>
    </div>

    <div class="cover-center-monument">
        <div class="cover-shamseh-seal">
            <svg viewBox="0 0 100 100" width="100" height="100">
                <circle cx="50" cy="50" r="46" fill="rgba(212,175,55,0.15)" stroke="#d4af37" stroke-width="2.5"/>
                <circle cx="50" cy="50" r="38" fill="rgba(212,175,55,0.25)" stroke="#fce8a6" stroke-width="1.5" stroke-dasharray="4 2"/>
                <text x="50" y="58" font-size="34" text-anchor="middle" fill="#ffd700">⚖️</text>
            </svg>
        </div>

        <h1 class="cover-title-big">کۆتاییهێنان بە گرێبەستی کار</h1>
        <h2 class="cover-subtitle-big">بە ویستی یەکێک لە لایەنەکان یان هەردووکیان</h2>

        <div class="cover-flourish">
            <span class="cover-flourish-line"></span>
            <span style="color: #ffd700; font-size: 26px;">❖ ✤ ❖</span>
            <span class="cover-flourish-line"></span>
        </div>

        <div class="cover-topic-pill">
            بابەتی یاسای کار (Business Law)
        </div>
        <div style="font-size: 23px; color: #cbd5e1; font-weight: 600;">
            بەشی پێنجەم — باسی دووەم (ل 324 - 366)
        </div>
    </div>

    <div class="cover-cards-grid">
        <div class="cover-info-card">
            <span class="card-role">سەرپەرشتیار:</span>
            <span class="card-val">م.ی. هالة رحمن (Ass.L. Hala Rahman)</span>
        </div>
        <div class="cover-info-card">
            <span class="card-role">سەرچاوەی باوەڕپێکراو:</span>
            <span class="card-val">د. عەدنان عابید و د. یوسف ئیلیاس (زانکۆی بەغدا)</span>
        </div>
        <div class="cover-info-card">
            <span class="card-role">شار و ساڵ:</span>
            <span class="card-val">هەولێر — هەرێمی کوردستان | ساڵی ئەکادیمی 2026</span>
        </div>
    </div>
</div>

<!-- 2. SLIDE 1 (01 / 04) -->
<div class="slide-page">
    <div class="page-border-frame"></div>
    <svg class="corner-ornament top-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament top-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>

    <div>
        <div class="top-header">
            <div class="univ-brand">
                <img src="{logo_gold_b64}" alt="زانکۆی نۆلج" class="univ-logo">
                <div class="univ-title-text">
                    <span class="univ-name">زانکۆی نۆلج — Knowledge University</span>
                    <span class="dept-name">بەشی بازاڕگەریی دیجیتاڵی | Business Law</span>
                </div>
            </div>
            <div class="header-badges">
                <span class="badge-counter">01 / 04</span>
            </div>
        </div>

        <div class="slide-intro-block">
            <span class="section-pill" style="border-color: #c59b27; color: #ffd700; background: rgba(197, 155, 39, 0.15);">
                بەرگی پێشکەشکردنی ئەکادیمی
            </span>
            <h1 class="slide-main-title">کۆتاییهێنان بە گرێبەستی کار بە ویستی یەکێک لە لایەنەکان یان هەردووکیان</h1>
            <p class="slide-subtitle-text">بابەتی یاسای کار (Business Law) — بە سەرپەرشتی: م.ی. هالة رحمن (Ass.L. Hala Rahman)</p>
        </div>

        <div class="slide-media-container" style="height: 440px;">
            <img src="{img_slide1_b64}" alt="قەڵای هەولێر">
            <div class="media-caption-badge">
                <span>⚖️ گرێبەستی کاری فەرمی — دیمەنی قەڵای هەولێر</span>
            </div>
        </div>

        <div class="points-list-wrapper">
            <div class="point-mobile-card" style="padding: 22px 24px;">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">1</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">بابەتی خوێندن:</strong>
                    باسی دووەم لە بەشی پێنجەمی یاسای کاری عێراقی.
                </div>
            </div>
            <div class="point-mobile-card" style="padding: 22px 24px;">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">2</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">سەرچاوەی پەسەندکراو:</strong>
                    پەڕتووکی دکتۆر عەدنان عابید و دکتۆر یوسف ئیلیاس.
                </div>
            </div>
            <div class="point-mobile-card" style="padding: 22px 24px;">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">3</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">بنەمای یاسایی:</strong>
                    هەڵوەشاندنەوەی پەیوەندیی گرێبەست بە ڕەزامەندیی هاوبەش یان بە ویستی تاکلایەنە.
                </div>
            </div>
        </div>
    </div>

    <div class="slide-bottom-bar">
        <div class="legal-reference-pill">
            <span>📖</span>
            <span>پەڕتووکی یاسای کار (ل 324 - 366) | کۆلێژی یاسا - زانکۆی بەغدا</span>
        </div>
        <div class="academic-subfooter">
            <span class="supervisor-sub">سەرپەرشتیار: <strong>م.ی. هالة رحمن</strong></span>
            <span>لاپەڕە 2 لە 6 (پوختەی مۆبایل)</span>
        </div>
    </div>
</div>

<!-- 3. SLIDE 2 (02 / 04) -->
<div class="slide-page">
    <div class="page-border-frame"></div>
    <svg class="corner-ornament top-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament top-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>

    <div>
        <div class="top-header">
            <div class="univ-brand">
                <img src="{logo_gold_b64}" alt="زانکۆی نۆلج" class="univ-logo">
                <div class="univ-title-text">
                    <span class="univ-name">زانکۆی نۆلج — Knowledge University</span>
                    <span class="dept-name">بەشی بازاڕگەریی دیجیتاڵی | Business Law</span>
                </div>
            </div>
            <div class="header-badges">
                <span class="badge-counter">02 / 04</span>
            </div>
        </div>

        <div class="slide-intro-block">
            <span class="section-pill" style="border-color: #10b981; color: #6ee7b7; background: rgba(16, 185, 129, 0.15);">
                باسی دووەم - یەکەم
            </span>
            <h1 class="slide-main-title">کۆتاییهاتنی گرێبەست بە ڕێککەوتنی ویستی هەردوو لایەن</h1>
            <p class="slide-subtitle-text">هەڵوەشاندنەوەی پەیوەندیی گرێبەست بە ڕەزامەندیی هاوبەش و دەسەڵاتی ویست (ل 324)</p>
        </div>

        <div class="slide-media-container">
            <img src="{img_slide2_b64}" alt="ڕێککەوتنی فەرمی هەولێر">
            <div class="media-caption-badge">
                <span>⚖️ ڕێککەوتنی بەڕەزامەندی — شەقامی گوڵان هەولێر</span>
            </div>
        </div>

        <div class="points-list-wrapper">
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">1</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">بنەمای هەڵوەشاندنەوە:</strong>
                    جێبەجێکردنی بنەمای «گرێبەست شەریعەتی گرێبەستکەرانە» لە کۆتاییهێنان.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">2</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">درووستیی ڕەزامەندی:</strong>
                    بەتاڵبوونی ویستی کرێکار لە هەر زۆرلێکردنێکی ماددی یان دەروونی لەلایەن کارگێڕییەوە.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">3</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">پووچەڵبوونی دەستبەرداربوون:</strong>
                    پووچەڵیی دەستبەرداربوون لە مافە بنەڕەتییەکان وەک پاداشتی خزمەت.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">4</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">بەڵگەنامەکردنی نووسراو:</strong>
                    مەرجدارکردنی ڕێککەوتننامەی نووسراوی فەرمی کە بە یاسایی واژۆ کرابێت.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">5</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">بڕوانامەی ئەزموون:</strong>
                    پابەندبوونی خاوەنکار بە پێدانی ئەستۆپاکی و بڕوانامەی خزمەتی بێبەرامبەر.
                </div>
            </div>
        </div>
    </div>

    <div class="slide-bottom-bar">
        <div class="legal-reference-pill">
            <span>📖</span>
            <span>ماددەی (324 و دواتر) | هەڵوەشاندنەوەی بەڕەزامەندی و پاراستنی لایەنی لاوازتر</span>
        </div>
        <div class="academic-subfooter">
            <span class="supervisor-sub">سەرپەرشتیار: <strong>م.ی. هالة رحمن</strong></span>
            <span>لاپەڕە 3 لە 6 (پوختەی مۆبایل)</span>
        </div>
    </div>
</div>

<!-- 4. SLIDE 3 (03 / 04) -->
<div class="slide-page">
    <div class="page-border-frame"></div>
    <svg class="corner-ornament top-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament top-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>

    <div>
        <div class="top-header">
            <div class="univ-brand">
                <img src="{logo_gold_b64}" alt="زانکۆی نۆلج" class="univ-logo">
                <div class="univ-title-text">
                    <span class="univ-name">زانکۆی نۆلج — Knowledge University</span>
                    <span class="dept-name">بەشی بازاڕگەریی دیجیتاڵی | Business Law</span>
                </div>
            </div>
            <div class="header-badges">
                <span class="badge-counter">03 / 04</span>
            </div>
        </div>

        <div class="slide-intro-block">
            <span class="section-pill" style="border-color: #3b82f6; color: #93c5fd; background: rgba(59, 130, 246, 0.15);">
                باسی دووەم - دووەم
            </span>
            <h1 class="slide-main-title">کۆتاییهێنان بە گرێبەست بە ویستی تاکلایەنەی کرێکار</h1>
            <p class="slide-subtitle-text">پەیڕەوکردنی ئازادیی دەستووریی کرێکار لە کارکردن و مەرجەکانی ئاگادارکردنەوە (ل 328)</p>
        </div>

        <div class="slide-media-container">
            <img src="{img_slide3_b64}" alt="ئاگاداریی دەستلەکارکێشانەوە">
            <div class="media-caption-badge">
                <span>⚖️ ئاگاداریی دەستلەکارکێشانەوەی فەرمی — هەولێر</span>
            </div>
        </div>

        <div class="points-list-wrapper">
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">1</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">ئازادیی کارکردن:</strong>
                    قەدەغەکردنی کاری زۆرەملێ و چەسپاندنی مافی کرێکار لە دەستلەکارکێشانەوە.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">2</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">ماوەی ئاگادارکردنەوە:</strong>
                    پێشکەشکردنی ئاگاداریی نووسراوی فەرمی 30 ڕۆژ پێشوەختە.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">3</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">بەردەوامی لە کار:</strong>
                    پابەندبوونی کرێکار بە ئەنجامدانی ئەرکەکانی و وەرگرتنی مووچەکەی.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">4</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">بەجێهێشتنی دەستبەجێ:</strong>
                    ڕێگەپێدانی جێهێشتنی دەستبەجێ لەکاتی دەستدرێژیی خاوەنکار یان کەمکردنەوەی مووچە.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">5</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">سەلامەتیی پیشەیی:</strong>
                    مافی کرێکار لە کۆتاییهێنانی دەستبەجێ لەکاتی بوونی مەترسییەکی گەورە لەسەر تەندروستی.
                </div>
            </div>
        </div>
    </div>

    <div class="slide-bottom-bar">
        <div class="legal-reference-pill">
            <span>📖</span>
            <span>ماددەی (328 و دواتر) | دەستلەکارکێشانەوە و بارودۆخە ناوازەکانی جێهێشتنی ڕەوا</span>
        </div>
        <div class="academic-subfooter">
            <span class="supervisor-sub">سەرپەرشتیار: <strong>م.ی. هالة رحمن</strong></span>
            <span>لاپەڕە 4 لە 6 (پوختەی مۆبایل)</span>
        </div>
    </div>
</div>

<!-- 5. SLIDE 4 (04 / 04) -->
<div class="slide-page">
    <div class="page-border-frame"></div>
    <svg class="corner-ornament top-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament top-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>

    <div>
        <div class="top-header">
            <div class="univ-brand">
                <img src="{logo_gold_b64}" alt="زانکۆی نۆلج" class="univ-logo">
                <div class="univ-title-text">
                    <span class="univ-name">زانکۆی نۆلج — Knowledge University</span>
                    <span class="dept-name">بەشی بازاڕگەریی دیجیتاڵی | Business Law</span>
                </div>
            </div>
            <div class="header-badges">
                <span class="badge-counter">04 / 04</span>
            </div>
        </div>

        <div class="slide-intro-block">
            <span class="section-pill" style="border-color: #f59e0b; color: #fde68a; background: rgba(245, 158, 11, 0.15);">
                باسی دووەم - سێیەم
            </span>
            <h1 class="slide-main-title">کۆتاییهێنان بە گرێبەست بە ویستی خاوەنکار</h1>
            <p class="slide-subtitle-text">سنووردارکردنی دەسەڵاتی کارگێڕی و دەستەبەرییەکانی پاراستن لە دەرکردنی ستەمکارانە (ل 334)</p>
        </div>

        <div class="slide-media-container">
            <img src="{img_slide4_b64}" alt="پاراستن لە دەرکردنی ناڕەوا">
            <div class="media-caption-badge">
                <span>⚖️ چاودێریی دادگای کار — هەولێر</span>
            </div>
        </div>

        <div class="points-list-wrapper">
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">1</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">سنووردارکردنی دەسەڵات:</strong>
                    قەدەغەکردنی کۆتاییهێنان بە گرێبەستی بێسنوور بێ هۆکارێکی یاسایی و ڕژد.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">2</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">هۆکارە پەسەندکراوەکان:</strong>
                    داڕشتنەوەی ئابووری، نەبوونی لێهاتوویی سەلمێنراو، و خانەنشینی.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">3</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">پێوەری ستەمکاری:</strong>
                    پووچەڵبوونی دەرکردن کە پەیوەست بێت بە چالاکیی سەندیکایی یان جیاکاری.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">4</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">گەڕاندنەوەی کرێکار:</strong>
                    دەسەڵاتی دادگای کار لە بڕیاردان بە گەڕاندنەوەی دەرکراو و خەرجکردنی مووچەکانی.
                </div>
            </div>
            <div class="point-mobile-card">
                <div class="point-star-num">
                    <svg viewBox="0 0 32 32"><use href="#star8"/></svg>
                    <span class="point-digit">5</span>
                </div>
                <div class="point-content-text">
                    <strong class="point-prefix-strong">قەرەبووی دادپەروەرانە:</strong>
                    شایستەبوونی قەرەبووی دارایی دادپەروەرانە و پاداشتی خزمەت.
                </div>
            </div>
        </div>
    </div>

    <div class="slide-bottom-bar">
        <div class="legal-reference-pill">
            <span>📖</span>
            <span>ماددەی (334 و دواتر) | قەدەغەکردنی توندی کۆتاییهێنانی ستەمکارانە</span>
        </div>
        <div class="academic-subfooter">
            <span class="supervisor-sub">سەرپەرشتیار: <strong>م.ی. هالة رحمن</strong></span>
            <span>لاپەڕە 5 لە 6 (پوختەی مۆبایل)</span>
        </div>
    </div>
</div>

<!-- 7. BACK COVER (بەرگی کۆتایی) -->
<div class="slide-page back-cover-page">
    <div class="page-border-frame"></div>
    <svg class="corner-ornament top-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament top-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-right" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>
    <svg class="corner-ornament bottom-left" viewBox="0 0 50 50"><use href="#cornerArabesque"/></svg>

    <div class="cover-header-univ">
        <img src="{logo_gold_b64}" alt="زانکۆی نۆلج" class="cover-logo-large">
        <div class="cover-univ-title">زانکۆی نۆلج — Knowledge University</div>
        <div class="cover-dept-subtitle">کۆلێژی یاسا و کارگێڕی | بەشی بازاڕگەریی دیجیتاڵی</div>
    </div>

    <div class="cover-center-monument">
        <div class="cover-shamseh-seal">
            <svg viewBox="0 0 100 100" width="100" height="100">
                <circle cx="50" cy="50" r="46" fill="rgba(212,175,55,0.15)" stroke="#d4af37" stroke-width="2.5"/>
                <circle cx="50" cy="50" r="38" fill="rgba(212,175,55,0.25)" stroke="#fce8a6" stroke-width="1.5" stroke-dasharray="4 2"/>
                <text x="50" y="58" font-size="34" text-anchor="middle" fill="#ffd700">🛡️</text>
            </svg>
        </div>

        <h1 class="cover-title-big">بە سپاس و ستایشەوە کۆتایی هات</h1>
        <h2 class="cover-subtitle-big" style="font-size: 34px; color: #fce8a6;">
            کۆتایی توێژینەوەی کۆتاییهێنان بە گرێبەستی کار لە یاسای کاردا
        </h2>

        <div class="cover-flourish">
            <span class="cover-flourish-line"></span>
            <span style="color: #ffd700; font-size: 26px;">❖ ✤ ❖</span>
            <span class="cover-flourish-line"></span>
        </div>

        <div class="back-conclusion-list">
            <div class="back-conclusion-card">
                <span class="check-icon">✓</span>
                <span class="conclusion-text">تەواوکردنی سەرجەم بابەتەکانی باسی دووەم لە بەشی پێنجەمی یاسای کاری عێراقی.</span>
            </div>
            <div class="back-conclusion-card">
                <span class="check-icon">✓</span>
                <span class="conclusion-text">بنەمایەکی یاسایی ڕوون بۆ هاوسەنگی مافی کرێکار و بەرژەوەندییەکانی خاوەنکار.</span>
            </div>
            <div class="back-conclusion-card">
                <span class="check-icon">✓</span>
                <span class="conclusion-text">قەدەغەکردنی دەرکردنی ستەمکارانە و دەستەبەرکردنی چاودێریی دادگای کار.</span>
            </div>
            <div class="back-conclusion-card">
                <span class="check-icon">✓</span>
                <span class="conclusion-text">بەستنەوەی لایەنی تیۆری بە بازاڕی کار و کۆمپانیاکان لە هەولێر و بەغدا.</span>
            </div>
        </div>
    </div>

    <div class="cover-cards-grid">
        <div class="cover-info-card" style="justify-content: center; text-align: center; gap: 15px;">
            <span class="card-role">سەرپەرشتی و ڕێنوێنی:</span>
            <span class="card-val" style="color: #ffd700;">مامۆستای یاریدەدەر م.ی. هالة رحمن (Ass.L. Hala Rahman)</span>
        </div>
        <div style="font-size: 19px; color: #94a3b8; font-weight: 600; text-align: center;">
            مافی پارێزراوە © 2026 — زانکۆی نۆلج | یاسای کار (Business Law)
        </div>
    </div>
</div>

</body>
</html>
"""

def compile_pdf(html_file, output_pdf_path):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    
    print(f"[*] Compiling {os.path.basename(html_file)} -> {os.path.basename(output_pdf_path)}...", flush=True)
    file_url = "file:///" + os.path.abspath(html_file).replace("\\", "/")
    temp_ascii_pdf = os.path.join(BASE_DIR, "_temp_compile.pdf")
    if os.path.exists(temp_ascii_pdf):
        try:
            os.remove(temp_ascii_pdf)
        except Exception:
            pass

    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={temp_ascii_pdf}",
        file_url
    ]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        last_sz = 0
        stable = 0
        for _ in range(60):
            time.sleep(0.5)
            if os.path.exists(temp_ascii_pdf):
                sz = os.path.getsize(temp_ascii_pdf)
                if sz > 1000 and sz == last_sz:
                    stable += 1
                    if stable >= 2:
                        break
                else:
                    last_sz = sz
                    stable = 0
            if proc.poll() is not None:
                break
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            pass

        if os.path.exists(temp_ascii_pdf) and os.path.getsize(temp_ascii_pdf) > 1000:
            shutil.copyfile(temp_ascii_pdf, output_pdf_path)
            size_mb = os.path.getsize(output_pdf_path) / (1024 * 1024)
            print(f"[✓] Successfully generated {os.path.basename(output_pdf_path)} ({size_mb:.2f} MB)", flush=True)
            try:
                os.remove(temp_ascii_pdf)
            except Exception:
                pass
            return True
        else:
            print(f"[!] Error generating PDF. Output not created.", flush=True)
            return False
    except Exception as e:
        print(f"[!] Exception during PDF compile: {e}", flush=True)
        return False

def main():
    print("======================================================================")
    print("  Generating Mobile-Optimized Complete Slides PDF Presentation")
    print("======================================================================")
    
    # 1. Arabic HTML & PDF
    html_ar_path = os.path.join(BASE_DIR, "slides_presentation_mobile_ar.html")
    with open(html_ar_path, "w", encoding="utf-8") as f:
        f.write(generate_arabic_html())
    print(f"[✓] Created Arabic Mobile HTML: {html_ar_path}")

    # Copy to public
    shutil.copy(html_ar_path, os.path.join(BASE_DIR, "public", "slides_presentation_mobile_ar.html"))

    pdf_ar_root = os.path.join(BASE_DIR, "عرض_سلايدات_قانون_الاعمال_مخصص_للجوال.pdf")
    if compile_pdf(html_ar_path, pdf_ar_root):
        shutil.copy(pdf_ar_root, os.path.join(BASE_DIR, "public", "عرض_سلايدات_قانون_الاعمال_مخصص_للجوال.pdf"))
        print("[✓] Copied Arabic PDF to public/ directory.")

    # 2. Kurdish HTML & PDF
    html_ku_path = os.path.join(BASE_DIR, "slides_presentation_mobile_ku.html")
    with open(html_ku_path, "w", encoding="utf-8") as f:
        f.write(generate_kurdish_html())
    print(f"[✓] Created Kurdish Mobile HTML: {html_ku_path}")

    # Copy to public
    shutil.copy(html_ku_path, os.path.join(BASE_DIR, "public", "slides_presentation_mobile_ku.html"))

    pdf_ku_root = os.path.join(BASE_DIR, "پێشکەشکردنی_سلايده‌كانی_یاسای_کار_بۆ_مۆبایل.pdf")
    if compile_pdf(html_ku_path, pdf_ku_root):
        shutil.copy(pdf_ku_root, os.path.join(BASE_DIR, "public", "پێشکەشکردنی_سلايده‌كانی_یاسای_کار_بۆ_مۆبایل.pdf"))
        print("[✓] Copied Kurdish PDF to public/ directory.")

    print("\n[✓] Complete Mobile Slides PDF Generation Finished Successfully!")

if __name__ == "__main__":
    main()
