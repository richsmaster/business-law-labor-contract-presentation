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

# Load Fonts
qomra_bold_b64 = get_font_base64(os.path.join(BASE_DIR, "public", "fonts", "QOMRAARABICITF-BOLD.OTF"))
qomra_med_b64 = get_font_base64(os.path.join(BASE_DIR, "public", "fonts", "QOMRAARABICITF-MEDIUM.OTF"))
qomra_reg_b64 = get_font_base64(os.path.join(BASE_DIR, "public", "fonts", "QOMRAARABICITF-REGULAR.OTF"))
qomra_blk_b64 = get_font_base64(os.path.join(BASE_DIR, "public", "fonts", "QOMRAARABICITF-BLACK.OTF"))

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
if qomra_med_b64:
    font_faces += f"""
@font-face {{
    font-family: 'QomraCustom';
    src: url(data:font/opentype;base64,{qomra_med_b64}) format('opentype');
    font-weight: 500;
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
if qomra_blk_b64:
    font_faces += f"""
@font-face {{
    font-family: 'QomraCustom';
    src: url(data:font/opentype;base64,{qomra_blk_b64}) format('opentype');
    font-weight: 900;
    font-style: normal;
}}
"""

def generate_arabic_landscape_html():
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>عرض سلايدات قانون الأعمال — إنهاء عقد العمل</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@300;400;500;600;700;800;900&family=Amiri+Quran&family=Amiri:wght@400;700&family=Tajawal:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<style>
{font_faces}

:root {{
    --font-qomra: 'QomraCustom', 'Alexandria', 'Tajawal', sans-serif;
    --font-thuluth: 'Amiri', 'Amiri Quran', serif;
    --gold-primary: #d4af37;
    --gold-bright: #fce8a6;
    --gold-dark: #8c6710;
    --gold-gradient: linear-gradient(135deg, #fff5d0 0%, #e6c66e 30%, #d4af37 60%, #997314 100%);
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}}

@page {{
    size: 1920px 1080px;
    margin: 0;
}}

html, body {{
    margin: 0;
    padding: 0;
    background: #000000 !important;
    color: #ffffff;
    font-family: var(--font-qomra);
    direction: rtl;
}}

.slide-page {{
    width: 1920px;
    height: 1080px;
    position: relative;
    background: #000000;
    page-break-after: always;
    page-break-inside: avoid;
    break-after: page;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 32px 56px 36px 56px;
    box-sizing: border-box;
    overflow: hidden;
}}

/* Top Bar */
.slide-top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 64px;
    z-index: 30;
    padding-bottom: 12px;
    border-bottom: 1.5px solid rgba(212, 175, 55, 0.25);
}}

.univ-brand-box {{
    display: inline-flex;
    align-items: center;
    gap: 14px;
    background: rgba(14, 14, 14, 0.9);
    border: 1.4px solid rgba(212, 175, 55, 0.5);
    border-radius: 12px;
    padding: 6px 18px 6px 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.8), 0 0 18px rgba(212, 175, 55, 0.2);
}}

.univ-logo-img {{
    width: 38px;
    height: 38px;
    object-fit: contain;
    filter: drop-shadow(0 0 6px rgba(212, 175, 55, 0.5));
}}

.univ-brand-text {{
    font-size: 17px;
    font-weight: 700;
    color: var(--gold-bright);
    letter-spacing: 0.3px;
}}

.top-bar-left-box {{
    display: flex;
    align-items: center;
    gap: 16px;
}}

.course-pill {{
    background: rgba(212, 175, 55, 0.14);
    border: 1.4px solid rgba(212, 175, 55, 0.55);
    color: var(--gold-bright);
    padding: 7px 18px;
    border-radius: 9999px;
    font-size: 16px;
    font-weight: 800;
    box-shadow: 0 0 20px rgba(212, 175, 55, 0.22);
    display: flex;
    align-items: center;
    gap: 8px;
}}

.slide-counter-badge {{
    background: rgba(255, 255, 255, 0.08);
    border: 1.4px solid rgba(212, 175, 55, 0.45);
    padding: 7px 20px;
    border-radius: 10px;
    font-size: 17px;
    font-weight: 900;
    color: var(--gold-bright);
    font-family: 'Alexandria', sans-serif;
    letter-spacing: 1px;
}}

/* Main Slide Stage */
.slide-stage-container {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    margin-top: 14px;
}}

.book-page-leaf {{
    width: 100%;
    height: 100%;
    background: #000000 !important;
    border: 2px solid rgba(212, 175, 55, 0.52);
    border-radius: 20px;
    padding: 28px 60px;
    position: relative;
    box-shadow: 0 28px 70px rgba(0, 0, 0, 0.95), 0 0 40px rgba(212, 175, 55, 0.22);
    overflow: hidden;
    display: flex;
    align-items: center;
}}

/* Side Arabic Geometric Filigree Ornaments */
.side-arabesque-ornament {{
    position: absolute;
    top: 0;
    bottom: 0;
    width: 38px;
    pointer-events: none;
    z-index: 15;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    opacity: 0.85;
}}

.side-arabesque-ornament.right {{
    right: 8px;
}}

.side-arabesque-ornament.left {{
    left: 8px;
}}

.arabesque-pattern-svg {{
    width: 38px;
    height: 100%;
}}

/* Corner Filigrees */
.corner-filigree {{
    position: absolute;
    width: 60px;
    height: 60px;
    pointer-events: none;
    z-index: 16;
    opacity: 0.85;
}}

.corner-filigree.top-right {{ top: 8px; right: 8px; }}
.corner-filigree.top-left {{ top: 8px; left: 8px; }}
.corner-filigree.bottom-right {{ bottom: 8px; right: 8px; }}
.corner-filigree.bottom-left {{ bottom: 8px; left: 8px; }}

.page-spine-crease {{
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 35px;
    background: linear-gradient(to left, rgba(0, 0, 0, 0.7) 0%, transparent 100%);
    pointer-events: none;
    z-index: 10;
}}

.slide-bg-brain-watermark {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 540px;
    height: 540px;
    pointer-events: none;
    z-index: 1;
    opacity: 0.06;
    display: flex;
    align-items: center;
    justify-content: center;
    filter: drop-shadow(0 0 35px rgba(212, 175, 55, 0.2));
}}

.slide-bg-brain-watermark img {{
    width: 100%;
    height: 100%;
    object-fit: contain;
}}

/* 2-Column Slide Grid */
.slide-grid {{
    width: 100%;
    height: 100%;
    display: grid;
    grid-template-columns: 1.25fr 0.75fr;
    gap: 52px;
    align-items: center;
    position: relative;
    z-index: 10;
}}

.slide-content-col {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 14px;
    padding-left: 12px;
}}

.slide-badge-pill {{
    display: inline-flex;
    align-items: center;
    width: fit-content;
    padding: 4px 16px;
    border-radius: 9999px;
    border: 1.5px solid;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 2px;
}}

.slide-title-thuluth {{
    font-family: var(--font-qomra) !important;
    font-size: 38px;
    line-height: 1.32;
    font-weight: 800;
    color: #ffffff;
    text-shadow: 0 4px 16px rgba(0, 0, 0, 0.9), 0 0 32px rgba(212, 175, 55, 0.5);
    letter-spacing: 0.3px;
}}

.slide-subtitle {{
    font-family: var(--font-qomra);
    font-size: 19px;
    color: var(--gold-bright);
    font-weight: 700;
    line-height: 1.45;
    border-right: 4.5px solid var(--gold-primary);
    padding-right: 14px;
}}

.points-list {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 6px;
}}

.point-card {{
    background: rgba(14, 14, 14, 0.94);
    border: 1.5px solid rgba(212, 175, 55, 0.35);
    border-radius: 14px;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.65);
}}

.point-number-rosette {{
    position: relative;
    width: 44px;
    height: 44px;
    min-width: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    filter: drop-shadow(0 0 6px rgba(212, 175, 55, 0.5));
}}

.point-star-svg {{
    position: absolute;
    width: 100%;
    height: 100%;
}}

.point-digit {{
    position: relative;
    z-index: 2;
    font-weight: 900;
    font-size: 20px;
    color: #fffdf2;
    font-family: 'Alexandria', sans-serif;
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.9);
}}

.point-text {{
    font-size: 20px;
    color: #ffffff;
    line-height: 1.45;
    font-weight: 600;
    font-family: var(--font-qomra);
    letter-spacing: 0.2px;
}}

.point-gold-prefix {{
    color: var(--gold-bright);
    font-weight: 800;
    font-size: 20px;
    margin-left: 8px;
    text-shadow: 0 0 12px rgba(212, 175, 55, 0.35);
}}

.slide-footer-ref {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 15px;
    color: #fae69e;
    font-weight: 700;
    margin-top: 6px;
}}

/* Media Column */
.slide-media-col {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
}}

.image-card-wrapper {{
    width: 100%;
    height: 570px;
    max-height: 570px;
    border-radius: 22px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 25px 65px rgba(0, 0, 0, 0.85), 0 0 40px rgba(212, 175, 55, 0.32);
    border: 3px solid rgba(212, 175, 55, 0.52);
    background: #000000;
}}

.image-card-wrapper img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}}

.image-card-overlay {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.95) 0%, rgba(0, 0, 0, 0.5) 60%, transparent 100%);
    padding: 16px 20px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
}}

.image-stamp-badge {{
    background: rgba(212, 175, 55, 0.25);
    border: 1.2px solid var(--gold-primary);
    color: var(--gold-bright);
    padding: 5px 14px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 700;
    backdrop-filter: blur(8px);
}}

/* ======================================================== */
/* FRONT COVER STYLES                                       */
/* ======================================================== */
.cover-page-container {{
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}}

.book-leather-cover {{
    width: 100%;
    height: 100%;
    background: #000000;
    border: 2px solid rgba(212, 175, 55, 0.85);
    border-radius: 22px;
    padding: 18px 32px;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: inset 0 0 85px rgba(0, 0, 0, 0.98), inset 0 0 45px rgba(212, 175, 55, 0.45), 0 25px 65px rgba(0,0,0,0.9);
}}

.book-ornate-border {{
    border: 2px solid rgba(212, 175, 55, 0.8);
    outline: 1px dashed rgba(212, 175, 55, 0.5);
    outline-offset: -9px;
    height: 100%;
    border-radius: 16px;
    padding: 24px 36px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    position: relative;
    background: #000000;
}}

.book-spine-line {{
    position: absolute;
    right: 22px;
    top: 0;
    bottom: 0;
    width: 6px;
    background: linear-gradient(to bottom, rgba(212, 175, 55, 0.2), rgba(212, 175, 55, 0.85), rgba(212, 175, 55, 0.2));
    box-shadow: -3px 0 10px rgba(0,0,0,0.7);
}}

.cover-corner-ornament {{
    position: absolute;
    width: 104px;
    height: 104px;
    z-index: 12;
    pointer-events: none;
}}
.cover-corner-ornament.top-right {{ top: -3px; right: -3px; }}
.cover-corner-ornament.top-left {{ top: -3px; left: -3px; transform: scaleX(-1); }}
.cover-corner-ornament.bottom-right {{ bottom: -3px; right: -3px; transform: scaleY(-1); }}
.cover-corner-ornament.bottom-left {{ bottom: -3px; left: -3px; transform: scale(-1); }}

.cover-top-headpiece {{
    width: 100%;
    display: flex;
    justify-content: center;
    margin-bottom: 2px;
}}
.headpiece-svg {{
    width: 440px;
    height: 32px;
    filter: drop-shadow(0 0 8px rgba(212, 175, 55, 0.7));
}}

.cover-brain-watermark-3d {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 580px;
    height: 580px;
    pointer-events: none;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.brain-3d-halo {{
    position: absolute;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(212, 175, 55, 0.26) 0%, rgba(212, 175, 55, 0.1) 45%, transparent 70%);
    filter: blur(32px);
}}

.brain-3d-img {{
    width: 100%;
    height: 100%;
    object-fit: contain;
    opacity: 0.16;
    filter: drop-shadow(0 0 35px rgba(212, 175, 55, 0.6)) drop-shadow(0 0 75px rgba(212, 175, 55, 0.35));
}}

.cover-center-content {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
    z-index: 10;
    width: 100%;
    margin-top: -10px;
}}

.cover-shamseh-seal {{
    position: relative;
    width: 86px;
    height: 86px;
    display: flex;
    align-items: center;
    justify-content: center;
    filter: drop-shadow(0 0 25px rgba(212, 175, 55, 0.85));
    margin-bottom: 4px;
}}
.shamseh-svg {{
    width: 100%;
    height: 100%;
}}
.shamseh-icon-overlay {{
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.cover-title-container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 4px 0;
    padding: 10px 40px;
    text-align: center;
}}

.thuluth-cover-title {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    text-align: center;
}}

.title-row-1 {{
    font-size: 68px;
    font-weight: 900;
    line-height: 1.25;
    color: #ffffff;
    text-shadow: 0 4px 22px rgba(0, 0, 0, 0.95), 0 0 45px rgba(212, 175, 55, 0.8), 0 0 90px rgba(212, 175, 55, 0.45);
    letter-spacing: 0.5px;
}}

.title-row-2 {{
    font-size: 42px;
    font-weight: 700;
    line-height: 1.35;
    color: var(--gold-bright);
    text-shadow: 0 4px 18px rgba(0, 0, 0, 0.95), 0 0 35px rgba(212, 175, 55, 0.7);
    letter-spacing: 0.3px;
}}

.calligraphic-flourish {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin: 8px 0;
}}

.flourish-line {{
    width: 140px;
    height: 2px;
    background: linear-gradient(to right, transparent, rgba(212, 175, 55, 0.85), transparent);
}}

.flourish-diamond {{
    color: var(--gold-bright);
    font-size: 24px;
    filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.9));
}}

.cover-bottom-year {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    z-index: 10;
}}

.cover-footer-badges {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    width: 100%;
}}

.footer-tag-univ,
.footer-tag-dept,
.footer-tag-course {{
    background: rgba(14, 14, 14, 0.92);
    border: 1.3px solid rgba(212, 175, 55, 0.5);
    border-radius: 10px;
    padding: 6px 20px;
    font-size: 16px;
    font-weight: 700;
    color: var(--gold-bright);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.75), 0 0 14px rgba(212, 175, 55, 0.22);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    white-space: nowrap;
}}

.footer-diamond {{
    color: var(--gold-primary);
    margin-left: 8px;
    font-size: 14px;
}}

.cover-footer-subline {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    font-size: 16px;
    font-weight: 600;
    color: #e2e8f0;
    text-shadow: 0 1px 6px rgba(0, 0, 0, 0.9);
    margin-top: 4px;
}}

/* ======================================================== */
/* BACK COVER STYLES                                        */
/* ======================================================== */
.back-cover-border {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    height: 100%;
    padding: 36px;
}}

.back-cover-center {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 24px;
    width: 100%;
    max-width: 1100px;
}}

.back-cover-title {{
    font-size: 56px;
    font-weight: 900;
    color: #ffffff;
    text-shadow: 0 4px 25px rgba(0, 0, 0, 0.95), 0 0 50px rgba(212, 175, 55, 0.85), 0 0 95px rgba(212, 175, 55, 0.45);
    margin: 0;
    line-height: 1.3;
}}

.cover-gold-divider {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 450px;
    position: relative;
    margin: 4px auto;
}}
.cover-gold-divider::before,
.cover-gold-divider::after {{
    content: '';
    flex: 1;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.85), transparent);
}}
.cover-gold-divider .divider-diamond {{
    color: #fce8a6;
    font-size: 22px;
    padding: 0 18px;
    filter: drop-shadow(0 0 12px rgba(212, 175, 55, 0.9));
}}

.back-cover-sub {{
    text-align: center;
    font-size: 24px;
    font-weight: 500;
    color: #fce8a6;
    line-height: 1.6;
    max-width: 900px;
    text-shadow: 0 2px 14px rgba(0, 0, 0, 0.9), 0 0 25px rgba(212, 175, 55, 0.5);
}}

.back-cover-author {{
    display: inline-flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    gap: 16px;
    background: rgba(212, 175, 55, 0.12);
    border: 1.8px solid rgba(212, 175, 55, 0.55);
    border-radius: 9999px;
    padding: 14px 44px;
    backdrop-filter: blur(12px);
    box-shadow: 0 6px 30px rgba(0, 0, 0, 0.7), inset 0 0 25px rgba(212, 175, 55, 0.2);
}}

.back-author-role {{
    color: #fce8a6;
    font-weight: 700;
    font-size: 19px;
}}

.back-author-name {{
    color: #ffffff;
    font-weight: 800;
    font-size: 21px;
    letter-spacing: 0.3px;
}}

.summary-cards-container {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    width: 100%;
    max-width: 940px;
    margin-top: 6px;
}}

.summary-card {{
    background: rgba(14, 14, 14, 0.88);
    border: 1.3px solid rgba(212, 175, 55, 0.35);
    border-radius: 12px;
    padding: 12px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    text-align: right;
}}

.summary-check {{
    color: #10b981;
    font-size: 20px;
    font-weight: 900;
}}

.summary-text {{
    font-size: 18px;
    color: #ffffff;
    font-weight: 600;
}}
</style>
</head>
<body>

<!-- SVG Defs for Arabesques and Corners -->
<svg style="display: none;">
  <defs>
    <!-- Corner Arabesque -->
    <g id="cornerArabesque">
      <path d="M4,4 L44,4 Q56,4 56,16 L56,56 Q56,4 4,4" fill="none" stroke="url(#cornerGrad)" stroke-width="1.8" />
      <path d="M10,10 Q32,10 42,20 Q52,30 52,52" fill="none" stroke="url(#cornerGrad)" stroke-width="1.2" />
      <path d="M10,10 Q10,32 20,42 Q30,52 52,52" fill="none" stroke="url(#cornerGrad)" stroke-width="1.2" />
      <path d="M22,22 Q32,14 40,24 Q48,34 38,40 Q28,46 22,34 Z" fill="rgba(212, 175, 55, 0.2)" stroke="url(#cornerGrad)" stroke-width="1" />
      <circle cx="14" cy="14" r="3" fill="#fffdfa" stroke="#aa8216" stroke-width="1" />
      <circle cx="48" cy="48" r="2.5" fill="#fce8a6" />
      <circle cx="30" cy="30" r="3.5" fill="#ffd700" stroke="#7a580a" stroke-width="1" />
    </g>
    <linearGradient id="cornerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff5d0" />
      <stop offset="50%" stop-color="#d4af37" />
      <stop offset="100%" stop-color="#8a6712" />
    </linearGradient>

    <!-- Side Arabesque Ornament Pattern -->
    <g id="sideArabesque">
      <line x1="3" y1="10" x2="3" y2="590" stroke="url(#goldSideGrad)" stroke-width="1.5" stroke-opacity="0.85" />
      <line x1="7" y1="20" x2="7" y2="580" stroke="url(#goldSideGrad)" stroke-width="0.8" stroke-dasharray="4 3" stroke-opacity="0.7" />
      <!-- Star Rosettes -->
      <g transform="translate(0, 50)"><use href="#rosetteCluster" /></g>
      <g transform="translate(0, 130)"><use href="#rosetteCluster" /></g>
      <g transform="translate(0, 210)"><use href="#rosetteCluster" /></g>
      <g transform="translate(0, 290)"><use href="#rosetteCluster" /></g>
      <g transform="translate(0, 370)"><use href="#rosetteCluster" /></g>
      <g transform="translate(0, 450)"><use href="#rosetteCluster" /></g>
      <g transform="translate(0, 530)"><use href="#rosetteCluster" /></g>
    </g>
    <g id="rosetteCluster">
      <path d="M19,-36 L26,-22 L19,-8 L12,-22 Z" fill="none" stroke="url(#goldSideGrad)" stroke-width="1.2" />
      <circle cx="19" cy="-22" r="2" fill="#fff5d0" />
      <rect x="11" y="-8" width="16" height="16" fill="rgba(212, 175, 55, 0.15)" stroke="url(#goldSideGrad)" stroke-width="1.3" />
      <rect x="11" y="-8" width="16" height="16" transform="rotate(45 19 0)" fill="rgba(212, 175, 55, 0.15)" stroke="url(#goldSideGrad)" stroke-width="1.3" />
      <circle cx="19" cy="0" r="3" fill="#fffbf0" stroke="#997314" stroke-width="0.8" />
      <path d="M19,10 Q28,18 19,26 Q10,18 19,10" fill="none" stroke="url(#goldSideGrad)" stroke-width="1.1" />
      <circle cx="19" cy="18" r="1.5" fill="#fce8a6" />
    </g>
    <linearGradient id="goldSideGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff2cc" />
      <stop offset="40%" stop-color="#d4af37" />
      <stop offset="75%" stop-color="#aa8216" />
      <stop offset="100%" stop-color="#e5c158" />
    </linearGradient>

    <!-- Point Star Rosette -->
    <g id="pointStar">
      <rect x="6" y="6" width="20" height="20" fill="rgba(212, 175, 55, 0.25)" stroke="#d4af37" stroke-width="1.2" />
      <rect x="6" y="6" width="20" height="20" transform="rotate(45 16 16)" fill="rgba(212, 175, 55, 0.25)" stroke="#d4af37" stroke-width="1.2" />
    </g>
  </defs>
</svg>

<!-- ======================================================== -->
<!-- 1. FRONT COVER (الغلاف الأمامي الملكي)                    -->
<!-- ======================================================== -->
<div class="slide-page" id="page-cover">
    <div class="cover-page-container">
        <div class="book-leather-cover">
            <div class="book-ornate-border">
                <!-- 4 Corner Arabesques -->
                <svg class="cover-corner-ornament top-right" viewBox="0 0 96 96">
                    <path d="M4,4 L88,4 Q88,24 74,38 Q60,52 38,74 Q24,88 4,88 Z" fill="rgba(212, 175, 55, 0.2)" stroke="#d4af37" stroke-width="1.6" />
                    <g transform="translate(30, 30)">
                        <rect x="-10" y="-10" width="20" height="20" fill="rgba(212, 175, 55, 0.4)" stroke="#d4af37" stroke-width="1.2" />
                        <rect x="-10" y="-10" width="20" height="20" transform="rotate(45)" fill="rgba(212, 175, 55, 0.4)" stroke="#d4af37" stroke-width="1.2" />
                        <circle cx="0" cy="0" r="3.5" fill="#ffffff" stroke="#997314" stroke-width="0.8" />
                    </g>
                </svg>
                <svg class="cover-corner-ornament top-left" viewBox="0 0 96 96">
                    <path d="M4,4 L88,4 Q88,24 74,38 Q60,52 38,74 Q24,88 4,88 Z" fill="rgba(212, 175, 55, 0.2)" stroke="#d4af37" stroke-width="1.6" />
                    <g transform="translate(30, 30)">
                        <rect x="-10" y="-10" width="20" height="20" fill="rgba(212, 175, 55, 0.4)" stroke="#d4af37" stroke-width="1.2" />
                        <rect x="-10" y="-10" width="20" height="20" transform="rotate(45)" fill="rgba(212, 175, 55, 0.4)" stroke="#d4af37" stroke-width="1.2" />
                        <circle cx="0" cy="0" r="3.5" fill="#ffffff" stroke="#997314" stroke-width="0.8" />
                    </g>
                </svg>
                <svg class="cover-corner-ornament bottom-right" viewBox="0 0 96 96">
                    <path d="M4,4 L88,4 Q88,24 74,38 Q60,52 38,74 Q24,88 4,88 Z" fill="rgba(212, 175, 55, 0.2)" stroke="#d4af37" stroke-width="1.6" />
                    <g transform="translate(30, 30)">
                        <rect x="-10" y="-10" width="20" height="20" fill="rgba(212, 175, 55, 0.4)" stroke="#d4af37" stroke-width="1.2" />
                        <rect x="-10" y="-10" width="20" height="20" transform="rotate(45)" fill="rgba(212, 175, 55, 0.4)" stroke="#d4af37" stroke-width="1.2" />
                        <circle cx="0" cy="0" r="3.5" fill="#ffffff" stroke="#997314" stroke-width="0.8" />
                    </g>
                </svg>
                <svg class="cover-corner-ornament bottom-left" viewBox="0 0 96 96">
                    <path d="M4,4 L88,4 Q88,24 74,38 Q60,52 38,74 Q24,88 4,88 Z" fill="rgba(212, 175, 55, 0.2)" stroke="#d4af37" stroke-width="1.6" />
                    <g transform="translate(30, 30)">
                        <rect x="-10" y="-10" width="20" height="20" fill="rgba(212, 175, 55, 0.4)" stroke="#d4af37" stroke-width="1.2" />
                        <rect x="-10" y="-10" width="20" height="20" transform="rotate(45)" fill="rgba(212, 175, 55, 0.4)" stroke="#d4af37" stroke-width="1.2" />
                        <circle cx="0" cy="0" r="3.5" fill="#ffffff" stroke="#997314" stroke-width="0.8" />
                    </g>
                </svg>

                <div class="book-spine-line"></div>

                <!-- Top Royal Crown Arch -->
                <div class="cover-top-headpiece">
                    <svg viewBox="0 0 460 36" class="headpiece-svg">
                        <defs>
                            <linearGradient id="headpieceGoldCover" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stop-color="transparent" />
                                <stop offset="20%" stop-color="#997314" />
                                <stop offset="50%" stop-color="#fff8e7" />
                                <stop offset="80%" stop-color="#997314" />
                                <stop offset="100%" stop-color="transparent" />
                            </linearGradient>
                        </defs>
                        <path d="M20,32 Q130,32 185,16 Q210,6 230,2 Q250,6 275,16 Q330,32 440,32" fill="none" stroke="url(#headpieceGoldCover)" stroke-width="2.2" />
                        <path d="M50,28 Q140,28 190,14 Q210,6 230,4 Q250,6 270,14 Q320,28 410,28" fill="none" stroke="url(#headpieceGoldCover)" stroke-width="1.2" stroke-dasharray="3 2" opacity="0.85" />
                        <circle cx="230" cy="2" r="3.5" fill="#ffffff" stroke="#997314" stroke-width="1" />
                    </svg>
                </div>

                <!-- 3D Brain Watermark Background -->
                <div class="cover-brain-watermark-3d">
                    <div class="brain-3d-halo"></div>
                    <img src="{brain_watermark_b64}" alt="Knowledge University Brain" class="brain-3d-img">
                </div>

                <!-- Central Content -->
                <div class="cover-center-content">
                    <!-- Royal Shamseh Seal with Scales of Justice -->
                    <div class="cover-shamseh-seal">
                        <svg viewBox="0 0 90 90" class="shamseh-svg">
                            <defs>
                                <linearGradient id="shamsehGold" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stop-color="#fffdf0" />
                                    <stop offset="35%" stop-color="#f5d36e" />
                                    <stop offset="70%" stop-color="#d4af37" />
                                    <stop offset="100%" stop-color="#7a550a" />
                                </linearGradient>
                            </defs>
                            <circle cx="45" cy="45" r="42" fill="none" stroke="url(#shamsehGold)" stroke-width="1.3" stroke-dasharray="3 3" />
                            <circle cx="45" cy="45" r="39" fill="rgba(20, 12, 6, 0.9)" stroke="url(#shamsehGold)" stroke-width="1.8" />
                            <rect x="20" y="20" width="50" height="50" fill="none" stroke="url(#shamsehGold)" stroke-width="1.4" opacity="0.95" />
                            <rect x="20" y="20" width="50" height="50" transform="rotate(45 45 45)" fill="none" stroke="url(#shamsehGold)" stroke-width="1.4" opacity="0.95" />
                            <circle cx="45" cy="45" r="23" fill="rgba(212, 175, 55, 0.2)" stroke="url(#shamsehGold)" stroke-width="1.2" />
                        </svg>
                        <div class="shamseh-icon-overlay">
                            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff8e7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>
                            </svg>
                        </div>
                    </div>

                    <!-- Grand Titles -->
                    <div class="cover-title-container">
                        <h1 class="thuluth-cover-title">
                            <span class="title-row-1">إنهاء عقد العمل</span>
                            <span class="title-row-2">بإرادة أحد طرفيه أو كليهما</span>
                        </h1>
                    </div>

                    <!-- Flourish -->
                    <div class="calligraphic-flourish">
                        <span class="flourish-line" style="transform: scaleX(-1);"></span>
                        <span style="color: #d4af37; font-size: 18px;">✤</span>
                        <span class="flourish-diamond">❖</span>
                        <span style="color: #d4af37; font-size: 18px;">✤</span>
                        <span class="flourish-line"></span>
                    </div>

                    <p style="font-size: 20px; color: #fae69e; font-weight: 600; text-align: center; max-width: 820px; text-shadow: 0 2px 10px rgba(0,0,0,0.9);">
                        دراسة قانونية متخصصة ومقارنة في ضوء أحكام قانون العمل العراقي رقم (37) لسنة 2015
                    </p>
                </div>

                <!-- Footer Badges -->
                <div class="cover-bottom-year">
                    <div class="cover-footer-badges">
                        <span class="footer-tag-univ">
                            <span class="footer-diamond">❖</span>
                            جامعة نولج — Knowledge University
                        </span>
                        <span class="footer-tag-dept">
                            قسم التسويق الرقمي (Digital Marketing)
                        </span>
                        <span class="footer-tag-course">
                            مقرر قانون الأعمال (Business Law)
                        </span>
                    </div>
                    <div class="cover-footer-subline">
                        <span>إشراف الأستاذة: م.م. هالة رحمن (Ass.L. Hala Rahman)</span>
                        <span style="color: #d4af37;">•</span>
                        <span>العام الأكاديمي 2025 - 2026</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- 2. SLIDE 1 (01 / 04) - مفهوم إنهاء عقد العمل             -->
<!-- ======================================================== -->
<div class="slide-page" id="slide-1">
    <!-- Top Bar -->
    <div class="slide-top-bar">
        <div class="univ-brand-box">
            <img src="{logo_gold_b64}" alt="جامعة نولج" class="univ-logo-img">
            <span class="univ-brand-text">جامعة نولج — Knowledge University | قسم التسويق الرقمي</span>
        </div>
        <div class="top-bar-left-box">
            <div class="course-pill">
                <span>⚖️</span>
                <span>قانون الأعمال | Business Law</span>
            </div>
            <div class="slide-counter-badge">01 / 04</div>
        </div>
    </div>

    <!-- Main Stage -->
    <div class="slide-stage-container">
        <div class="book-page-leaf">
            <div class="page-spine-crease"></div>
            <!-- Side Arabesques -->
            <div class="side-arabesque-ornament right"><svg class="arabesque-pattern-svg" viewBox="0 0 38 600"><use href="#sideArabesque" /></svg></div>
            <div class="side-arabesque-ornament left"><svg class="arabesque-pattern-svg" viewBox="0 0 38 600" style="transform: scaleX(-1);"><use href="#sideArabesque" /></svg></div>
            <!-- Corners -->
            <svg class="corner-filigree top-right" viewBox="0 0 64 64"><use href="#cornerArabesque" /></svg>
            <svg class="corner-filigree top-left" viewBox="0 0 64 64" style="transform: scaleX(-1);"><use href="#cornerArabesque" /></svg>
            <svg class="corner-filigree bottom-right" viewBox="0 0 64 64" style="transform: scaleY(-1);"><use href="#cornerArabesque" /></svg>
            <svg class="corner-filigree bottom-left" viewBox="0 0 64 64" style="transform: scale(-1);"><use href="#cornerArabesque" /></svg>

            <!-- Brain Watermark -->
            <div class="slide-bg-brain-watermark"><img src="{brain_watermark_b64}" alt="Brain Watermark"></div>

            <div class="slide-grid">
                <!-- Content Column -->
                <div class="slide-content-col">
                    <span class="slide-badge-pill" style="border-color: #c59b27; color: #fde68a; background: rgba(197, 155, 39, 0.15);">
                        غلاف العرض التقديمي الأكاديمي
                    </span>
                    <h1 class="slide-title-thuluth">إنهاء عقد العمل بإرادة أحد طرفيه أو كليهما</h1>
                    <p class="slide-subtitle">مقرر قانون الأعمال (Business Law) — بإشراف: م.م. هالة رحمن (Ass.L. Hala Rahman)</p>
                    <div class="points-list">
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">1</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">الموضوع الدراسي:</strong>
                                <span>المبحث الثاني من الفصل الخامس في قانون العمل العراقي.</span>
                            </div>
                        </div>
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">2</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">المرجع المعتمد:</strong>
                                <span>مؤلف الدكتور عدنان العابد والدكتور يوسف إلياس.</span>
                            </div>
                        </div>
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">3</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">التأصيل القانوني:</strong>
                                <span>انحلال الرابطة العقدية بالرضا المشترك أو بالإرادة المنفردة.</span>
                            </div>
                        </div>
                    </div>
                    <div class="slide-footer-ref">
                        <span>📖 كتاب قانون العمل (ص 324 - 366) | كلية القانون - جامعة بغداد</span>
                    </div>
                </div>

                <!-- Media Column -->
                <div class="slide-media-col">
                    <div class="image-card-wrapper">
                        <img src="{img_slide1_b64}" alt="مكتب المحاماة الفاخر وإطلالة قلعة أربيل">
                        <div class="image-card-overlay">
                            <div class="image-stamp-badge">⚖️ عقد عمل موثق — إطلالة قلعة أربيل</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- 3. SLIDE 2 (02 / 04) - التقايل الرضائي                   -->
<!-- ======================================================== -->
<div class="slide-page" id="slide-2">
    <!-- Top Bar -->
    <div class="slide-top-bar">
        <div class="univ-brand-box">
            <img src="{logo_gold_b64}" alt="جامعة نولج" class="univ-logo-img">
            <span class="univ-brand-text">جامعة نولج — Knowledge University | قسم التسويق الرقمي</span>
        </div>
        <div class="top-bar-left-box">
            <div class="course-pill">
                <span>⚖️</span>
                <span>قانون الأعمال | Business Law</span>
            </div>
            <div class="slide-counter-badge">02 / 04</div>
        </div>
    </div>

    <!-- Main Stage -->
    <div class="slide-stage-container">
        <div class="book-page-leaf">
            <div class="page-spine-crease"></div>
            <div class="side-arabesque-ornament right"><svg class="arabesque-pattern-svg" viewBox="0 0 38 600"><use href="#sideArabesque" /></svg></div>
            <div class="side-arabesque-ornament left"><svg class="arabesque-pattern-svg" viewBox="0 0 38 600" style="transform: scaleX(-1);"><use href="#sideArabesque" /></svg></div>
            <svg class="corner-filigree top-right" viewBox="0 0 64 64"><use href="#cornerArabesque" /></svg>
            <svg class="corner-filigree top-left" viewBox="0 0 64 64" style="transform: scaleX(-1);"><use href="#cornerArabesque" /></svg>
            <svg class="corner-filigree bottom-right" viewBox="0 0 64 64" style="transform: scaleY(-1);"><use href="#cornerArabesque" /></svg>
            <svg class="corner-filigree bottom-left" viewBox="0 0 64 64" style="transform: scale(-1);"><use href="#cornerArabesque" /></svg>

            <div class="slide-grid">
                <!-- Content Column -->
                <div class="slide-content-col">
                    <span class="slide-badge-pill" style="border-color: #10b981; color: #a7f3d0; background: rgba(16, 185, 129, 0.15);">
                        المبحث الثاني - أولاً
                    </span>
                    <h1 class="slide-title-thuluth">انتهاء العقد باتفاق إرادتي طرفيه (التقايل الرضائي)</h1>
                    <p class="slide-subtitle">انحلال الرابطة العقدية بالتراضي المشترك وسلطان الإرادة (ص 324)</p>
                    <div class="points-list">
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">1</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">مبدأ التقايل:</strong>
                                <span>تطبيق قاعدة «العقد شريعة المتعاقدين» في إنهائه رضائياً.</span>
                            </div>
                        </div>
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">2</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">سلامة الرضا:</strong>
                                <span>خلو إرادة العامل من أي إكراه مادي أو معنوي صادر عن الإدارة.</span>
                            </div>
                        </div>
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">3</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">بطلان التنازل:</strong>
                                <span>بطلان إسقاط الحقوق الآمرة كمكافأة نهاية الخدمة والإجازات.</span>
                            </div>
                        </div>
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">4</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">التوثيق الخطي:</strong>
                                <span>اشتراط عقد مخالصة كتابي رسمي موقع ومختوم قانوناً.</span>
                            </div>
                        </div>
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">5</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">شهادة الخبرة:</strong>
                                <span>التزام صاحب العمل بتسليم العامل براءة ذمة وشهادة خدمة مجانية.</span>
                            </div>
                        </div>
                    </div>
                    <div class="slide-footer-ref">
                        <span>📖 المادة (324 وما بعدها) | التقايل الرضائي وحماية الطرف الأضعف</span>
                    </div>
                </div>

                <!-- Media Column -->
                <div class="slide-media-col">
                    <div class="image-card-wrapper">
                        <img src="{img_slide2_b64}" alt="عقود عمل موثقة وإطلالة فندق ديفان أربيل">
                        <div class="image-card-overlay">
                            <div class="image-stamp-badge">⚖️ إطلالة فندق ديفان أربيل — شارع كولان</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- 4. SLIDE 3 (03 / 04) - استقالة العامل والترك              -->
<!-- ======================================================== -->
<div class="slide-page" id="slide-3">
    <!-- Top Bar -->
    <div class="slide-top-bar">
        <div class="univ-brand-box">
            <img src="{logo_gold_b64}" alt="جامعة نولج" class="univ-logo-img">
            <span class="univ-brand-text">جامعة نولج — Knowledge University | قسم التسويق الرقمي</span>
        </div>
        <div class="top-bar-left-box">
            <div class="course-pill">
                <span>⚖️</span>
                <span>قانون الأعمال | Business Law</span>
            </div>
            <div class="slide-counter-badge">03 / 04</div>
        </div>
    </div>

    <!-- Main Stage -->
    <div class="slide-stage-container">
        <div class="book-page-leaf">
            <div class="page-spine-crease"></div>
            <div class="side-arabesque-ornament right"><svg class="arabesque-pattern-svg" viewBox="0 0 38 600"><use href="#sideArabesque" /></svg></div>
            <div class="side-arabesque-ornament left"><svg class="arabesque-pattern-svg" viewBox="0 0 38 600" style="transform: scaleX(-1);"><use href="#sideArabesque" /></svg></div>
            <svg class="corner-filigree top-right" viewBox="0 0 64 64"><use href="#cornerArabesque" /></svg>
            <svg class="corner-filigree top-left" viewBox="0 0 64 64" style="transform: scaleX(-1);"><use href="#cornerArabesque" /></svg>
            <svg class="corner-filigree bottom-right" viewBox="0 0 64 64" style="transform: scaleY(-1);"><use href="#cornerArabesque" /></svg>
            <svg class="corner-filigree bottom-left" viewBox="0 0 64 64" style="transform: scale(-1);"><use href="#cornerArabesque" /></svg>

            <div class="slide-grid">
                <!-- Content Column -->
                <div class="slide-content-col">
                    <span class="slide-badge-pill" style="border-color: #3b82f6; color: #bfdbfe; background: rgba(59, 130, 246, 0.15);">
                        المبحث الثاني - ثانياً
                    </span>
                    <h1 class="slide-title-thuluth">إنهاء العقد بالإرادة المنفردة للعامل (الاستقالة والترك)</h1>
                    <p class="slide-subtitle">ممارسة العامل لحريته الدستورية في العمل وضوابط الإخطار (ص 328)</p>
                    <div class="points-list">
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">1</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">حرية العمل:</strong>
                                <span>حظر السخرة وإقرار حق العامل في الاستقالة بإرادته المنفردة.</span>
                            </div>
                        </div>
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">2</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">مهلة الإخطار:</strong>
                                <span>توجيه إنذار كتابي رسمي قبل 30 يوماً لضمان انتظام العمل.</span>
                            </div>
                        </div>
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">3</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">الاستمرار بالعمل:</strong>
                                <span>التزام العامل بأداء واجباته وتقاضي أجره خلال مهلة الإنذار.</span>
                            </div>
                        </div>
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">4</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">الترك الفوري المبرر:</strong>
                                <span>جواز المغادرة الفورية عند اعتداء صاحب العمل أو خفض الأجر.</span>
                            </div>
                        </div>
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">5</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">السلامة المهنية:</strong>
                                <span>حق العامل بإنهاء العقد فوراً عند ثبوت خطر داهم يهدد صحته.</span>
                            </div>
                        </div>
                    </div>
                    <div class="slide-footer-ref">
                        <span>📖 المادة (328 وما بعدها) | الاستقالة والحالات الاستثنائية للترك المشروع</span>
                    </div>
                </div>

                <!-- Media Column -->
                <div class="slide-media-col">
                    <div class="image-card-wrapper">
                        <img src="{img_slide3_b64}" alt="إشعار استقالة في مكتب تنفيذي بأربيل">
                        <div class="image-card-overlay">
                            <div class="image-stamp-badge">⚖️ إشعار استقالة رسمي — أربيل</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- 5. SLIDE 4 (04 / 04) - إنهاء صاحب العمل                  -->
<!-- ======================================================== -->
<div class="slide-page" id="slide-4">
    <!-- Top Bar -->
    <div class="slide-top-bar">
        <div class="univ-brand-box">
            <img src="{logo_gold_b64}" alt="جامعة نولج" class="univ-logo-img">
            <span class="univ-brand-text">جامعة نولج — Knowledge University | قسم التسويق الرقمي</span>
        </div>
        <div class="top-bar-left-box">
            <div class="course-pill">
                <span>⚖️</span>
                <span>قانون الأعمال | Business Law</span>
            </div>
            <div class="slide-counter-badge">04 / 04</div>
        </div>
    </div>

    <!-- Main Stage -->
    <div class="slide-stage-container">
        <div class="book-page-leaf">
            <div class="page-spine-crease"></div>
            <div class="side-arabesque-ornament right"><svg class="arabesque-pattern-svg" viewBox="0 0 38 600"><use href="#sideArabesque" /></svg></div>
            <div class="side-arabesque-ornament left"><svg class="arabesque-pattern-svg" viewBox="0 0 38 600" style="transform: scaleX(-1);"><use href="#sideArabesque" /></svg></div>
            <svg class="corner-filigree top-right" viewBox="0 0 64 64"><use href="#cornerArabesque" /></svg>
            <svg class="corner-filigree top-left" viewBox="0 0 64 64" style="transform: scaleX(-1);"><use href="#cornerArabesque" /></svg>
            <svg class="corner-filigree bottom-right" viewBox="0 0 64 64" style="transform: scaleY(-1);"><use href="#cornerArabesque" /></svg>
            <svg class="corner-filigree bottom-left" viewBox="0 0 64 64" style="transform: scale(-1);"><use href="#cornerArabesque" /></svg>

            <div class="slide-grid">
                <!-- Content Column -->
                <div class="slide-content-col">
                    <span class="slide-badge-pill" style="border-color: #f59e0b; color: #fde68a; background: rgba(245, 158, 11, 0.15);">
                        المبحث الثاني - ثالثاً
                    </span>
                    <h1 class="slide-title-thuluth">إنهاء العقد بإرادة صاحب العمل</h1>
                    <p class="slide-subtitle">قيود سلطة الإدارة في الإنهاء وضمانات الحماية من الفصل الجائر (ص 334)</p>
                    <div class="points-list">
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">1</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">تقييد سلطة الإنهاء:</strong>
                                <span>حظر إنهاء العقد غير محدد المدة دون سبب مشروع وجدي.</span>
                            </div>
                        </div>
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">2</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">الأسباب المقبولة:</strong>
                                <span>إعادة الهيكلة الاقتصادية، عدم الكفاءة المثبتة، وبلوغ التقاعد.</span>
                            </div>
                        </div>
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">3</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">معيار التعسف:</strong>
                                <span>بطلان الفصل المرتبط بنشاط نقابي، شكوى قانونية، أو تمييز.</span>
                            </div>
                        </div>
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">4</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">إعادة العامل:</strong>
                                <span>اختصاص محكمة العمل بالحكم بإعادة المفصول وصرف كامل أجوره.</span>
                            </div>
                        </div>
                        <div class="point-card">
                            <div class="point-number-rosette">
                                <svg viewBox="0 0 32 32" class="point-star-svg"><use href="#pointStar" /></svg>
                                <span class="point-digit">5</span>
                            </div>
                            <div class="point-text">
                                <strong class="point-gold-prefix">التعويض الجابر:</strong>
                                <span>استحقاق تعويض مالي عادل وبدل مهلة الإخطار ومكافأة الخدمة.</span>
                            </div>
                        </div>
                    </div>
                    <div class="slide-footer-ref">
                        <span>📖 المادة (334 وما بعدها) | الحظر الصارم للإنهاء التعسفي</span>
                    </div>
                </div>

                <!-- Media Column -->
                <div class="slide-media-col">
                    <div class="image-card-wrapper">
                        <img src="{img_slide4_b64}" alt="إنهاء العقد وضمانات الرقابة القضائية">
                        <div class="image-card-overlay">
                            <div class="image-stamp-badge">⚖️ رقابة القضاء العمالي — أربيل</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- ======================================================== -->
<!-- 6. BACK COVER (غلاف الخاتمة والتوصيات)                   -->
<!-- ======================================================== -->
<div class="slide-page" id="page-back">
    <div class="cover-page-container">
        <div class="book-leather-cover">
            <div class="book-ornate-border back-cover-border">
                <!-- 4 Corner Arabesques -->
                <svg class="cover-corner-ornament top-right" viewBox="0 0 96 96">
                    <path d="M4,4 L88,4 Q88,24 74,38 Q60,52 38,74 Q24,88 4,88 Z" fill="rgba(212, 175, 55, 0.2)" stroke="#d4af37" stroke-width="1.6" />
                </svg>
                <svg class="cover-corner-ornament top-left" viewBox="0 0 96 96">
                    <path d="M4,4 L88,4 Q88,24 74,38 Q60,52 38,74 Q24,88 4,88 Z" fill="rgba(212, 175, 55, 0.2)" stroke="#d4af37" stroke-width="1.6" />
                </svg>
                <svg class="cover-corner-ornament bottom-right" viewBox="0 0 96 96">
                    <path d="M4,4 L88,4 Q88,24 74,38 Q60,52 38,74 Q24,88 4,88 Z" fill="rgba(212, 175, 55, 0.2)" stroke="#d4af37" stroke-width="1.6" />
                </svg>
                <svg class="cover-corner-ornament bottom-left" viewBox="0 0 96 96">
                    <path d="M4,4 L88,4 Q88,24 74,38 Q60,52 38,74 Q24,88 4,88 Z" fill="rgba(212, 175, 55, 0.2)" stroke="#d4af37" stroke-width="1.6" />
                </svg>

                <div class="back-cover-center">
                    <div style="font-size: 48px; filter: drop-shadow(0 0 20px #d4af37);">⚖️</div>
                    <h1 class="back-cover-title">تم بحمد الله وتوفيقه</h1>

                    <div class="cover-gold-divider">
                        <span class="divider-diamond">◆</span>
                    </div>

                    <p class="back-cover-sub">
                        خاتمة العرض التقديمي لمبحث إنهاء عقد العمل في قانون الأعمال العراقي
                    </p>

                    <div class="back-cover-author">
                        <span class="back-author-role">إشراف وتوجيه:</span>
                        <span class="back-author-name">الأستاذة م.م. هالة رحمن (Ass.L. Hala Rahman)</span>
                    </div>

                    <div class="summary-cards-container">
                        <div class="summary-card">
                            <span class="summary-check">✓</span>
                            <span class="summary-text">استيفاء كافة أحكام وضوابط المبحث الثاني من الفصل الخامس في قانون العمل العراقي رقم (37) لسنة 2015.</span>
                        </div>
                        <div class="summary-card">
                            <span class="summary-check">✓</span>
                            <span class="summary-text">توثيق الضمانات الحمائية للعمال وحرية العمل والتوازن التشريعي مع مصلحة استقرار المشروع الاستثماري.</span>
                        </div>
                        <div class="summary-card">
                            <span class="summary-check">✓</span>
                            <span class="summary-text">تحديد المعايير القضائية الصارمة لمنع التعسف وضمان رقابة محكمة العمل في أربيل وبغداد.</span>
                        </div>
                    </div>

                    <div style="font-size: 16px; color: var(--gold-bright); font-weight: 700; margin-top: 10px; display: flex; align-items: center; gap: 12px;">
                        <span>جامعة نولج — كلية العلوم الإدارية | قسم التسويق الرقمي</span>
                        <span>•</span>
                        <span>العام الأكاديمي 2025 - 2026</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

</body>
</html>
"""

def compile_pdf(html_path, output_pdf_path):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        candidates = [
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ]
        for c in candidates:
            if os.path.exists(c):
                chrome_path = c
                break

    temp_pdf = os.path.join(BASE_DIR, "_temp_compile_presentation.pdf")
    if os.path.exists(temp_pdf):
        try:
            os.remove(temp_pdf)
        except Exception:
            pass

    file_url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    print(f"[*] Compiling {os.path.basename(html_path)} -> {os.path.basename(output_pdf_path)}...")

    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--no-margins",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={temp_pdf}",
        file_url
    ]

    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    start_time = time.time()
    last_size = -1
    stable_count = 0
    timeout = 90

    while time.time() - start_time < timeout:
        time.sleep(1.0)
        if os.path.exists(temp_pdf):
            try:
                cur_size = os.path.getsize(temp_pdf)
                if cur_size > 0 and cur_size == last_size:
                    stable_count += 1
                    if stable_count >= 2:
                        break
                else:
                    stable_count = 0
                last_size = cur_size
            except Exception:
                pass
        if proc.poll() is not None and os.path.exists(temp_pdf) and os.path.getsize(temp_pdf) > 0:
            break

    try:
        proc.kill()
    except Exception:
        pass

    if os.path.exists(temp_pdf) and os.path.getsize(temp_pdf) > 1000:
        time.sleep(0.5)
        shutil.copy2(temp_pdf, output_pdf_path)
        try:
            os.remove(temp_pdf)
        except Exception:
            pass
        size_mb = os.path.getsize(output_pdf_path) / (1024 * 1024)
        print(f"[✓] Successfully generated {os.path.basename(output_pdf_path)} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"[!] Compilation failed or output was empty: {output_pdf_path}")
        return False

def main():
    print("=" * 70)
    print("  Generating Landscape 16:9 Presentation Slides PDF (Arabic Only)")
    print("=" * 70)

    html_file = os.path.join(BASE_DIR, "slides_presentation_landscape_ar.html")
    html_content = generate_arabic_landscape_html()

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[✓] Created Arabic Presentation HTML: {html_file}")

    # Copy to public/
    public_html = os.path.join(BASE_DIR, "public", "slides_presentation_landscape_ar.html")
    shutil.copy2(html_file, public_html)

    # Compile PDF
    output_pdf = os.path.join(BASE_DIR, "عرض_سلايدات_قانون_الاعمال.pdf")
    success = compile_pdf(html_file, output_pdf)

    if success:
        public_pdf = os.path.join(BASE_DIR, "public", "عرض_سلايدات_قانون_الاعمال.pdf")
        shutil.copy2(output_pdf, public_pdf)
        print(f"[✓] Copied Presentation PDF to public/ directory.")

    print("\n[✓] Finished Presentation PDF Generation!")

if __name__ == "__main__":
    main()
