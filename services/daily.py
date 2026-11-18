from datetime import timedelta


def daily_summary(course, exam, nb_due, results, today):
    """Résumé du jour pour un cours (fonction pure, facile à tester)."""
    summary = {
        "title": course["title"],
        "due": nb_due,
        "days_left": None,
        "hours": None,
        "target": None,
        "mock_recommended": False,
        "last_score": results[-1]["score"] if results else None,
    }
    if exam:
        days_left = (exam["exam_date"] - today).days
        summary["days_left"] = days_left
        summary["hours"] = exam["hours_per_day"]
        summary["target"] = exam["target_grade"]
        if days_left >= 0:
            mock_date = exam["exam_date"] - timedelta(days=3)
            dernier = results[-1]["taken_at"] if results else None
            summary["mock_recommended"] = today >= mock_date and (
                dernier is None or dernier < mock_date
            )
    return summary