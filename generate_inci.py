import json

# --- DIE GROSSE KOSMETIK-DATENBANK (INCI) 💄 ---
# Kategorien:
# 🔴 BEDENKLICH: Hormonell wirksam, Krebserregend, Umweltbelastend
# 🟠 VORSICHT: Allergiepotenzial, Umstritten, Irritierend
# 🟢 GUT: Pflegend, Unbedenklich, Natürlich

inci_data = [
    # --- 🔴 KONSERVIERUNGSSTOFFE (Die "Dirty Dozen") ---
    {"code": "PROPYLPARABEN", "name": "Propylparaben", "rating": "Gefährlich", "desc": "Konservierungsstoff. Steht im starken Verdacht, hormonell wirksam zu sein.", "vegan": True},
    {"code": "BUTYLPARABEN", "name": "Butylparaben", "rating": "Gefährlich", "desc": "Hormonell wirksam. Sollte unbedingt gemieden werden.", "vegan": True},
    {"code": "METHYLPARABEN", "name": "Methylparaben", "rating": "Bedenklich", "desc": "Konservierungsstoff. Allergiepotenzial und hormoneller Verdacht.", "vegan": True},
    {"code": "TRICLOSAN", "name": "Triclosan", "rating": "Gefährlich", "desc": "Antibakteriell. Fördert Resistenzen, belastet die Leber und Umwelt.", "vegan": True},
    {"code": "METHYLISOTHIAZOLINONE", "name": "Methylisothiazolinone (MI)", "rating": "Gefährlich", "desc": "Starkes Allergen. Wurde in vielen Leave-on Produkten verboten.", "vegan": True},
    {"code": "DMDM HYDANTOIN", "name": "DMDM Hydantoin", "rating": "Gefährlich", "desc": "Formaldehydabspalter. Kann krebserregendes Formaldehyd freisetzen.", "vegan": True},
    {"code": "IMIDAZOLIDINYL UREA", "name": "Imidazolidinyl Urea", "rating": "Bedenklich", "desc": "Formaldehydabspalter. Kann Hautirritationen auslösen.", "vegan": True},
    {"code": "BHT", "name": "BHT (Butylhydroxytoluol)", "rating": "Bedenklich", "desc": "Antioxidans. Steht im Verdacht, das Immunsystem zu beeinträchtigen.", "vegan": True},
    
    # --- 🔴 SILIKONE & MINERALÖLE (Die "Plastiktüte" für die Haut) ---
    {"code": "DIMETHICONE", "name": "Dimethicone", "rating": "Vorsicht", "desc": "Silikonöl. Bildet einen Film, der Poren verstopfen kann. Schwer abbaubar.", "vegan": True},
    {"code": "CYCLOPENTASILOXANE", "name": "Cyclopentasiloxane", "rating": "Bedenklich", "desc": "Silikon. Umweltbelastend und bioakkumulierend.", "vegan": True},
    {"code": "PARAFFINUM LIQUIDUM", "name": "Paraffinöl", "rating": "Bedenklich", "desc": "Erdölprodukt. Kann die Hautatmung behindern und austrocknen.", "vegan": True},
    {"code": "PETROLATUM", "name": "Vaseline", "rating": "Vorsicht", "desc": "Erdölbasis. Dichtet die Haut ab, keine Pflegewirkung.", "vegan": True},
    {"code": "CERA MICROCRISTALLINA", "name": "Mikrowachs", "rating": "Bedenklich", "desc": "Mineralölwachs. Potenziell krebserregende MOAH-Rückstände.", "vegan": True},
    {"code": "MINERAL OIL", "name": "Mineralöl", "rating": "Bedenklich", "desc": "Abfallprodukt der Erdölindustrie.", "vegan": True},

    # --- 🔴 TENSIDE & REINIGUNG (Die "Schaumschläger") ---
    {"code": "SODIUM LAURYL SULFATE", "name": "SLS", "rating": "Bedenklich", "desc": "Aggressives Tensid. Trocknet die Haut stark aus und irritiert.", "vegan": True},
    {"code": "SODIUM LAURETH SULFATE", "name": "SLES", "rating": "Vorsicht", "desc": "Tensid. Weniger aggressiv als SLS, aber macht die Haut durchlässiger.", "vegan": True},
    {"code": "AMMONIUM LAURYL SULFATE", "name": "ALS", "rating": "Vorsicht", "desc": "Kann Hautirritationen hervorrufen.", "vegan": True},

    # --- 🔴 MIKROPLASTIK & POLYMERE (Umweltkiller) ---
    {"code": "ACRYLATES COPOLYMER", "name": "Acrylates Copolymer", "rating": "Bedenklich", "desc": "Flüssiges Mikroplastik / Synthetisches Polymer. Umweltbelastend.", "vegan": True},
    {"code": "CARBOMER", "name": "Carbomer", "rating": "Vorsicht", "desc": "Synthetisches Gel-Mittel. Oft als flüssiges Plastik eingestuft.", "vegan": True},
    {"code": "NYLON-12", "name": "Nylon-12", "rating": "Bedenklich", "desc": "Mikroplastik. Wird oft als Füllstoff verwendet.", "vegan": True},
    {"code": "POLYETHYLENE", "name": "Polyethylene (PE)", "rating": "Gefährlich", "desc": "Mikroplastik-Partikel. Verschmutzen Weltmeere.", "vegan": True},
    
    # --- 🟠 UV-FILTER & STABILISATOREN ---
    {"code": "BENZOPHENONE-3", "name": "Benzophenone-3", "rating": "Bedenklich", "desc": "UV-Filter. Hormonell wirksam und allergieauslösend.", "vegan": True},
    {"code": "OCTOCRYLENE", "name": "Octocrylene", "rating": "Vorsicht", "desc": "UV-Filter. Kann sich zersetzen und Allergien auslösen.", "vegan": True},
    {"code": "HOMOSALATE", "name": "Homosalate", "rating": "Vorsicht", "desc": "UV-Filter. Verdacht auf Hormonwirkung.", "vegan": True},
    {"code": "DISODIUM EDTA", "name": "Disodium EDTA", "rating": "Vorsicht", "desc": "Macht die Zellmembran durchlässiger für Schadstoffe.", "vegan": True},
    {"code": "ALUMINUM CHLOROHYDRATE", "name": "Aluminiumsalze", "rating": "Bedenklich", "desc": "Verschließt Poren. Nervenschädigend bei hoher Aufnahme.", "vegan": True},

    # --- 🟠 DUFTSTOFFE (Allergene) ---
    {"code": "LIMONENE", "name": "Limonene", "rating": "Vorsicht", "desc": "Duftstoff (Zitrus). Deklarationspflichtiges Allergen.", "vegan": True},
    {"code": "LINALOOL", "name": "Linalool", "rating": "Vorsicht", "desc": "Duftstoff (Lavendel). Kann Allergien auslösen.", "vegan": True},
    {"code": "CITRONELLOL", "name": "Citronellol", "rating": "Vorsicht", "desc": "Duftstoff. Potenzielles Allergen.", "vegan": True},
    {"code": "PARFUM", "name": "Parfum / Fragrance", "rating": "Vorsicht", "desc": "Unbekannte Mischung. Häufigste Ursache für Kontaktallergien.", "vegan": True},

    # --- 🟢 SKIN HEROES (Die Guten) ---
    {"code": "AQUA", "name": "Wasser", "rating": "Unbedenklich", "desc": "Feuchtigkeitsbasis.", "vegan": True},
    {"code": "GLYCERIN", "name": "Glycerin", "rating": "Gut", "desc": "Bindet Feuchtigkeit in der Haut.", "vegan": True},
    {"code": "PANTHENOL", "name": "Panthenol (Provitamin B5)", "rating": "Exzellent", "desc": "Wundheilend, beruhigend und feuchtigkeitsspendend.", "vegan": False},
    {"code": "NIACINAMIDE", "name": "Niacinamid (Vitamin B3)", "rating": "Exzellent", "desc": "Verfeinert Poren, stärkt die Hautbarriere, hellt auf.", "vegan": True},
    {"code": "SODIUM HYALURONATE", "name": "Hyaluronsäure", "rating": "Exzellent", "desc": "Speichert massiv Feuchtigkeit, polstert auf.", "vegan": True},
    {"code": "TOCOPHEROL", "name": "Vitamin E", "rating": "Gut", "desc": "Starkes Antioxidans, schützt vor freien Radikalen.", "vegan": True},
    {"code": "ALLANTOIN", "name": "Allantoin", "rating": "Gut", "desc": "Beruhigt gereizte Haut und verfeinert das Hautbild.", "vegan": True},
    {"code": "RETINOL", "name": "Retinol (Vitamin A)", "rating": "Gut", "desc": "Anti-Aging Goldstandard. Fördert Zellerneuerung (Vorsicht bei Sonne).", "vegan": True},
    {"code": "CERAMIDE NP", "name": "Ceramide", "rating": "Exzellent", "desc": "Bausteine der Hautbarriere. Repariert Schutzschicht.", "vegan": True},
    {"code": "UREA", "name": "Urea (Harnstoff)", "rating": "Gut", "desc": "Bindet Feuchtigkeit tief in der Haut.", "vegan": False},
    {"code": "ZINC OXIDE", "name": "Zinkoxid", "rating": "Gut", "desc": "Mineralischer UV-Filter und entzündungshemmend.", "vegan": True},

    # --- 🟢 NATÜRLICHE ÖLE & BUTTER ---
    {"code": "BUTYROSPERMUM PARKII BUTTER", "name": "Sheabutter", "rating": "Exzellent", "desc": "Reichhaltige Pflege, nicht komedogen.", "vegan": True},
    {"code": "SIMMONDSIA CHINENSIS SEED OIL", "name": "Jojobaöl", "rating": "Exzellent", "desc": "Hautähnliches Wachs, reguliert Talgproduktion.", "vegan": True},
    {"code": "PRUNUS AMYGDALUS DULCIS OIL", "name": "Mandelöl", "rating": "Gut", "desc": "Mildes Öl, ideal für empfindliche Haut.", "vegan": True},
    {"code": "ALOE BARBADENSIS LEAF JUICE", "name": "Aloe Vera", "rating": "Exzellent", "desc": "Kühlt, beruhigt und spendet Feuchtigkeit.", "vegan": True},
    {"code": "ARGANIA SPINOSA KERNEL OIL", "name": "Arganöl", "rating": "Exzellent", "desc": "Reich an Vitamin E und Fettsäuren.", "vegan": True},
    {"code": "COCOS NUCIFERA OIL", "name": "Kokosöl", "rating": "Gut", "desc": "Pflegend, kann aber bei manchen Hauttypen Pickel fördern.", "vegan": True},
    {"code": "SQUALANE", "name": "Squalan", "rating": "Exzellent", "desc": "Bewahrt Feuchtigkeit, macht Haut seidig. Meist aus Oliven.", "vegan": True},
    {"code": "CAPRYLIC/CAPRIC TRIGLYCERIDE", "name": "Neutralöl", "rating": "Unbedenklich", "desc": "Basisöl aus Kokos. Verträglich und leicht.", "vegan": True},

    # --- 🟢 EMULGATOREN & ALKOHOLE (Die Guten) ---
    {"code": "CETEARYL ALCOHOL", "name": "Cetearylalkohol", "rating": "Unbedenklich", "desc": "Fettalkohol (nicht austrocknend!). Macht Haut weich.", "vegan": True},
    {"code": "CETYL ALCOHOL", "name": "Cetylalkohol", "rating": "Unbedenklich", "desc": "Co-Emulgator und Weichmacher.", "vegan": True},
    {"code": "STEARIC ACID", "name": "Stearinsäure", "rating": "Unbedenklich", "desc": "Natürlicher Bestandteil von Fetten.", "vegan": True},
    {"code": "XANTHAN GUM", "name": "Xanthan", "rating": "Unbedenklich", "desc": "Natürliches Verdickungsmittel.", "vegan": True},
]

# Konvertierung für die App (Speed-Optimiert)
db = {}
print(f"💄 Verarbeite {len(inci_data)} INCI-Stoffe...")

for item in inci_data:
    # Wir speichern sowohl "DIMETHICONE" als Key
    db[item["code"]] = {
        "n": item["name"],
        "r": item["rating"],
        "d": item["desc"],
        "v": item["vegan"]
    }

# Speichern
with open('app_database.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False) # Minified

print(f"✅ Fertig! Datenbank 'app_database.json' wurde aktualisiert.")
