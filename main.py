import os
import json
import logging
from dotenv import load_dotenv
import requests

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Charger la clé API depuis .env
load_dotenv()

api_key = os.getenv('OPENROUTER_API_KEY')
api_url = "https://openrouter.ai/api/v1/messages"

# Templates de prompts pour différents types de contenu
TEMPLATES = {
    "linkedin": {
        "description": "Contenu LinkedIn optimisé pour l'engagement",
        "system_prompt": """Tu es un expert en communication sur LinkedIn.
Transforme cette description en contenu LinkedIn engageant.
Réponds UNIQUEMENT en JSON valide avec ces clés:
- "title": Titre accrocheur (max 100 caractères)
- "hook": Première ligne captivante (max 150 caractères)
- "body": Corps du post, 2-3 paragraphes (max 300 caractères)
- "call_to_action": CTA clair (max 100 caractères)
- "hashtags": 5 hashtags pertinents
Réponds UNIQUEMENT le JSON."""
    },
    "twitter": {
        "description": "Tweet structuré et viralisant",
        "system_prompt": """Tu es un expert Twitter. Crée un tweet structuré.
Réponds en JSON avec:
- "tweet": Tweet principal (max 280 caractères)
- "thread": Liste de 2-3 tweets complémentaires si pertinent
- "hashtags": 3 hashtags pertinents
Réponds UNIQUEMENT le JSON."""
    },
    "product_description": {
        "description": "Description de produit convaincante",
        "system_prompt": """Tu es copywriter spécialisé en descriptions produit.
Crée une description convaincante et structurée.
Réponds en JSON avec:
- "short_desc": Description courte (max 100 caractères)
- "benefits": Liste de 3-5 bénéfices clés
- "use_case": Cas d'usage principal
- "cta": Appel à l'action
Réponds UNIQUEMENT le JSON."""
    },
    "newsletter": {
        "description": "Contenu newsletter structuré et engageant",
        "system_prompt": """Tu es un expert en création de newsletters efficaces.
Transforme cette description en newsletter structurée et professionnelle.
Réponds UNIQUEMENT en JSON valide avec ces clés:
- "subject": Ligne de sujet (max 60 caractères, doit donner envie d'ouvrir)
- "preview": Preview text visible avant d'ouvrir (max 50 caractères)
- "intro": Accroche chaleureuse et personnelle (2-3 lignes)
- "main_content": Contenu principal avec insights (3-4 paragraphes)
- "call_to_action": CTA clair et irrésistible
- "signature": Signature chaleureuse de fermeture
Réponds UNIQUEMENT le JSON."""
    }
}

def generate_content(raw_description: str, template_type: str = "linkedin") -> dict:
    """
    Génère du contenu structuré via API.
    
    Args:
        raw_description: Texte brut à transformer
        template_type: Type de contenu ('linkedin', 'twitter', 'product_description')
    
    Returns:
        dict: Contenu structuré ou erreur
    """
    
    if not api_key:
        logger.error("OPENROUTER_API_KEY non trouvée dans .env")
        return {"error": "API key not configured. Set OPENROUTER_API_KEY in .env"}
    
    if template_type not in TEMPLATES:
        logger.warning(f"Template '{template_type}' inconnu. Utilisation de 'linkedin'")
        template_type = "linkedin"
    
    template = TEMPLATES[template_type]
    logger.info(f"Génération de contenu: type={template_type}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Content Generator",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": f"{template['system_prompt']}\n\nContenu à transformer:\n{raw_description}"
            }
        ]
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()  # Lève une exception pour status != 2xx
        
    except requests.exceptions.Timeout:
        logger.error("Timeout: Requête API trop lente")
        return {"error": "API request timed out"}
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur requête: {str(e)}")
        return {"error": f"API Error: {str(e)}"}
    
    try:
        response_data = response.json()
        response_text = response_data['content'][0]['text']
        
        # Parser le JSON
        content = json.loads(response_text)
        logger.info(f"✅ Contenu généré avec succès ({template_type})")
        return content
        
    except json.JSONDecodeError:
        logger.error("Erreur parsing JSON de la réponse API")
        return {"error": "Invalid JSON response from API", "raw": response_text}


# Backward compatibility
def generate_linkedin_content(raw_description: str) -> dict:
    """Alias pour generate_content avec template LinkedIn."""
    return generate_content(raw_description, template_type="linkedin")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🚀 Générateur de contenu structuré via IA (OpenRouter)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python main.py --text "Mon app génère des rapports automatiques" --type linkedin
  python main.py --type twitter --text "Building in public avec l'IA"
  python main.py --type product_description --text "Tool d'automation des process métier"
  python main.py --type newsletter --text "Les 5 tendances IA de 2026"
        """
    )
    
    parser.add_argument(
        '--text', '-t',
        required=True,
        help='Texte brut à transformer'
    )
    parser.add_argument(
        '--type', '-T',
        default='linkedin',
        choices=['linkedin', 'twitter', 'product_description', 'newsletter'],
        help='Type de contenu à générer (défaut: linkedin)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("🚀 Générateur de contenu structuré")
    print("=" * 70)
    print(f"\n📝 Entrée: {args.text[:80]}...")
    print(f"🎯 Type: {args.type}")
    print("\n⏳ Appel à Claude via OpenRouter...")
    
    result = generate_content(args.text, template_type=args.type)
    
    print("\n" + "-" * 70)
    if "error" not in result:
        print("✅ Résultat:\n")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"❌ Erreur: {result['error']}")
    print("-" * 70 + "\n")


if __name__ == "__main__":
    main()
