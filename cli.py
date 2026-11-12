from db.database import (
    init_db, get_or_create_user, add_course, add_question,
    get_courses, get_due_questions, record_answer,
)


def ajouter_cours(user_id):
    titre = input("Titre du cours : ").strip()
    if not titre:
        print("Titre vide, annulé.")
        return
    course_id = add_course(user_id, titre, "")
    print("Ajoute des questions (laisse la question vide pour terminer).")
    while True:
        question = input("Question : ").strip()
        if not question:
            break
        reponse = input("Réponse : ").strip()
        add_question(course_id, question, reponse)
    print("Cours enregistré.")


def reviser(user_id):
    courses = get_courses(user_id)
    if not courses:
        print("Aucun cours pour l'instant.")
        return
    for i, c in enumerate(courses, 1):
        print(f"{i}. {c['title']}")
    choix = input("Numéro du cours : ").strip()
    if not choix.isdigit() or not 1 <= int(choix) <= len(courses):
        print("Choix invalide.")
        return
    course = courses[int(choix) - 1]
    a_reviser = get_due_questions(course["id"])
    if not a_reviser:
        print("Rien à réviser aujourd'hui !")
        return
    for q in a_reviser:
        print(f"\nQuestion : {q['question']}")
        input("Appuie sur Entrée pour voir la réponse...")
        print(f"Réponse : {q['answer']}")
        reponse = input("Tu le savais ? (o/n) : ").strip().lower()
        _, quand = record_answer(q["id"], reponse == "o")
        print(f"Prochaine révision : {quand.strftime('%d/%m/%Y')}")


def main():
    init_db()
    user_id = get_or_create_user("moi")
    while True:
        print("\n1. Ajouter un cours   2. Réviser   3. Quitter")
        choix = input("> ").strip()
        if choix == "1":
            ajouter_cours(user_id)
        elif choix == "2":
            reviser(user_id)
        elif choix == "3":
            break


if __name__ == "__main__":
    main()