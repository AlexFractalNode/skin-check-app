import os

# --- KONFIGURATION ---
OUTPUT_HTML = "index.html"
OUTPUT_MANIFEST = "manifest.json"
APP_NAME = "Skin-Check"

# Link zum Lexikon (Relativ)
LEXIKON_BASE = "lexikon"

# 💰 DEIN GELD-MACHER TAG
AMAZON_TAG = "dein-tag-21" 

# 📧 FEEDBACK ZIEL
FEEDBACK_MAIL = "feedback@skincheck.app"

# Lila/Blau Verlauf für Kosmetik-Look
THEME_COLOR = "#4c1d95" 
BG_gradient = "linear-gradient(135deg, #4c1d95 0%, #1e1b4b 100%)"

# --- 1. MANIFEST ---
manifest_content = f"""
{{
    "name": "{APP_NAME}",
    "short_name": "{APP_NAME}",
    "start_url": "./index.html",
    "display": "standalone",
    "background_color": "{THEME_COLOR}",
    "theme_color": "{THEME_COLOR}",
    "icons": [
        {{
            "src": "https://img.icons8.com/fluency/192/cosmetic-brush.png",
            "sizes": "192x192",
            "type": "image/png"
        }},
        {{
            "src": "https://img.icons8.com/fluency/512/cosmetic-brush.png",
            "sizes": "512x512",
            "type": "image/png"
        }}
    ]
}}
"""

# --- 2. HTML/JS CODE ---
html_content = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>{APP_NAME}</title>
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="{THEME_COLOR}">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <link rel="apple-touch-icon" href="https://img.icons8.com/fluency/192/cosmetic-brush.png">
    <script src="https://unpkg.com/html5-qrcode" type="text/javascript"></script>
    <style>
        :root {{ 
            --bg: #0f172a; --card: #1e293b; --text: #f8fafc; --muted: #94a3b8;
            --primary: #8b5cf6; --accent: #ec4899;
            --safe: #34d399; --danger: #f87171; --gold: #f59e0b;
        }}
        body {{ font-family: -apple-system, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 0; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }}
        
        /* Header */
        header {{ 
            padding: 1rem; text-align: center; 
            background: {BG_gradient}; 
            box-shadow: 0 4px 20px rgba(76, 29, 149, 0.4);
            z-index: 20; padding-top: max(1rem, env(safe-area-inset-top));
        }}
        header h1 {{ margin: 0; font-size: 1.2rem; letter-spacing: 1px; font-weight: 800; }}

        /* Scanner Bereich */
        #scanner-wrapper {{ 
            flex: 1; position: relative; background: #000; display: flex; align-items: center; justify-content: center; 
        }}
        
        /* Der eigentliche Kamera-Feed */
        #reader {{ 
            width: 100%; height: 100%; object-fit: cover; z-index: 1; 
        }}
        
        /* Das Overlay (Rahmen) - Muss über dem Reader liegen, aber Klicks durchlassen */
        .scan-overlay {{
            position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            display: flex; align-items: center; justify-content: center;
            pointer-events: none; /* WICHTIG: Klicks gehen durch! */
            z-index: 10;
        }}

        .scan-frame {{ 
            width: 70%; aspect-ratio: 1; border: 2px solid rgba(255,255,255,0.2); border-radius: 20px;
            box-shadow: 0 0 0 4000px rgba(0,0,0,0.7); position: relative;
        }}
        .scan-frame::after {{
            content: ''; position: absolute; inset: -3px; border: 3px solid var(--accent); border-radius: 20px;
            animation: pulse 2s infinite; clip-path: polygon(0% 0%, 100% 0%, 100% 20%, 0% 20%);
        }}
        @keyframes pulse {{ 0% {{ top:0; opacity:0; }} 50% {{ opacity:1; }} 100% {{ top:100%; opacity:0; }} }}
        
        /* Result Sheet */
        #result-sheet {{ 
            position: absolute; bottom: 0; left: 0; right: 0; 
            background: var(--card); border-radius: 25px 25px 0 0; 
            padding: 1.5rem; transform: translateY(110%); transition: 0.3s cubic-bezier(0.19, 1, 0.22, 1); 
            box-shadow: 0 -10px
