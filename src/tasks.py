# =============================================================================
# tasks.py — Définition des tâches assignées aux agents
# =============================================================================
# Une "Task" dans CrewAI est une mission concrète donnée à un agent.
# Elle contient :
#   - description    : l'instruction précise (le "prompt" de la tâche)
#   - expected_output: ce qu'on attend comme résultat (guide le LLM)
#   - agent          : l'agent responsable de cette tâche
#   - context        : liste des tâches précédentes dont le résultat
#                      sera transmis en contexte à cet agent
#
# Les tâches sont exécutées dans l'ordre défini dans la Crew (tasks.py → main.py).
# =============================================================================

from crewai import Task
from src.agents import chercheur, analyste, redacteur


# -----------------------------------------------------------------------------
# Tâche 1 : Recherche d'informations
# -----------------------------------------------------------------------------
# Assignée au Chercheur. Il utilisera WikipediaTool pour collecter les données.
# Le résultat sera transmis en contexte aux tâches suivantes.
# -----------------------------------------------------------------------------
tache_recherche = Task(
    description=(
        "Recherche des informations complètes sur l'entreprise '{entreprise}' via Wikipedia. "
        "Extrait les éléments suivants : "
        "- Secteur d'activité principal "
        "- Date et lieu de création "
        "- Produits et services principaux "
        "- Chiffres clés (CA, effectifs, présence géographique) "
        "- URL de la page Wikipedia"
    ),
    expected_output=(
        "Un rapport structuré en sections claires avec : secteur, date de création, "
        "produits/services, chiffres clés et URL Wikipedia."
    ),
    agent=chercheur,
    # Pas de context ici — c'est la première tâche de la chaîne
)


# -----------------------------------------------------------------------------
# Tâche 2 : Analyse commerciale
# -----------------------------------------------------------------------------
# Assignée à l'Analyste. Il reçoit le rapport du Chercheur via context=[].
# Son rôle est de transformer les faits bruts en opportunités commerciales.
# -----------------------------------------------------------------------------
tache_analyse = Task(
    description=(
        "À partir du rapport collecté sur '{entreprise}', analyse les informations "
        "et produis une analyse commerciale structurée en 3 parties : "
        "1. Les besoins potentiels de l'entreprise (technologiques, humains, organisationnels) "
        "2. Les opportunités commerciales identifiées (minimum 3) "
        "3. L'angle d'approche recommandé pour la prospection de '{entreprise}' (en lien avec les besoins et opportunités)"
    ),
    expected_output=(
        "Une analyse commerciale avec 3 opportunités clairement identifiées "
        "et un angle d'approche argumenté."
    ),
    agent=analyste,
    context=[tache_recherche]  # il vas recevoir automatiquement le resultat  du chercheur
)


# -----------------------------------------------------------------------------
# Tâche 3 : Rédaction de l'email
# -----------------------------------------------------------------------------
# Assignée au Rédacteur. Il reçoit les résultats des DEUX tâches précédentes.
# C'est l'output final du pipeline — l'email prêt à être envoyé.
# -----------------------------------------------------------------------------
tache_redaction = Task(
    description=(
        "Rédige un email de prospection commerciale B2B pour '{entreprise}' "
        "en t'appuyant sur le rapport de recherche et l'analyse commerciale fournis. "
        "L'email doit respecter cette structure : "
        "- Objet : accrocheur et personnalisé (max 60 caractères) "
        "- Introduction : montre que tu connais l'entreprise (2-3 phrases) "
        "- Corps : présente la valeur ajoutée de ta solution par rapport aux besoins identifiés "
        "- Call-to-action : proposition concrète (appel, démo, rendez-vous) "
        "- Signature : professionnelle"
    ),
    expected_output=(
        "Un email complet et prêt à envoyer avec : Objet, Introduction personnalisée, "
        "Corps orienté valeur, Call-to-action précis et Signature."
    ),
    agent=redacteur,
    context=[tache_recherche, tache_analyse]  # Reçoit les résultats des 2 agents précédents
)
