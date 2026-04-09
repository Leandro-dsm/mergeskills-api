import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from database import db
from models import Course, Lesson, Question, User

USERS = [
    {"id": 1, "username": "aluno_teste"},
    {"id": 2, "username": "aluno_02"}
]

COURSES = [
    {
        "id": 1,
        "title": "Python Fundamentos",
        "description": "Aprenda o básico de Python",
        "icon": "python",
        "color": "#306998",
        "total_lessons": 2,
    },
    {
        "id": 2,
        "title": "Flask API Masterclass",
        "description": "Crie APIs profissionais",
        "icon": "flask",
        "color": "#FF5722",
        "total_lessons": 2,
    },
]

LESSONS = [
    {"id": 1, "course_id": 1, "title": "Introdução ao Python",
     "description": "Primeiros passos com Python", "order": 1},
    {"id": 2, "course_id": 1, "title": "Variáveis e Tipos",
     "description": "Tipos de dados em Python", "order": 2},
    {"id": 3, "course_id": 2, "title": "Setup do Ambiente Flask",
     "description": "Configurando o Flask", "order": 1},
    {"id": 4, "course_id": 2, "title": "Blueprints e Rotas",
     "description": "Organizando rotas com Blueprints", "order": 2},
]

QUESTIONS = [
    {
        "id": 1,
        "lesson_id": 1,
        "question": "O que é Python?",
        "code": None,
        "options": ["Um réptil", "Uma linguagem de programação", "Um editor de texto"],
        "correct_answer": 1,
        "order": 1,
    },
    {
        "id": 2,
        "lesson_id": 1,
        "question": "Qual comando imprime textos?",
        "code": "# Para imprimir 'Olá mundo':\n[BLANK]('Olá mundo')",
        "options": ["echo()", "console.log()", "print()"],
        "correct_answer": 2,
        "order": 2,
    },
]


def seed():
    """Popula o banco de dados com os dados iniciais."""
    app = create_app()

    with app.app_context():
        # Verifica se já existem dados
        if Course.query.first():
            print("Banco já possui dados. Pulando seed.")
            return

        print("Populando banco de dados...")

        for u in USERS:
            db.session.add(User(**u))
        print(f"  ✅ {len(USERS)} usuários inseridos")

        for c in COURSES:
            db.session.add(Course(**c))
        print(f"  ✅ {len(COURSES)} cursos inseridos")

        for l in LESSONS:
            db.session.add(Lesson(**l))
        print(f"  ✅ {len(LESSONS)} lições inseridas")

        for q in QUESTIONS:
            db.session.add(Question(**q))
        print(f"  ✅ {len(QUESTIONS)} perguntas inseridas")

        db.session.commit()
        print("✨ Seed concluído com sucesso!")


if __name__ == '__main__':
    seed()