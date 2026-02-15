import json
import os
import shutil
import re
from datetime import datetime

# --- KONFIGURATION ---
OUTPUT_DIR = 'lexikon'
DATA_FILE = 'app_database.json'
APP_URL = "../index.html" # Link zurück zur App (Root)
AMAZON_TAG = "dein-tag-21" # Dein Partner-Tag

# Design (Lila Theme passend zur App)
CSS = """
<style>
    :root { --bg: #f8fafc; --text: #0f172a; --primary: #7c3aed; --accent: #db2777; --card: #ffffff; }
    body { font-family: -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; margin: 0; padding-bottom: 80px; }
    
    /* Nav */
    nav { background: white; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 10; display: flex; justify-content: space-between; align-items: center; }
    .logo { font-weight: 800; color: var(--primary); text-decoration: none; font-size: 1.1rem; }
    .btn-app { background: var(--primary); color: white; padding: 8px 16px; border-radius: 99px; text-decoration: none; font-weight: bold; font-size: 0.9rem; transition: transform 0.2s; }
    .btn-app:hover { transform: scale(1.05); }
    
    /* Layout */
    .container { max-width: 800px; margin: 0 auto; padding: 2rem 1rem; }
    .card { background: var(--card); border-radius: 16px; padding: 2rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin-bottom: 2rem; border: 1px solid #e2e8f0; }
    
    h1 { margin-top: 0; font-size: 2rem; color: var(--primary); line-height: 1.2; }
    h2 { font-size: 1.3rem; margin-top: 2rem; }
    
    .badge { display: inline-block; padding: 6px 12px; border-radius: 8px; font-weight: bold; margin-bottom: 1rem; }
    .b-red { background: #fee2e2; color: #991b1b; }
    .b-green { background: #dcfce7; color: #166534; }
    .b-orange { background: #ffedd5; color: #9a3412; }
    
    /* Promo Box (Der Trichter zur App) */
    .promo-box { background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%); color: white; padding: 2.5rem; border-radius: 16px; text-align: center; margin-top: 3rem; box-shadow: 0 10px 25px -5px rgba(124, 58, 237, 0.4); }
    .promo-btn { display: inline-block; background: white; color: var(--primary); padding: 14px 28px; border-radius: 99px; font-weight: 800; text-decoration: none; margin-top: 1.5rem; transition: transform 0.2s; font-size: 1.1rem; }
    .promo-btn:hover { transform: scale(1.05); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }

    /* List */
    .index-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
    .index-item { display: block; background: white; padding: 1.5rem; border-radius: 12px; text-decoration: none; color: inherit; border: 1px solid #e2e8f0; transition: border-color 0.2s; }
    .index-item:hover { border-color: var(--primary); transform: translateY(-2px); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    
    footer { text-align: center; color: #94a3b8; margin-top: 3rem; font-size: 0.9rem; }
</style>
"""

def clean_slug(text):
    # Erstellt saubere URLs (z.B. "Sodium Lauryl Sulfate" -> "sodium-lauryl-sulfate")
    return re.sub(r'[^a-z0-9]+', '-', str(text).lower()).strip('-')

def get_risk_badge(rating):
    r = rating.lower()
    if "bedenklich" in r or "gefährlich" in r: return "b-red"
    if "vorsicht" in r: return "b-orange"
    return "b-green"

def build():
    # 1. Output Ordner 'lexikon' leeren/erstellen
    if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # 2. Datenbank laden
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            db = json.load(f)
    except FileNotFoundError:
        print("❌ app_database.json nicht gefunden! Bitte erst generate_inci.py ausführen.")
        return

    print(f"📚 Generiere Lexikon für {len(db)} Inhaltsstoffe...")

    # 3. DETAILSEITEN GENERIEREN
    for code, info in db.items():
        slug = clean_slug(info['n'])
        filename = f"{slug}.html"
        rating = info['r']
        badge = get_risk_badge(rating)
        
        # Affiliate / Alternative Logik
        affiliate_html = ""
        if badge in ["b-red", "b-orange"]:
            search = f"Naturkosmetik Alternative ohne {info['n']}"
            link = f"https://www.amazon.de/s?k={search}&tag={AMAZON_TAG}"
            affiliate_html = f"""
            <div style="margin-top:2rem; padding:1.5rem; background:#fff7ed; border:1px solid #ffedd5; border-radius:12px;">
                <h3 style="margin-top:0; color:#9a3412; font-size:1.1rem;">⚠️ Gesunde Alternative gesucht?</h3>
                <p style="color:#7c2d12;">Vermeide <strong>{info['n']}</strong> in deiner täglichen Pflege.</p>
                <a href="{link}" target="_blank" style="display:inline-block; margin-top:0.5rem; color:#c2410c; font-weight:bold; text-decoration:none;">🌿 Bio-Alternativen bei Amazon finden →</a>
            </div>
            """

        # HTML Template für Detailseite
        html = f"""
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ist {info['n']} schädlich? | INCI Check</title>
            <meta name="description" content="Was ist {info['n']}? Bewertung: {rating}. Wirkung, Risiken und Alternativen im Kosmetik-Check.">
            {CSS}
        </head>
        <body>
            <nav>
                <a href="index.html" class="logo">🧬 INCI Lexikon</a>
                <a href="{APP_URL}" class="btn-app">📷 Zur App</a>
            </nav>
            
            <div class="container">
                <a href="index.html" style="color:#64748b; text-decoration:none; font-size:0.9rem;">← Zurück zur Übersicht</a>
                
                <article class="card" style="margin-top:1.5rem;">
                    <span class="badge {badge}">{rating}</span>
                    <h1>{info['n']}</h1>
                    <p style="font-family:monospace; color:#64748b; background:#f1f5f9; display:inline-block; padding:2px 6px; border-radius:4px;">INCI: {code}</p>
                    
                    <h2>Was ist das?</h2>
                    <p style="font-size:1.1rem; color:#334155;">{info['d']}</p>
                    
                    <div style="margin-top:2rem; display:flex; gap:20px; flex-wrap:wrap;">
                        <div>
                            <small style="color:#64748b; display:block;">Vegan?</small>
                            <strong>{'🌱 Ja' if info['v'] else '🥩 Nein / Unklar'}</strong>
                        </div>
                        <div>
                            <small style="color:#64748b; display:block;">Bewertung</small>
                            <strong>{rating}</strong>
                        </div>
                    </div>

                    {affiliate_html}
                </article>

                <div class="promo-box">
                    <h2 style="margin-top:0;">Stehst du gerade im Bad? 🛁</h2>
                    <p style="font-size:1.1rem; opacity:0.9;">Überprüfe alle deine Produkte in Sekunden auf Mikroplastik und Schadstoffe.</p>
                    <a href="{APP_URL}" class="promo-btn">📲 Jetzt Barcode scannen</a>
                    <p style="margin-top:1rem; font-size:0.8rem; opacity:0.7;">Kostenlos & ohne Anmeldung</p>
                </div>
            </div>
            
            <footer>
                &copy; {datetime.now().year} Skin-Check • <a href="{APP_URL}" style="color:inherit;">Scanner App</a>
            </footer>
        </body>
        </html>
        """
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(html)

    # 4. INDEX SEITE (Übersicht)
    list_html = ""
    sorted_items = sorted(db.items(), key=lambda x: x[1]['n']) # Alphabetisch sortieren
    
    for code, info in sorted_items:
        slug = clean_slug(info['n'])
        badge = get_risk_badge(info['r'])
        emoji = "⚠️" if badge in ["b-red", "b-orange"] else "✅"
        
        list_html += f"""
        <a href="{slug}.html" class="index-item">
            <div style="display:flex; justify-content:space-between; align-items:start;">
                <strong>{info['n']}</strong>
                <span style="font-size:0.8rem;">{emoji}</span>
            </div>
            <small style="color:#94a3b8; display:block; margin-top:4px;">{code}</small>
        </a>
        """

    index_html = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>INCI Lexikon - Kosmetik Inhaltsstoffe von A-Z</title>
        <meta name="description" content="Große Datenbank für Kosmetik-Inhaltsstoffe. Prüfe Mikroplastik, Parabene und Silikone.">
        {CSS}
    </head>
    <body>
        <nav>
            <a href="#" class="logo">🧬 INCI Lexikon</a>
            <a href="{APP_URL}" class="btn-app">📷 App laden</a>
        </nav>
        
        <div class="container">
            <div style="text-align:center; margin: 2rem 0 4rem 0;">
                <h1 style="font-size:2.5rem; margin-bottom:1rem;">Was schmierst du dir<br>auf die Haut?</h1>
                <p style="font-size:1.2rem; color:#475569; max-width:600px; margin:0 auto;">
                    Die große Datenbank für Inhaltsstoffe. Von Mikroplastik bis Parabene.
                    Wir übersetzen das Kleingedruckte.
                </p>
                <div style="margin-top:2rem;">
                    <a href="{APP_URL}" class="btn-app" style="font-size:1.1rem; padding:16px 32px; box-shadow:0 10px 20px -5px rgba(124, 58, 237, 0.3);">📷 Barcode jetzt scannen</a>
                </div>
            </div>
            
            <h2 style="border-bottom:2px solid #e2e8f0; padding-bottom:10px; margin-bottom:1.5rem;">Alle Inhaltsstoffe A-Z</h2>
            <div class="index-list">
                {list_html}
            </div>
        </div>
        
        <footer>
            &copy; {datetime.now().year} Skin-Check Lexikon
        </footer>
    </body>
    </html>
    """
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    print("✅ Lexikon erfolgreich generiert!")

if __name__ == "__main__":
    build()
