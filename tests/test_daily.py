from datetime import date

from services.daily import daily_summary

TODAY = date(2027, 1, 12)
COURS = {"title": "Réseaux"}
EXAM = {"exam_date": date(2027, 1, 15), "target_grade": 14, "hours_per_day": 2}


def test_sans_examen():
    s = daily_summary(COURS, None, 3, [], TODAY)
    assert s["days_left"] is None
    assert s["due"] == 3
    assert not s["mock_recommended"]


def test_examen_blanc_recommande_a_trois_jours():
    s = daily_summary(COURS, EXAM, 0, [], TODAY)
    assert s["days_left"] == 3
    assert s["mock_recommended"]


def test_examen_blanc_deja_passe_recemment():
    resultats = [{"taken_at": date(2027, 1, 12), "score": 13}]
    s = daily_summary(COURS, EXAM, 0, resultats, TODAY)
    assert not s["mock_recommended"]
    assert s["last_score"] == 13


def test_pas_de_recommandation_trop_tot():
    s = daily_summary(COURS, EXAM, 0, [], date(2026, 12, 1))
    assert not s["mock_recommended"]


def test_examen_passe():
    s = daily_summary(COURS, EXAM, 0, [], date(2027, 1, 20))
    assert s["days_left"] < 0
    assert not s["mock_recommended"]