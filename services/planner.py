from datetime import date, timedelta

PHASES = [
    ("Découverte du cours", 0.45),
    ("Consolidation", 0.30),
    ("Révision finale", 0.25),
]


def plan_revision(exam_date, target_grade, hours_per_day, today=None):
    today = today or date.today()
    days_left = (exam_date - today).days
    if days_left <= 0:
        raise ValueError("La date de l'examen doit être dans le futur.")
    if not 0 <= target_grade <= 20:
        raise ValueError("La note visée doit être entre 0 et 20.")
    if not 0 < hours_per_day <= 12:
        raise ValueError("Les heures par jour doivent être entre 0 et 12.")

    total_hours = days_left * hours_per_day

    # Plus la note visée est haute, plus il faut de fiches (de 1x à 2x)
    intensity = 1 + max(0, target_grade - 10) / 10
    nb_fiches = round(min(20, max(5, total_hours * 0.5 * intensity)))

    phases = []
    start = today
    for i, (name, share) in enumerate(PHASES):
        if i == len(PHASES) - 1:
            end = exam_date
        else:
            end = start + timedelta(days=round(days_left * share))
        if end > start or i == len(PHASES) - 1:
            phases.append({"name": name, "start": start, "end": end})
        start = end

    if days_left <= 3:
        mock_exam_date = today
    else:
        mock_exam_date = exam_date - timedelta(days=3)

    return {
        "days_left": days_left,
        "total_hours": total_hours,
        "nb_fiches": nb_fiches,
        "phases": phases,
        "mock_exam_date": mock_exam_date,
    }