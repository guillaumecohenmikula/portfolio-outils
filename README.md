# rep-03 : Premier Appel API + Git/GitHub

**Plateforme d'apprentissage pour maîtriser Python, les APIs, et Git en l'utilisant pour de vrai.**

## 🎯 Objectif du rep-03

C'est pas un projet "fini". C'est un **stepping stone** (palier d'apprentissage) où tu vas:

1. ✅ Faire ton **premier appel API réussi** (Python → OpenRouter → Claude)
2. ✅ Structurer et parser des **réponses JSON**
3. ✅ Gérer les **variables d'environnement** (.env) et les secrets
4. ✅ Utiliser **Git et GitHub** pour vrai (pas du drag-and-drop)
5. ✅ Apprendre **Python en le pratiquant** (pas en le théorisant)

## 🛠 Setup

### Prérequis
- Python 3.9+
- Terminal / Shell

### Installation
```bash
# Clone le repo
git clone https://github.com/guillaumecohenmikula-cpu/portfolio-outils.git
cd rep-03-premier-appel-ia

# Crée l'environnement virtuel
python3 -m venv venv

# Activates l'env
source venv/bin/activate  # ou: venv\Scripts\activate sur Windows

# Installe les dépendances
pip install -r requirements.txt
```

### Configuration de l'API
```bash
# Crée un fichier .env
cat > .env << EOF
OPENROUTER_API_KEY=sk-or-v1-votre-cle-api
EOF
```

**Où trouver ta clé OpenRouter?**
1. Va sur https://openrouter.ai/
2. Inscris-toi (gratuit)
3. Crée une clé API dans Settings
4. Colle-la dans `.env`

## 💻 Utilisation

### Utilisation simple (CLI)

```bash
# Générer du contenu LinkedIn
python main.py --text "J'ai créé une app qui automatise les tâches répétitives" --type linkedin

# Générer un tweet
python main.py --text "Building with AI" --type twitter

# Générer une description produit
python main.py --text "Tool d'automation des process métier" --type product_description
```

### Utilisation en Python

```python
from main import generate_content

# Générer du contenu LinkedIn
content = generate_content(
    "Mon app transforme les process métier Excel en apps web",
    template_type="linkedin"
)

print(content)
```
