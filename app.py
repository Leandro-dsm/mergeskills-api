from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv
import os

from schemas.course_schema import CourseSchema
from schemas.lesson_schema import LessonSchema
from schemas.question_schema import QuestionSchema, QuestionIdSchema
from schemas.progress_schema import (
    SubmitAnswerSchema,
    AnswerResultSchema,
    ResetProgressSchema,
    UserHistorySchema,
    ProgressResponseSchema,
)

load_dotenv()


def create_app():
    app = Flask(__name__)

    from database import init_db
    init_db(app)

    # Configuração do Swagger
    app.config['SWAGGER'] = {
        'title': 'LDW Merge Skills',
        'uiversion': 3,
        'description': 'Plataforma de aprendizado de habilidades de desenvolvimento web',
        'specs_route': '/apidocs/'
    }

    swagger_template = {
        "tags": [
            {"name": "Health"},
            {"name": "Cursos"},
            {"name": "Aulas"},
            {"name": "Perguntas"},
            {"name": "Progresso"}
        ],
        "definitions": {
            "Course": CourseSchema.model_json_schema(),
            "Lesson": LessonSchema.model_json_schema(),
            "Question": QuestionSchema.model_json_schema(),
            "QuestionId": QuestionIdSchema.model_json_schema(),
            "SubmitAnswer": SubmitAnswerSchema.model_json_schema(),
            "AnswerResult": AnswerResultSchema.model_json_schema(),
            "ResetProgress": ResetProgressSchema.model_json_schema(),
            "UserHistory": UserHistorySchema.model_json_schema(),
            "UserProgress": ProgressResponseSchema.model_json_schema(),
            "Error": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        }
    }

    Swagger(app, template=swagger_template)

    # Register Blueprints
    from routes.health import health_bp
    from routes.courses import courses_bp
    from routes.lessons import lessons_bp
    from routes.questions import questions_bp
    from routes.progress import progress_bp

    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(courses_bp, url_prefix='/api/cursos')
    app.register_blueprint(lessons_bp, url_prefix='/api/aulas')
    app.register_blueprint(questions_bp, url_prefix='/api/perguntas')
    app.register_blueprint(progress_bp, url_prefix='/api/progresso')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)