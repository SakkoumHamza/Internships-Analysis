import requests
import json
import os
import re 
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words"
)
print(response.text)


# Define the prompt template
template = """
Tu es un assistant qui analyse des annonces d'emploi ou de stage.
Voici une annonce brute :

{annonce}

Analyse-la et renvoie **uniquement du JSON valide** avec les champs suivants :
- titre
- entreprise
- domaine
- missions
- niveau_exigé
- compétences
- lieu
- durée
- rémunération
- pré-embauche (True/False)
- date_pub
- lien

Réponds uniquement avec du JSON valide. Ne mets aucun texte ou commentaire.
Si un champ est absent, mets-le à null.
"""


def structure_offer(raw_offer: dict) -> dict:
    raw_text = raw_offer.get("raw_text", "")
    raw_text = re.sub(r"\s+", " ", raw_text.replace("\t", " ").replace("\n", " ")).strip() # Text cleaning
    prompt = template.format(annonce=raw_text)

    try:
        print(f"➡️ Sending request to Gemini for: '{raw_text[:70]}...'")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        data = json.loads(response.text)  # parse Gemini output

        # Ensure all fields exist
        fields = ["titre", "entreprise", "domaine", "missions", "niveau_exigé",
                  "compétences", "lieu", "durée", "rémunération", "pré-embauche",
                  "date_pub", "lien"]
        parsed = {k: data.get(k, None) for k in fields}
        print("✅ Data received")
        return parsed

    except json.JSONDecodeError:
        print("❌ Gemini returned invalid JSON")
        return None
    except Exception as e:
        print("❌ UNEXPECTED ERROR:", e)
        return None
