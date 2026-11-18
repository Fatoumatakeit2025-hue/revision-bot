from datetime import date

import pytest

from services.planner import plan_revision

TODAY = date(2026, 11, 18)


def test_plan_basique():
    plan = plan_revision(date(2027, 1, 15), 14, 2, TODAY)
    assert plan["days_left"] == 58
    assert plan["total_hours"] == 116
    assert 5 <= plan["nb_fiches"] <= 20
    assert plan["phases"][0]["start"] == TODAY
    assert plan["phases"][-1]["end"] == date(2027, 1, 15)
    assert plan["mock_exam_date"] == date(2027, 1, 12)


def test_note_plus_haute_donne_plus_de_fiches():
    bas = plan_revision(date(2026, 11, 28), 10, 1, TODAY)
    haut = plan_revision(date(2026, 11, 28), 18, 1, TODAY)
    assert haut["nb_fiches"] >= bas["nb_fiches"]


def test_date_passee():
    with pytest.raises(ValueError):
        plan_revision(date(2026, 11, 1), 12, 2, TODAY)


def test_note_invalide():
    with pytest.raises(ValueError):
        plan_revision(date(2027, 1, 15), 25, 2, TODAY)


def test_examen_demain():
    plan = plan_revision(date(2026, 11, 19), 12, 2, TODAY)
    assert plan["mock_exam_date"] == TODAY