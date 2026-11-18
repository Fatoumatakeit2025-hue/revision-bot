from datetime import datetime
from db.exams import set_exam, get_exam, save_mock_result, get_mock_results
from services.mock_exam import generate_mock_exam, grade_exam, final_score
from services.planner import plan_revision
from db.database import (
    init_db, get_or_create_user, add_course, add_question,
    get_courses, get_due_questions, record_answer,
)
from services.ai import generate_flashcards, answer_with_ai
from services.answering import answer


def lire_texte():
    print("Écris ou colle le texte du cours (termine par une ligne vide) :")
    lignes = []
    while True:
        ligne = input()
        if not ligne.strip():
            break
        lignes.append(ligne)
    return "\n".join(lignes)


def fiches_ia(course_id, texte, n=5):
    if not texte.strip():
        print("Texte vide : impossible de générer des fiches.")
        return
    print("Génération des fiches...")
    try:
        cartes = generate_flashcards(texte, n=n)
    except Exception as e:
        print(f"L'IA n'est pas disponible ({type(e).__name__}).")
        return
    if not cartes:
        print("L'IA n'a pas renvoyé de fiches exploitables.")
        return
    for i, c in enumerate(cartes, 1):
        print(f"\n{i}. {c['question']}\n   -> {c['answer']}")
    if input("\nEnregistrer ces fiches ? (o/n) : ").strip().lower() == "o":
        for c in cartes:
            add_question(course_id, c["question"], c["answer"])
        print(f"{len(cartes)} fiches enregistrées.")
def saisir_texte():
    print("Écris ou colle le texte du cours (termine par une ligne vide) :")
    lignes = []
    while True:
        ligne = input()
        if not ligne.strip():
            break
        lignes.append(ligne)
    return "\n".join(lignes)       
        
def demander_examen():
    if input("Ajouter les infos de ton examen ? (o/n) : ").strip().lower() != "o":
        return None
    try:
        jour = input("Date de l'examen (JJ/MM/AAAA) : ").strip()
        exam_date = datetime.strptime(jour, "%d/%m/%Y").date()
        note = float(input("Note visée (sur 20) : ").replace(",", "."))
        heures = float(input("Heures de révision par jour : ").replace(",", "."))
        plan = plan_revision(exam_date, note, heures)
    except ValueError as e:
        print(f"Informations invalides : {e}")
        return None
    return exam_date, note, heures, plan


def afficher_plan(plan):
    print(f"\nIl te reste {plan['days_left']} jours, soit {plan['total_hours']:g} h de révision.")
    for p in plan["phases"]:
        print(f"- {p['name']} : du {p['start']:%d/%m/%Y} au {p['end']:%d/%m/%Y}")
    print(f"- Examen blanc conseillé le {plan['mock_exam_date']:%d/%m/%Y}")
    print(f"Fiches à générer : {plan['nb_fiches']}")
    
def choisir_cours(user_id):
    courses = get_courses(user_id)
    if not courses:
        print("Aucun cours pour l'instant.")
        return None
    for i, c in enumerate(courses, 1):
        print(f"{i}. {c['title']}")
    choix = input("Numéro du cours : ").strip()
    if not choix.isdigit() or not 1 <= int(choix) <= len(courses):
        print("Choix invalide.")
        return None
    return courses[int(choix) - 1]


def passer_examen_blanc(course):
    if not course["content"].strip():
        print("Ce cours n'a pas de texte : impossible de créer un examen.")
        return
    exam = get_exam(course["id"])
    cible = exam["target_grade"] if exam else 12
    print("Création de l'examen blanc...")
    try:
        questions = generate_mock_exam(course["content"], cible)
    except Exception as e:
        print(f"L'IA n'est pas disponible ({type(e).__name__}).")
        return
    if not questions:
        print("L'IA n'a pas renvoyé d'examen exploitable.")
        return

    print(f"\n=== EXAMEN BLANC : {course['title']} (sur 20) ===")
    reponses = []
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i} ({q['points']:g} pts) : {q['question']}")
        reponses.append(input("Ta réponse : ").strip())

    print("\nCorrection en cours...")
    try:
        resultats = grade_exam(questions, reponses)
    except Exception:
        resultats = None
    if resultats is None:
        print("Correction automatique indisponible. Compare avec les réponses types :")
        for i, q in enumerate(questions, 1):
            print(f"{i}. {q['model_answer']}")
        return

    for i, (q, r) in enumerate(zip(questions, resultats), 1):
        print(f"\nQuestion {i} : {r['score']:g}/{q['points']:g}")
        print(f"  {r['comment']}")
        print(f"  Réponse type : {q['model_answer']}")
    note = final_score(resultats)
    print(f"\nNote : {note:g}/20 (objectif : {cible:g})")
    if note >= cible:
        print("Objectif atteint, bravo !")
    else:
        print(f"Il te manque {cible - note:g} points : revois les questions ratées.")
    save_mock_result(course["id"], note)

def ajouter_cours(user_id):
    titre = input("Titre du cours : ").strip()
    if not titre:
        print("Titre vide, annulé.")
        return
    texte = saisir_texte()
    course_id = add_course(user_id, titre, texte)

    nb_fiches = 5
    infos = demander_examen()
    if infos:
        exam_date, note, heures, plan = infos
        set_exam(course_id, exam_date, note, heures)
        afficher_plan(plan)
        nb_fiches = plan["nb_fiches"]

    if input("Générer des fiches avec l'IA ? (o/n) : ").strip().lower() == "o":
        fiches_ia(course_id, texte, nb_fiches)
    print("Questions manuelles (question vide pour terminer).")
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
    if not question:
        return
    try:
        print("\n" + answer_with_ai(question, courses))
    except Exception:
        print("\nIA indisponible : je cherche dans tes cours.")
        resultats = answer(question, courses)
        if not resultats:
            print("Je n'ai rien trouvé dans tes cours à ce sujet.")
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
        print("\n1. Ajouter un cours   2. Réviser   3. Poser une question")
        print("4. Examen blanc   5. Quitter")
        choix = input("> ").strip()
        if choix == "1":
            ajouter_cours(user_id)
        elif choix == "2":
            reviser(user_id)
        elif choix == "3":
            poser_question(user_id)
        elif choix == "4":
            course = choisir_cours(user_id)
            if course:
                passer_examen_blanc(course)
        elif choix == "5":
            break


if __name__ == "__main__":
    main()