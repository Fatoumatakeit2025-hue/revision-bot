import os
import tempfile

from db.database import init_db, add_user, add_course, add_question, get_questions


def test_ajout_et_lecture_de_questions():
    path = os.path.join(tempfile.mkdtemp(), "test.db")
    init_db(path)

    user_id = add_user("Test", path)
    course_id = add_course(user_id, "Graphes", "Un graphe est ...", path)
    add_question(course_id, "Qu'est-ce qu'un graphe ?", "Un ensemble de sommets et d'arêtes", path)

    questions = get_questions(course_id, path)
    assert len(questions) == 1
    assert questions[0]["question"] == "Qu'est-ce qu'un graphe ?"