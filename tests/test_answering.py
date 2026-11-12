from services.answering import answer

COURS = [{
    "title": "Graphes",
    "content": "Un graphe est un ensemble de sommets reliés par des arêtes. "
               "Dijkstra calcule les plus courts chemins.",
}]


def test_trouve_le_bon_passage():
    resultats = answer("Que fait Dijkstra ?", COURS)
    assert resultats[0][2].startswith("Dijkstra")


def test_question_sans_resultat():
    assert answer("recette de cuisine", COURS) == []