# =============================================================================
# agents.py — Définition des agents du système multi-agents
# =============================================================================
# Un "Agent" dans CrewAI est une entité autonome avec :
#   - un rôle  : ce qu'il est (ex: chercheur, analyste)
#   - un goal  : ce qu'il cherche à accomplir
#   - un backstory : son contexte/expertise (influence le comportement du LLM)
#   - un llm   : le modèle de langage qu'il utilise pour raisonner
#   - des tools : les capacités externes qu'il peut utiliser
# =============================================================================

from crewai import Agent, LLM
from src.tools import WikipediaTool
from dotenv import load_dotenv
import os
load_dotenv()  # Charge les variables d'environnement depuis le fichier .env

# Récupération des variables d'environnement pour la configuration du LLM
model = os.getenv("OLLAMA_MODEL")
base_url = os.getenv("OLLAMA_BASE_URL")

# -----------------------------------------------------------------------------
# Configuration du LLM (Large Language Model)
# -----------------------------------------------------------------------------
# On utilise Mistral via Ollama en local — aucune clé API requise, 100% gratuit.
# LiteLLM (installé via crewai[litellm]) permet de connecter n'importe quel LLM
# à CrewAI, y compris les modèles locaux Ollama.
# -----------------------------------------------------------------------------
llm = LLM(
    model=model,       
    base_url= base_url
)

# Instanciation de l'outil Wikipedia (partagé avec l'agent Chercheur)
wiki_tool = WikipediaTool()


# -----------------------------------------------------------------------------
# Agent 1 : Chercheur
# -----------------------------------------------------------------------------
# Rôle : collecter des informations brutes sur l'entreprise cible.
# Il est équipé de WikipediaTool pour faire des recherches réelles.
# C'est le premier maillon de la chaîne.
# -----------------------------------------------------------------------------
chercheur = Agent(
    role="Chercheur en informations entreprises",
    goal="Collecter des informations fiables et complètes sur une entreprise",
    backstory=(
        "Tu es un expert en veille informationnelle. "
        "Tu utilises Wikipedia pour collecter des données précises sur les entreprises : "
        "leur secteur, leur histoire, leurs produits et leurs chiffres clés."
    ),
    tools=[wiki_tool],  # Seul agent avec accès à Wikipedia
    llm=llm,
    verbose=True,
    max_iter=3, # Limite le nombre d'itérations pour éviter les boucles infinies (optionnel)
)
  


# -----------------------------------------------------------------------------
# Agent 2 : Analyste
# -----------------------------------------------------------------------------
# Rôle : interpréter les informations collectées par le Chercheur.
# Il n'a pas d'outil externe — il raisonne uniquement à partir
# du contexte transmis par l'agent précédent.
# -----------------------------------------------------------------------------
analyste = Agent(
    role="Analyste commercial",
    goal="Analyser les informations collectées et identifier les opportunités commerciales",
    backstory=(
        "Tu es un analyste B2B expérimenté. À partir des informations sur une entreprise, "
        "tu identifies ses besoins potentiels, ses axes de croissance "
        "et les angles d'approche commerciale les plus pertinents."
    ),
    llm=llm,
    verbose=True,
)


# -----------------------------------------------------------------------------
# Agent 3 : Rédacteur
# -----------------------------------------------------------------------------
# Rôle : produire l'output final — un email de prospection personnalisé.
# Il reçoit le contexte du Chercheur ET de l'Analyste pour rédiger
# un email ciblé et percutant.
# -----------------------------------------------------------------------------
redacteur = Agent(
    role="Rédacteur commercial senior",
    goal="Rédiger un email de prospection personnalisé, professionnel et convaincant",
    backstory=(
        "Tu es expert en copywriting B2B. Tu rédiges des emails de prospection "
        "percutants en t'appuyant sur les informations spécifiques à chaque entreprise. "
        "Ton style est direct, professionnel et orienté résultats."
    ),
    llm=llm,
    verbose=True,
     langage="fr" 
)
