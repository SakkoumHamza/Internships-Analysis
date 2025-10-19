import json
import re
import ollama 


PROMPT_TEMPLATE = """
Tu es un expert en recrutement qui analyse des annonces d'emploi pour les structurer en JSON.

Analyse l'annonce brute suivante et remplis les champs du format JSON demandé.
Si une information n'est pas explicite, utilise ton raisonnement pour la DÉDUIRE du contexte. Ne laisse pas de champs `null` si tu peux faire une inférence logique.

Règles de déduction :

- "titre": Le titre principal de l'offre.
- "entreprise": Le nom de l'entreprise qui recrute. Si non spécifié, cherche des indices comme 'chez', 'pour le compte de'.
- "domaine": Déduis le domaine principal (ex: "Gestion/Administration", "Communication", "IT", "Rédaction") à partir des missions.
- "missions": Liste les tâches principales décrites. Si une liste n'est pas claire, résume les responsabilités en quelques points.
- "niveau_exigé": Déduis le niveau d'études (ex: "Bac+2/BUT/BTS", "Licence/Bac+3", "Toute formation") ou le niveau d'expérience demandé.
- "compétences": Liste les compétences techniques (logiciels, langages) et les qualités humaines (soft skills) mentionnées.
- "lieu": Indique la ville et si des informations sur les transports ou le télétravail sont mentionnées.
- "durée": Précise la durée en mois ou en semaines. Si non spécifié, indique "À étudier".
- "rémunération": Si non spécifié, indique "À étudier" ou "Non spécifié". Si un montant est donné, indique-le.
- "pré-embauche": Mets `True` uniquement si les mots "pré-embauche", "CDI à la clé" ou similaire sont présents, sinon `False`.
- "url": {url}
- "date_pub":{date_pub}

Annonce brute :
---
{annonce}
---

Ta réponse doit être UNIQUEMENT l'objet JSON, sans aucun texte, commentaire ou ```json avant ou après.
"""

def structure_offer(raw_offer: dict):
    """
    Analyse le texte brut d'une offre d'emploi en utilisant un modèle Ollama local
    et le structure en un dictionnaire JSON.
    """
    # Nettoyage initial du texte brut
    raw_text = raw_offer.get("raw_text", "") 
    url = raw_offer.get("url", "")
    date_pub =  raw_offer.get("date_pub", "").strip()
    if not raw_text:
        print("⚠️ Offre ignorée car le texte est vide.")
        return None

    raw_text = re.sub(r"[\n\t]+", " ", raw_text) # Remplace les sauts de ligne et tabulations par un espace
    raw_text = re.sub(r"\s{2,}", " ", raw_text).strip() # Remplace les espaces multiples par un seul
    # Préparation du prompt final
    prompt = PROMPT_TEMPLATE.format(url=url,date_pub=date_pub,annonce=raw_text)

    try:
        print(f"➡️ Envoi de la requête à Ollama pour : '{raw_text[:70]}...'")
        
        # --- APPEL AU MODÈLE OLLAMA LOCAL ---
        response = ollama.chat(
            model='llama3.2', # Utilise le nom du modèle que tu as sur Ollama
            messages=[{'role': 'user', 'content': prompt}],
            format='json'  # Forcer une sortie JSON !
        )

        
        data_str = response['message']['content']
        data = json.loads(data_str)

        
        fields = ["titre", "entreprise", "domaine", "missions", "niveau_exigé",
                  "compétences", "lieu", "durée", "rémunération", "pré-embauche",
                  "date_pub", "url"]
        
        parsed_data = {k: data.get(k) for k in fields}
        print("✅ Données structurées reçues d'Ollama.")
        return parsed_data

    except json.JSONDecodeError as e:
        print(f"❌ ERREUR: Ollama a renvoyé un JSON invalide. Erreur: {e}")
        print(f"Réponse reçue: {data_str}")
        return None
    except Exception as e:
        print(f"❌ ERREUR INATTENDUE: {e}")
        return None


def main():
    """
    Fonction principale pour lire les offres brutes, les structurer et les sauvegarder.
    """
    raw_path = "../data/raw/stages.json"
    structured_path = "../data/structured/stages_structured.jl"

    print(f"Lecture depuis : {raw_path}")
    print(f"Écriture dans : {structured_path}")

    try:
        with open(raw_path, "r", encoding="utf-8") as f_raw:
            raw_offres = json.load(f_raw)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"❌ Impossible de lire le fichier source : {e}")
        return 

    with open(structured_path, "a", encoding="utf-8") as f_structured:
        for i, raw_offre in enumerate(raw_offres):
            print(f"\n--- Traitement de l'offre {i+1}/{len(raw_offres)} ---")
            # Assure-toi que chaque 'raw_offre' est bien un dictionnaire
            if isinstance(raw_offre, dict):
                structured_data = structure_offer(raw_offre)
                if structured_data:
                    # Écrit le JSON structuré sur une nouvelle ligne (format JSON Lines)
                    f_structured.write(json.dumps(structured_data, ensure_ascii=False) + "\n")
            else:
                print(f"⚠️ Élément ignoré car ce n'est pas un objet valide : {raw_offre}")


    print(f"\n✅ Traitement terminé. Les offres structurées sont dans {structured_path}")


if __name__ == "__main__":
    main()
