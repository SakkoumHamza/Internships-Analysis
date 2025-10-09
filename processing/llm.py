import requests
import json
import os

url = "http://localhost:5000/predict"

# Define the prompt template
template = """
Tu es un assistant qui analyse des annonces d'emploi ou de stage.
Voici une annonce brute :

{annonce}

Analyse-la et renvoie un JSON avec les champs suivants :

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

Réponds uniquement avec du JSON valide, sans texte ou formatage additionnel.
"""

def structure_offer(raw_offer: dict) -> dict:
    raw_text = raw_offer.get("raw_text", "")
    if not raw_text:
        return {"error": "Input dictionary does not contain a 'raw_text' field or it is empty."}

    # Fill the template with the annonce
    prompt_text = template.replace("{annonce}", raw_text[:2000])  # truncate if needed

    try:
        print(f"➡️ Sending request to local FLAN-T5 for: '{raw_text[:70]}...'")
        response = requests.post(url, json={"text": prompt_text})

        if response.status_code != 200:
            raise Exception(f"Request failed with status {response.status_code}: {response.text}")

        result_text = response.json().get("result", "")
        cleaned_result = result_text.strip().replace("```json", "").replace("```", "").strip()

        structured_data = json.loads(cleaned_result)
        print("✅ Successfully parsed JSON from the response!")
        return structured_data

    except json.JSONDecodeError:
        print(f"❌ JSON DECODE ERROR: The model's response was not valid JSON.")
        return {"error": "LLM response was not valid JSON.", "raw_response": result_text, "original_text": raw_text}
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        return {"error": str(e), "original_text": raw_text}