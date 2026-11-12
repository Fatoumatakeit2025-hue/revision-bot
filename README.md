# Assistant de révisions

Assistant en Python pour réviser ses cours : enregistrer un cours, réviser avec des fiches planifiées par **répétition espacée**, et **poser des questions** dont les réponses sont cherchées dans ses propres cours.

> Projet en cours de développement. Une version Telegram est prévue.

## Fonctionnalités

- Ajout de cours (titre, texte, fiches question/réponse)
- Révision par répétition espacée : une réussite repousse la question à 1, 3, 7 puis 15 jours, un échec la ramène au lendemain
- Mode « Poser une question » : le programme retrouve les passages de cours les plus pertinents
- Base de données SQLite locale
- Tests automatiques avec pytest

## Technologies

Python 3.14, SQLite, pytest, Git/GitHub

## Structure du projet

```
cli.py                  # interface en ligne de commande
db/database.py          # base de données SQLite
services/
  spaced_repetition.py  # calcul des prochaines révisions
  answering.py          # recherche de réponses dans les cours
tests/                  # tests automatiques
```

## Installation

```
git clone https://github.com/<ton-pseudo>/revision-bot.git
cd revision-bot
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Utilisation

```
python cli.py
```

## Tests

```
python -m pytest
```

## Feuille de route

- [x] Base de données et tests
- [x] Répétition espacée
- [x] Interface en ligne de commande
- [x] Réponses par recherche dans les cours
- [ ] Génération de questions et réponses rédigées par une IA
- [ ] Bot Telegram
- [ ] Rappels quotidiens
- [ ] Déploiement