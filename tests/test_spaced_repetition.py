from datetime import date

from services.spaced_repetition import next_review

TODAY = date(2026, 11, 3)


def test_premiere_reussite():
    level, when = next_review(0, True, TODAY)
    assert level == 1
    assert when == date(2026, 11, 4)


def test_reussites_successives():
    level = 0
    jours = []
    for _ in range(5):
        level, when = next_review(level, True, TODAY)
        jours.append((when - TODAY).days)
    assert jours == [1, 3, 7, 15, 15]


def test_echec_remet_a_zero():
    level, when = next_review(3, False, TODAY)
    assert level == 0
    assert when == date(2026, 11, 4)