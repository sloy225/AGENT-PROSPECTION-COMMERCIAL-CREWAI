# =============================================================================
# tools.py — Outils personnalisés utilisés par les agents CrewAI
# =============================================================================
# Dans CrewAI, un "Tool" est une capacité externe qu'un agent peut utiliser
# pour interagir avec le monde (API, base de données, fichier, etc.)
# Ici on encapsule l'API Wikipedia dans un outil réutilisable.
# =============================================================================

import wikipedia
from crewai.tools import BaseTool


class WikipediaTool(BaseTool):
    """
    Outil de recherche Wikipedia.
    Hérite de BaseTool (classe de base CrewAI pour tous les outils custom).
    L'agent Chercheur utilisera cet outil pour collecter des infos sur une entreprise.
    """

    # Nom de l'outil — utilisé par le LLM pour décider quand l'appeler
    name: str = "Wikipedia Search"

    # Description — le LLM lit cette description pour comprendre l'utilité de l'outil
    description: str = "Recherche des informations sur une entreprise via Wikipedia"

    def _run(self, entreprise: str) -> str:
        """
        Méthode principale appelée quand l'agent utilise cet outil.

        Args:
            entreprise (str): Nom de l'entreprise à rechercher

        Returns:
            str: Résumé de l'entreprise + URL Wikipedia, ou message d'erreur
        """
        try:
            # Récupère un résumé de 5 phrases depuis Wikipedia
            resume = wikipedia.summary(entreprise, sentences=5)

            # Récupère la page complète pour obtenir l'URL
            page = wikipedia.page(entreprise)

            return f"Résumé : {resume}\nURL : {page.url}"

        except wikipedia.exceptions.DisambiguationError as e:
            # Cas où le nom est ambigu (ex: "Apple" → Apple Inc. ou Apple Records)
            return f"Ambiguïté détectée. Options possibles : {e.options[:3]}"

        except wikipedia.exceptions.PageError:
            # Cas où aucune page n'existe pour ce nom
            return f"Aucune page Wikipedia trouvée pour '{entreprise}'."
