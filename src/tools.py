import wikipedia
from crewai.tools import BaseTool


class WikipediaTool(BaseTool):
    name: str = "Wikipedia Search"
    description: str = "Recherche des informations sur une entreprise via Wikipedia"

    def _run(self, entreprise: str) -> str:
        try:
            resume = wikipedia.summary(entreprise, sentences=5)
            page = wikipedia.page(entreprise)
            return f"Résumé : {resume}\nURL : {page.url}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Ambiguïté détectée. Options : {e.options[:3]}"
        except wikipedia.exceptions.PageError:
            return f"Aucune page Wikipedia trouvée pour '{entreprise}'."
