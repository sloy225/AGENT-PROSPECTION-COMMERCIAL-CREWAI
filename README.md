#  POC Prospection Commerciale — CrewAI

> Système multi-agents IA pour automatiser la prospection commerciale B2B.
> Chaque agent a un rôle précis : collecter, analyser, puis rédiger un email personnalisé.

##  Architecture

(assets/architecture_poc.png)

##  Stack technique
CrewAI : orchestre plusieurs agents pour gérer les tâches de manière coordonnée.

Mistral ou deepseek-r1:1.5b ( mon cas) via Ollama : modèle de langage local, gratuit et 100 % offline.

Wikipedia API : fournit des données sur les entreprises pour enrichir les réponses.

LiteLLM : connecteur universel permettant d’intégrer facilement différents LLM.
##  Structure du projet

```
crewai-prospection-poc/
├── src/
│   ├── agents.py     # Définition des 3 agents
│   ├── tasks.py      # Définition des 3 tâches
│   ├── tools.py      # Outil Wikipedia custom
│   └── main.py       # Point d'entrée
├── assets/
│   └── architecture_poc.png
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

##  Installation

```bash
# 1. Cloner le repo
git clone https://github.com/TON_USERNAME/crewai-prospection-poc.git
cd crewai-prospection-poc

# 2. Créer et activer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Télécharger le modèle LLM local / ça depend de toi 
ollama pull deepseek-r1:1.5b
```

##  Lancement

```bash
python src/main.py
```

##  Résultat attendu

Pour chaque entreprise de la liste, le pipeline génère :
1. **Rapport de recherche** — infos Wikipedia structurées
2. **Analyse commerciale** — 3 opportunités identifiées
3. **Email de prospection** — prêt à envoyer

##  Perspectives d'évolution

- Connecter un CRM (HubSpot, Salesforce) pour automatiser l'envoi
- Remplacer Wikipedia par une source métier (LinkedIn, base interne)
- Ajouter un agent de validation qualité
- Déployer sur Azure avec une interface web (Streamlit ou FastAPI)
