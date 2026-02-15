import json
import os
import shutil
import re

# --- KONFIGURATION ---
OUTPUT_DIR = 'lexikon'
DATA_FILE = 'app_database.json'
APP_URL = "../index.html" # Link zurück zur App (Root)
AMAZON_TAG = "dein-tag-21" # Dein Partner-Tag

# Design (Lila Theme)
CSS = """
<style>
    :root { --bg: #f8fafc; --text: #0f172a; --primary: #7c3aed; --accent: #db2777; --card: #ffffff; }
    body { font-family: -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; margin: 0; padding-bottom: 80px; }
    
    /* Nav */
    nav { background: white; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 10; display: flex; justify-content: space-between; align-items: center; }
    .logo { font-weight: 800; color: var(--primary); text-decoration: none; font-size: 1.2rem; }
    .btn-app { background: var(--primary); color: white; padding: 8px 16px; border-radius: 99px; text-decoration: none; font-weight: bold; font-size: 0.9rem; }
    
    /* Layout */
    .container { max-width: 800px; margin: 0 auto; padding: 2rem 1rem; }
    .card { background: var(--card); border-radius: 16px; padding: 2rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin-bottom: 2rem; }
    
    h1 { margin-top: 0; font-size: 2rem; color: var(--primary); }
    .badge { display: inline-block; padding: 6px 12px; border-radius: 8px; font-weight: bold; margin-bottom: 1rem; }
    .b-red { background: #fee2e2; color: #991b1b; }
    .b-green { background: #dcfce7; color: #166534; }
    
    /* Affiliate Box */
    .promo-box { background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%); color: white; padding: 2rem; border-radius: 16px; text-align: center; margin-top: 3rem; }
    .promo-btn { display: inline-block; background: white; color: var(--primary); padding: 12px 24px; border-radius: 99px; font-weight: bold; text-decoration: none; margin-top: 1rem; transition: transform 0.2s; }
    .promo-btn:hover { transform: scale(1.05); }

    /* List */
    .index-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1rem; }
    .index-item { display: block; background: white; padding: 1rem; border-radius: 8px; text-decoration: none; color: inherit; border: 1px solid #e2e8f0; }
    .index-item:hover { border-color: var(--primary); }
</style>
"""

def clean_slug(text):
    return re.sub(r'[^a-z0-9]+', '-', str(text).lower()).strip('-')

def build():
    # Ordner vorbereiten
    if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # Daten laden
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        db = json.load(f)

    # 1. DETAIL SEITEN
    for code, info in db.items():
        slug = clean_slug(info['n'])
        filename = f"{slug}.html"
        
        is_bad = "Bedenklich" in info['r'] or "Gefährlich" in info['r'] or "Vorsicht" in info['r']
        badge_class = "b-red" if is_bad else "b-green"
        
        # Affiliate Link generieren
        affiliate_html = ""
        if is_bad:
            search = f"Naturkosmetik Alternative ohne {info['n']}"
            link = f"https://www.amazon.de/s?k={search}&tag={AMAZON_TAG}"
            affiliate_html = f"""
            <div style="margin-top:2rem; padding:1.5rem; background:#fff7ed; border:1px solid #ffedd5; border-radius:12px;">
                <h3 style="margin-top:0; color:#9a3412;">Gesunde Alternative gesucht?</h3>
                <p>Vermeide {info['n']} in deiner Pflege.</p>
                <a href="{link}" target="_blank" style="color:#c2410c; font-weight:bold;">🌿 Bio-Alternativen bei Amazon ansehen →</a>
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ist {info['n']} schädlich? | Skin-Check Lexikon</title>
            <meta name="description" content="Was ist {info['n']} (INCI)? Bewertung: {info['r']}. Erfahre alles über Wirkung und Risiken in Kosmetik.">
            {CSS}
        </head>
        <body>
            <nav>
                <a href="index.html" class="logo">🧬 Skin-Check</a>
                <a href="{APP_URL}" class="btn-app">📷 Scanner App</a>
            </nav>
            
            <div class="container">
                <a href="index.html" style="color:#64748b; text-decoration:none;">← Zurück zur Übersicht</a>
                
                <article class="card" style="margin-top:1rem;">
                    <span class="badge {badge_class}">{info['r']}</span>
                    <h1>{info['n']}</h1>
                    <p style="font-size:1.1rem; color:#334155;"><strong>INCI-Code:</strong> {code}</p>
                    
                    <h2>Was ist das?</h2>
                    <p>{info['d']}</p>
                    
                    <div style="margin-top:2rem;">
                        <strong>Vegan?</strong> {'🌱 Ja' if info['v'] else '🥩 Nein / Unklar'}
                    </div>

                    {affiliate_html}
                </article>

                <div class="promo-box">
                    <h2>Stehst du gerade im Bad?</h2>
                    <p>Überprüfe alle deine Produkte in Sekunden auf Mikroplastik und Schadstoffe.</p>
                    <a href="{APP_URL}" class="promo-btn">📲 Jetzt App öffnen & Scannen</a>
                </div>
            </div>
        </body>
        </html>
        """
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(html)

    # 2. INDEX SEITE (Liste aller Stoffe)
    list_html = ""
    for code, info in db.items():
        slug = clean_slug(info['n'])
        emoji = "⚠️" if ("Bedenklich" in info['r'] or "Gefährlich" in info['r']) else "✅"
        list_html += f'<a href="{slug}.html" class="index-item"><strong>{emoji} {info["n"]}</strong><br><small style="color:#64748b">{code}</small></a>'

    index_html = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>INCI Lexikon - Kosmetik Inhaltsstoffe checken</title>
        {CSS}
    </head>
    <body>
        <nav>
            <a href="#" class="logo">🧬 Skin-Check Lexikon</a>
            <a href="{APP_URL}" class="btn-app">📷 Zur App</a>
        </nav>
        <div class="container">
            <div style="text-align:center; margin-bottom:3rem;">
                <h1>Was schmierst du dir auf die Haut?</h1>
                <p>Die große Datenbank für Inhaltsstoffe (INCI). <br>Von Mikroplastik bis Parabene.</p>
                <a href="{APP_URL}" class="btn-app" style="font-size:1.2rem; padding:12px 24px;">📷 Barcode scannen</a>
            </div>
            
            <h2>Alle Inhaltsstoffe A-Z</h2>
            <div class="index-list">
                {list_html}
            </div>
        </div>
    </body>
    </html>
    """
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    print("📚 Lexikon generiert!")

if __name__ == "__main__":
    build()
