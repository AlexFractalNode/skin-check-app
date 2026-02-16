import json
import os
import shutil
import re
from datetime import datetime

# --- KONFIGURATION ---
OUTPUT_DIR = 'blog'
DATA_FILE = 'app_database.json'
APP_URL = "../index.html" # Link zur App
AMAZON_TAG = "dein-tag-21"

# Lila Theme (identisch zur App)
CSS = """
<style>
    :root { --bg: #f8fafc; --text: #0f172a; --primary: #7c3aed; --accent: #db2777; --card: #ffffff; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; margin: 0; padding-bottom: 80px; }
    
    /* Nav */
    nav { background: white; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 10; display: flex; justify-content: space-between; align-items: center; }
    .logo { font-weight: 800; color: var(--primary); text-decoration: none; font-size: 1.2rem; }
    .btn-app { background: var(--primary); color: white; padding: 8px 16px; border-radius: 99px; text-decoration: none; font-weight: bold; font-size: 0.9rem; transition: transform 0.2s; }
    .btn-app:hover { transform: scale(1.05); }
    
    /* Layout */
    .container { max-width: 700px; margin: 0 auto; padding: 2rem 1rem; }
    .article-header { text-align: center; margin-bottom: 3rem; }
    h1 { font-size: 2.5rem; color: #1e1b4b; line-height: 1.2; margin-bottom: 1rem; }
    .meta { color: #64748b; font-size: 0.9rem; }
    
    .content { font-size: 1.1rem; color: #334155; }
    h2 { color: var(--primary); margin-top: 2.5rem; font-size: 1.8rem; }
    
    /* Ingredient Cards within Text */
    .ing-card { background: white; border-left: 4px solid var(--accent); padding: 1.5rem; margin: 2rem 0; border-radius: 0 12px 12px 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
    .ing-title { font-weight: bold; font-size: 1.2rem; display: block; margin-bottom: 0.5rem; color: #1e1b4b; }
    
    /* Call to Action Box */
    .cta-box { background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%); color: white; padding: 2.5rem; border-radius: 16px; text-align: center; margin: 4rem 0; }
    .cta-btn { display: inline-block; background: white; color: var(--primary); padding: 14px 28px; border-radius: 99px; font-weight: 800; text-decoration: none; margin-top: 1.5rem; transition: transform 0.2s; }
    
    /* Blog Index Grid */
    .blog-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-top: 2rem; }
    .blog-card { background: white; border-radius: 16px; padding: 2rem; text-decoration: none; color: inherit; border: 1px solid #e2e8f0; transition: transform 0.2s; }
    .blog-card:hover { transform: translateY(-5px); border-color: var(--primary); }
    .tag { display: inline-block; background: #f3e8ff; color: var(--primary); padding: 4px 10px; border-radius: 99px; font-size: 0.8rem; font-weight: bold; margin-bottom: 1rem; }
</style>
"""

# --- THEMEN-DEFINITIONEN ---
# Hier definieren wir, worüber der Bot schreiben soll und welche Stoffe dazu gehören.
TOPICS = [
    {
        "slug": "die-dirty-dozen-kosmetik",
        "title": "Die 'Dirty Dozen': 5 Inhaltsstoffe, die du sofort meiden solltest",
        "desc": "Parabene, Formaldehyd und Co. Diese Stoffe haben in deiner Hautpflege nichts verloren.",
        "tag": "Gesundheit",
        "filter_keywords": ["PARABEN", "TRICLOSAN", "FORMALDEHYDE", "BHT", "METHYLISOTHIAZOLINONE"],
        "intro": "Deine Haut ist dein größtes Organ. Alles, was du darauf schmierst, landet in deinem Körper. Wir zeigen dir die gefährlichsten Stoffe, die immer noch in Drogerie-Produkten lauern.",
        "outro": "Geh auf Nummer sicher. Scanne deine Produkte im Bad jetzt sofort."
    },
    {
        "slug": "mikroplastik-in-cremes",
        "title": "Plastik im Gesicht? Warum Acrylates und Co. gefährlich sind",
        "desc": "Mikroplastik versteckt sich oft hinter komplizierten Namen. Wir decken auf.",
        "tag": "Umwelt",
        "filter_keywords": ["ACRYLATES", "CARBOMER", "NYLON", "POLYETHYLENE", "DIMETHICONE"],
        "intro": "Es klingt absurd, ist aber Realität: Viele Cremes bestehen zu einem großen Teil aus flüssigem Plastik. Das verstopft nicht nur deine Poren, sondern landet am Ende im Meer.",
        "outro": "Willst du wissen, ob deine Tagescreme Plastik enthält? Der Scanner verrät es dir in einer Sekunde."
    },
    {
        "slug": "anti-aging-wirkstoffe",
        "title": "Anti-Aging Guide: Was wirklich gegen Falten hilft",
        "desc": "Vergiss teures Marketing. Diese Inhaltsstoffe sind wissenschaftlich belegt.",
        "tag": "Beauty-Tipps",
        "filter_keywords": ["RETINOL", "HYALURON", "NIACINAMIDE", "CERAMIDE", "TOCOPHEROL"],
        "intro": "Die Kosmetikindustrie verspricht viel. Doch welche Stoffe wirken wirklich? Wir haben die Datenbank nach den 'Skin Heroes' durchsucht.",
        "outro": "Finde heraus, ob deine teure Creme diese Wirkstoffe wirklich enthält – oder nur billige Füllstoffe."
    }
]

def build():
    if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # Datenbank laden
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        db = json.load(f)

    print(f"✍️ Blog-Bot startet... Datenbank mit {len(db)} Stoffen geladen.")

    # 1. ARTIKEL GENERIEREN
    for topic in TOPICS:
        # Finde passende Inhaltsstoffe für diesen Artikel
        matches = []
        for code, info in db.items():
            # Prüfen ob eines der Filter-Keywords im Namen oder Code vorkommt
            for kw in topic['filter_keywords']:
                if kw in code or kw in info['n'].upper():
                    matches.append(info)
                    break
        
        # Generiere HTML Liste der Stoffe
        ingredients_html = ""
        for m in matches[:5]: # Top 5 Matches
            rating_emoji = "✅" if "Unbedenklich" in m['r'] or "Gut" in m['r'] or "Exzellent" in m['r'] else "⚠️"
            ingredients_html += f"""
            <div class="ing-card">
                <span class="ing-title">{rating_emoji} {m['n']}</span>
                <p>{m['d']}</p>
                <small style="color:#64748b; font-family:monospace;">INCI: {m['n'].upper()}</small>
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{topic['title']} | Skin-Check Blog</title>
            <meta name="description" content="{topic['desc']}">
            {CSS}
        </head>
        <body>
            <nav>
                <a href="../index.html" class="logo">🧬 Skin-Check Blog</a>
                <a href="{APP_URL}" class="btn-app">📷 Zur App</a>
            </nav>
            
            <div class="container">
                <div class="article-header">
                    <span class="tag">{topic['tag']}</span>
                    <h1>{topic['title']}</h1>
                    <div class="meta">Von Skin-Check Redaktion • Lesezeit: 3 Min.</div>
                </div>
                
                <div class="content">
                    <p><strong>{topic['intro']}</strong></p>
                    
                    <h2>Diese Stoffe solltest du kennen:</h2>
                    {ingredients_html}
                    
                    <h2>Unser Fazit</h2>
                    <p>{topic['outro']} Vertraue nicht blind der Werbung. Ein Blick auf die INCI-Liste (die Rückseite der Verpackung) verrät die Wahrheit.</p>
                </div>

                <div class="cta-box">
                    <h2>Checke jetzt dein Badezimmer 🛁</h2>
                    <p>Funktioniert mit jeder Creme, Shampoo oder Deo.</p>
                    <a href="{APP_URL}" class="cta-btn">📲 Jetzt Barcode scannen</a>
                </div>
                
                <div style="text-align:center; margin-top:3rem;">
                    <a href="index.html" style="color:var(--primary); font-weight:bold;">← Alle Artikel ansehen</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(os.path.join(OUTPUT_DIR, f"{topic['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(html)

    # 2. BLOG INDEX (Startseite) GENERIEREN
    cards_html = ""
    for topic in TOPICS:
        cards_html += f"""
        <a href="{topic['slug']}.html" class="blog-card">
            <span class="tag">{topic['tag']}</span>
            <h3 style="margin-top:0.5rem; color:#1e1b4b;">{topic['title']}</h3>
            <p style="color:#64748b;">{topic['desc']}</p>
            <span style="color:var(--primary); font-weight:bold; font-size:0.9rem;">Artikel lesen →</span>
        </a>
        """

    index_html = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Skin-Check Magazin - Alles über Inhaltsstoffe</title>
        {CSS}
    </head>
    <body>
        <nav>
            <a href="#" class="logo">🧬 Skin-Check Magazin</a>
            <a href="{APP_URL}" class="btn-app">📷 App öffnen</a>
        </nav>
        
        <div class="container" style="max-width:900px;">
            <div style="text-align:center; padding: 3rem 0;">
                <h1 style="font-size:3rem;">Wissen ist Hautschutz 🛡️</h1>
                <p style="font-size:1.2rem; color:#475569;">Die neuesten Erkenntnisse zu Inhaltsstoffen, verständlich erklärt.</p>
            </div>
            
            <div class="blog-grid">
                {cards_html}
            </div>
        </div>
        
        <footer style="text-align:center; padding:3rem; color:#94a3b8;">
            &copy; {datetime.now().year} Skin-Check
        </footer>
    </body>
    </html>
    """
    
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    
    print("✅ Blog erfolgreich generiert!")

if __name__ == "__main__":
    build()
