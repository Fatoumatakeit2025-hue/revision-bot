from datetime import date

from db.database import get_connection, DB_PATH


def _ensure_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL UNIQUE,
            exam_date TEXT NOT NULL,
            target_grade REAL NOT NULL,
            hours_per_day REAL NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)


def set_exam(course_id, exam_date, target_grade, hours_per_day, path=DB_PATH):
    with get_connection(path) as conn:
        _ensure_table(conn)
        conn.execute(
            """INSERT INTO exams (course_id, exam_date, target_grade, hours_per_day)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(course_id) DO UPDATE SET
                   exam_date = excluded.exam_date,
                   target_grade = excluded.target_grade,
                   hours_per_day = excluded.hours_per_day""",
            (course_id, exam_date.isoformat(), target_grade, hours_per_day),
        )


def get_exam(course_id, path=DB_PATH):
    with get_connection(path) as conn:
        _ensure_table(conn)
        row = conn.execute(
            "SELECT * FROM exams WHERE course_id = ?", (course_id,)
        ).fetchone()
    if row is None:
        return None
    exam = dict(row)
    exam["exam_date"] = date.fromisoformat(exam["exam_date"])
    return exam