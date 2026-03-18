# =============================================================================
# main.py — Point d'entrée du POC CrewAI Prospection Commerciale
# =============================================================================
# Ce fichier assemble tous les composants (agents + tâches) dans une Crew,
# puis lance le workflow pour chaque entreprise cible.
#
# Flux d'exécution :
#   main.py → Crew.kickoff() → tache_recherche → tache_analyse → tache_redaction
# =============================================================================

from crewai import Crew
from src.agents import chercheur, analyste, redacteur
from src.tasks import tache_recherche, tache_analyse, tache_redaction
from typing import List


# -----------------------------------------------------------------------------
# Assemblage de la Crew
# -----------------------------------------------------------------------------
# La Crew est le chef d'orchestre qui coordonne les agents et les tâches.
# - agents : liste des agents disponibles
# - tasks  : liste des tâches à exécuter dans l'ordre
# - verbose: affiche le raisonnement de chaque agent en temps réel
# -----------------------------------------------------------------------------
crew = Crew(
    agents=[chercheur, analyste, redacteur],
    tasks=[tache_recherche, tache_analyse, tache_redaction],
    verbose=True,
)


def main():
    """
    Fonction principale du POC.
    Lance le pipeline multi-agents pour chaque entreprise de la liste.
    """

    # Liste des entreprises à prospecter — modifiable selon le besoin
    entreprises: List[str] = ["OpenAI"]

    for entreprise in entreprises:
        # Séparateur visuel pour distinguer chaque traitement dans les logs
        print(f"\n{'='*50}")
        print(f"  Traitement : {entreprise}")
        print(f"{'='*50}")

        # Lancement du workflow complet pour cette entreprise
        # inputs={} injecte les variables dans les descriptions des tâches
        # Ex: '{entreprise}' dans task.description sera remplacé par "OpenAI"
        result = crew.kickoff(inputs={"entreprise": entreprise})

        # Affichage du résultat final (email rédigé par l'agent Rédacteur)
        print(f"\n--- Email final pour {entreprise} ---")
        print(result)


if __name__ == "__main__":
    # Point d'entrée — exécuté uniquement si ce fichier est lancé directement
    # (pas si importé comme module dans un autre fichier)
    main()
