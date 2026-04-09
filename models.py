from database import db
from sqlalchemy.dialects.postgresql import JSONB


class Course(db.Model):
    """Modelo SQLAlchemy para a tabela de Cursos."""
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    icon = db.Column(db.String)
    color = db.Column(db.String)
    total_lessons = db.Column(db.Integer, default=0)

    lessons = db.relationship('Lesson', backref='course', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'icon': self.icon,
            'color': self.color,
            'total_lessons': self.total_lessons,
        }


class Lesson(db.Model):
    """Modelo SQLAlchemy para a tabela de Aulas/Lições."""
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    order = db.Column(db.Integer, default=0)

    questions = db.relationship('Question', backref='lesson', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'order': self.order,
        }


class Question(db.Model):
    """Modelo SQLAlchemy para a tabela de Perguntas."""
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    question = db.Column(db.String, nullable=False)
    code = db.Column(db.String)
    options = db.Column(JSONB)
    correct_answer = db.Column(db.Integer)
    order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'lesson_id': self.lesson_id,
            'question': self.question,
            'code': self.code,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'order': self.order,
        }


class User(db.Model):
    """Modelo SQLAlchemy para a tabela de Usuários."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)

    attempts = db.relationship('QuestionAttempt', backref='user', lazy=True)
    progress = db.relationship('LessonProgress', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }


class QuestionAttempt(db.Model):
    """Modelo SQLAlchemy para registrar cada tentativa de resposta."""
    __tablename__ = 'question_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_option = db.Column(db.Integer, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'selected_option': self.selected_option,
            'is_correct': self.is_correct,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
        }


class LessonProgress(db.Model):
    """Modelo SQLAlchemy para registrar o progresso em cada lição."""
    __tablename__ = 'lesson_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'lesson_id': self.lesson_id,
            'is_completed': self.is_completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }