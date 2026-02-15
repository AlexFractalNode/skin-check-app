import json

# --- STARTER DATENBANK FÜR KOSMETIK (INCI) ---
inci_data = [
    # 🔴 Bedenklich / Vermeiden
    {"code": "PARABEN", "name": "Parabene", "rating": "Bedenklich", "desc": "Konservierungsstoff. Steht im Verdacht, hormonell wirksam zu sein.", "vegan": True},
    {"code": "DIMETHICONE", "name": "Dimethicone (Silikon)", "rating": "Vorsicht", "desc": "Silikonöl. Bildet einen Film auf der Haut, schwer abbaubar.", "vegan": True},
    {"code": "PETROLATUM", "name": "Vaseline (Erdöl)", "rating": "Vorsicht", "desc": "Basiert auf Erdöl. Kann Poren verstopfen.", "vegan": True},
    {"code": "PARAFFINUM LIQUIDUM", "name": "Paraffinöl", "rating": "Bedenklich", "desc": "Erdölprodukt. Kann die Hautatmung behindern.", "vegan": True},
    {"code": "SODIUM LAURYL SULFATE", "name": "SLS (Tensid)", "rating": "Bedenklich", "desc": "Aggressives Waschmittel. Kann die Haut austrocknen und irritieren.", "vegan": True},
    {"code": "ALUMINUM CHLOROHYDRATE", "name": "Aluminiumsalze", "rating": "Bedenklich", "desc": "Verschließt Schweißporen. Nervenschädigend bei hoher Dosis.", "vegan": True},
    {"code": "TRICLOSAN", "name": "Triclosan", "rating": "Gefährlich", "desc": "Antibakteriell. Kann Resistenzen fördern und die Umwelt belasten.", "vegan": True},
    {"code": "MICROCRISTALLINA CERA", "name": "Mikrowachs", "rating": "Bedenklich", "desc": "Mineralölbasis / Mikroplastik-Verdacht.", "vegan": True},
    
    # 🟢 Gut / Unbedenklich
    {"code": "AQUA", "name": "Wasser", "rating": "Unbedenklich", "desc": "Basis der meisten Cremes.", "vegan": True},
    {"code": "GLYCERIN", "name": "Glycerin", "rating": "Unbedenklich", "desc": "Feuchtigkeitsspender (meist pflanzlich).", "vegan": True},
    {"code": "ALOE BARBADENSIS LEAF JUICE", "name": "Aloe Vera", "rating": "Exzellent", "desc": "Beruhigt die Haut und spendet Feuchtigkeit.", "vegan": True},
    {"code": "BUTYROSPERMUM PARKII BUTTER", "name": "Sheabutter", "rating": "Exzellent", "desc": "Hochwertiges Fett, pflegt intensiv.", "vegan": True},
    {"code": "SIMMONDSIA CHINENSIS SEED OIL", "name": "Jojobaöl", "rating": "Exzellent", "desc": "Hautähnliches Wachs, zieht gut ein.", "vegan": True},
    {"code": "TOCOPHEROL", "name": "Vitamin E", "rating": "Gut", "desc": "Antioxidans, schützt die Haut und das Produkt.", "vegan": True},
    {"code": "PANTHENOL", "name": "Panthenol", "rating": "Gut", "desc": "Provitamin B5. Wirkt wundheilend und beruhigend.", "vegan": False}, # Kann tierisch sein
    {"code": "CETEARYL ALCOHOL", "name": "Fettalkohol", "rating": "Unbedenklich", "desc": "Emulgator, macht die Haut weich (kein 'böser' Alkohol).", "vegan": True},
]

# Konvertiere in Dictionary Format für schnellen Zugriff
db = {}
for item in inci_data:
    # Key ist der INCI Name (Uppercase)
    db[item["code"]] = {
        "n": item["name"],
        "r": item["rating"],
        "d": item["desc"],
        "v": item["vegan"]
    }

print("💄 Generiere Skin-Check Datenbank...")
with open('app_database.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False)
print(f"✅ Fertig! {len(db)} INCI-Stoffe gespeichert.")
