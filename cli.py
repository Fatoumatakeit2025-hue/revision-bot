from db.database import (
    init_db, get_or_create_user, add_course, add_question,
    get_courses, get_due_questions, record_answer,
)
from services.answering import answer


def ajouter_cours(user_id):
    titre = input("Titre du cours : ").strip()
    if not titre:
        print("Titre vide, annulé.")
        return
    print("Écris ou colle le texte du cours (termine par une ligne vide) :")
    lignes = []
    while True:
        ligne = input()
        if not ligne.strip():
            break
        lignes.append(ligne)
    course_id = add_course(user_id, titre, "\n".join(lignes))
    print("Questions de révision (question vide pour terminer).")
    while True:
        question = input("Question : ").strip()
        if not question:
            break
        reponse = input("Réponse : ").strip()
        if not reponse:
            print("Réponse vide, question ignorée.")
            continue
        add_question(course_id, question, reponse)
    print("Cours enregistré.")


def poser_question(user_id):
    courses = get_courses(user_id)
    if not courses:
        print("Aucun cours enregistré.")
        return
    question = input("Ta question : ").strip()
    resultats = answer(question, courses)
    if not resultats:
        print("Je n'ai rien trouvé dans tes cours à ce sujet.")
        return
    for _, titre, passage in resultats:
        print(f"\n[{titre}] {passage}")


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
        print("\n1. Ajouter un cours   2. Réviser   3. Poser une question   4. Quitter")
        choix = input("> ").strip()
        if choix == "1":
            ajouter_cours(user_id)
        elif choix == "2":
            reviser(user_id)
        elif choix == "3":
            poser_question(user_id)
        elif choix == "4":
            break


if __name__ == "__main__":
    main()