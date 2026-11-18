from services.ai import generate_flashcards, answer_with_ai, parse_flashcards


class FakeClient:
    """Imite le client de l'IA sans appeler Internet."""

    def __init__(self, text):
        self.text = text
        self.chat = self
        self.completions = self

    def create(self, **kwargs):
        message = type("Message", (), {"content": self.text})()
        choice = type("Choice", (), {"message": message})()
        return type("Response", (), {"choices": [choice]})()


def test_fiches_valides():
    client = FakeClient('[{"question": "Q1 ?", "answer": "R1"}]')
    cartes = generate_flashcards("Un cours", client=client)
    assert cartes == [{"question": "Q1 ?", "answer": "R1"}]


def test_json_invalide():
    assert parse_flashcards("pas du json") == []


def test_bloc_markdown_ignore():
    raw = '```json\n[{"question": "Q ?", "answer": "R"}]\n```'
    assert len(parse_flashcards(raw)) == 1


def test_entrees_incompletes_ignorees():
    raw = '[{"question": "Q ?"}, {"question": "", "answer": "R"}, 3]'
    assert parse_flashcards(raw) == []


def test_reponse_ia():
    client = FakeClient("Un graphe relie des sommets.")
    cours = [{"title": "Graphes", "content": "Un graphe est ..."}]
    assert answer_with_ai("C'est quoi un graphe ?", cours, client=client) == "Un graphe relie des sommets."