import os
import tempfile
from datetime import date, timedelta

from db.database import (
    init_db, add_user, add_course, add_question,
    get_due_questions, record_answer,
)


def make_db():
    path = os.path.join(tempfile.mkdtemp(), "test.db")
    init_db(path)
    user_id = add_user("Test", path)
    course_id = add_course(user_id, "Graphes", "Cours", path)
    return path, course_id


def test_question_planifiee_apres_reussite():
    path, course_id = make_db()
    question_id = add_question(course_id, "Q ?", "R", path)
    today = date.today()

    assert len(get_due_questions(course_id, today, path)) == 1

    record_answer(question_id, True, today, path)

    assert get_due_questions(course_id, today, path) == []
    demain = today + timedelta(days=1)
    assert len(get_due_questions(course_id, demain, path)) == 1


def test_echec_remet_le_niveau_a_zero():
    path, course_id = make_db()
    question_id = add_question(course_id, "Q ?", "R", path)
    today = date.today()

    record_answer(question_id, True, today, path)
    level, _ = record_answer(question_id, False, today, path)

    assert level == 0