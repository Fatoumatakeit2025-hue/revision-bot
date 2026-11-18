import os
import tempfile
from datetime import date

from db.database import init_db, add_user, add_course
from db.exams import set_exam, get_exam


def test_enregistrer_et_lire_examen():
    path = os.path.join(tempfile.mkdtemp(), "test.db")
    init_db(path)
    course_id = add_course(add_user("Test", path), "Réseaux", "Cours", path)

    assert get_exam(course_id, path) is None

    set_exam(course_id, date(2027, 1, 15), 14, 2, path)
    exam = get_exam(course_id, path)
    assert exam["exam_date"] == date(2027, 1, 15)
    assert exam["target_grade"] == 14

    set_exam(course_id, date(2027, 1, 20), 16, 3, path)
    assert get_exam(course_id, path)["target_grade"] == 16