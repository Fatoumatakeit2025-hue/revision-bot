from datetime import date, timedelta

# Délais (en jours) selon le niveau atteint
INTERVALS = [1, 3, 7, 15]


def next_review(level, success, today=None):
    """Retourne (nouveau_niveau, prochaine_date) pour une question."""
    today = today or date.today()

    if success:
        new_level = min(level + 1, len(INTERVALS))
        days = INTERVALS[new_level - 1]
    else:
        new_level = 0
        days = 1

    return new_level, today + timedelta(days=days)