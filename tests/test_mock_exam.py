import os
import tempfile
from datetime import date

from db.database import init_db, add_user, add_course
from db.exams import save_mock_result, get_mock_results
from services.mock_exam import (
    generate_mock_exam, grade_exam, final_score, parse_exam, level_for_grade,
)


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


QUESTIONS = [
    {"question": "Q1", "model_answer": "R1", "points": 10},
    {"question": "Q2", "model_answer": "R2", "points": 10},
]


def test_generation_de_l_examen():
    client = FakeClient(
        '[{"question": "Q1 ?", "model_answer": "R1"},'
        ' {"question": "Q2 ?", "model_answer": "R2"}]'
    )
    questions = generate_mock_exam("Un cours", 14, client=client)
    assert len(questions) == 2
    assert questions[0]["points"] == 10


def test_examen_invalide():
    assert parse_exam("pas du json") == []


def test_note_limitee_aux_points_de_la_question():
    client = FakeClient('[{"score": 5, "comment": "ok"}, {"score": 99, "comment": "trop"}]')
    resultats = grade_exam(QUESTIONS, ["a", "b"], client=client)
    assert [r["score"] for r in resultats] == [5, 10]
    assert final_score(resultats) == 15


def test_reponse_vide_vaut_zero():
    client = FakeClient('[{"score": 10, "comment": "x"}, {"score": 4, "comment": "y"}]')
    resultats = grade_exam(QUESTIONS, ["", "b"], client=client)
    assert resultats[0]["score"] == 0


def test_correction_invalide():
    assert grade_exam(QUESTIONS, ["a", "b"], client=FakeClient("n'importe quoi")) is None


def test_niveau_selon_la_note_visee():
    assert "difficile" in level_for_grade(17)
    assert "moyenne" in level_for_grade(13)
    assert "accessible" in level_for_grade(9)


def test_historique_des_notes():
    path = os.path.join(tempfile.mkdtemp(), "test.db")
    init_db(path)
    course_id = add_course(add_user("Test", path), "Réseaux", "Cours", path)
    assert get_mock_results(course_id, path) == []

    save_mock_result(course_id, 12.5, path, date(2026, 11, 18))
    save_mock_result(course_id, 14, path, date(2026, 11, 25))
    notes = get_mock_results(course_id, path)
    assert [n["score"] for n in notes] == [12.5, 14]
    assert notes[0]["taken_at"] == date(2026, 11, 18)