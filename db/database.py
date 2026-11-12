import sqlite3
from datetime import date, datetime

from services.spaced_repetition import next_review

DB_PATH = "revision.db"


def get_connection(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path=DB_PATH):
    with get_connection(path) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            level INTEGER NOT NULL DEFAULT 0,
            next_review TEXT NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        );
        """)


def add_user(name, path=DB_PATH):
    with get_connection(path) as conn:
        cur = conn.execute(
            "INSERT INTO users (name, created_at) VALUES (?, ?)",
            (name, datetime.now().isoformat()),
        )
        return cur.lastrowid


def add_course(user_id, title, content, path=DB_PATH):
    with get_connection(path) as conn:
        cur = conn.execute(
            "INSERT INTO courses (user_id, title, content, created_at) VALUES (?, ?, ?, ?)",
            (user_id, title, content, datetime.now().isoformat()),
        )
        return cur.lastrowid


def add_question(course_id, question, answer, path=DB_PATH):
    with get_connection(path) as conn:
        cur = conn.execute(
            "INSERT INTO questions (course_id, question, answer, next_review) VALUES (?, ?, ?, ?)",
            (course_id, question, answer, date.today().isoformat()),
        )
        return cur.lastrowid


def get_questions(course_id, path=DB_PATH):
    with get_connection(path) as conn:
        rows = conn.execute(
            "SELECT * FROM questions WHERE course_id = ?", (course_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_due_questions(course_id, today=None, path=DB_PATH):
    today = today or date.today()
    with get_connection(path) as conn:
        rows = conn.execute(
            "SELECT * FROM questions WHERE course_id = ? AND next_review <= ?",
            (course_id, today.isoformat()),
        ).fetchall()
        return [dict(r) for r in rows]


def record_answer(question_id, success, today=None, path=DB_PATH):
    today = today or date.today()
    with get_connection(path) as conn:
        row = conn.execute(
            "SELECT level FROM questions WHERE id = ?", (question_id,)
        ).fetchone()
        if row is None:
            raise ValueError(f"Question {question_id} introuvable")
        new_level, when = next_review(row["level"], success, today)
        conn.execute(
            "UPDATE questions SET level = ?, next_review = ? WHERE id = ?",
            (new_level, when.isoformat(), question_id),
        )
        return new_level, when