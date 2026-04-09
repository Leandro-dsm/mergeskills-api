from flask import Blueprint, jsonify, request
from database import db
from models import Lesson, Question

lessons_bp = Blueprint('lessons', __name__)


# GET - Listar todas as aulas
@lessons_bp.route('/', methods=['GET'])
def get_all_lessons():
    """
    Lista todas as aulas
    ---
    tags:
      - Aulas
    responses:
      200:
        description: Lista de todas as aulas
    """
    lessons = Lesson.query.all()
    return jsonify([l.to_dict() for l in lessons])


# GET - Buscar aula por ID
@lessons_bp.route('/<int:lesson_id>', methods=['GET'])
def get_lesson_by_id(lesson_id):
    """
    Obtém detalhes de uma aula específica
    ---
    tags:
      - Aulas
    parameters:
      - name: lesson_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Detalhes da aula
      404:
        description: Aula não encontrada
    """
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Aula não encontrada"}), 404
    return jsonify(lesson.to_dict())


# POST - Criar nova aula
@lessons_bp.route('/', methods=['POST'])
def create_lesson():
    """
    Cria uma nova aula
    ---
    tags:
      - Aulas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            course_id:
              type: integer
            title:
              type: string
            description:
              type: string
            order:
              type: integer
    responses:
      201:
        description: Aula criada com sucesso
      400:
        description: Dados inválidos
    """
    data = request.json
    if not data or 'course_id' not in data or 'title' not in data:
        return jsonify({"error": "course_id e title são obrigatórios"}), 400

    lesson = Lesson(
        course_id=data['course_id'],
        title=data['title'],
        description=data.get('description', ''),
        order=data.get('order', 0)
    )
    db.session.add(lesson)
    db.session.commit()
    return jsonify(lesson.to_dict()), 201


# PUT - Atualizar aula
@lessons_bp.route('/<int:lesson_id>', methods=['PUT'])
def update_lesson(lesson_id):
    """
    Atualiza uma aula existente
    ---
    tags:
      - Aulas
    parameters:
      - name: lesson_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            description:
              type: string
            order:
              type: integer
    responses:
      200:
        description: Aula atualizada
      404:
        description: Aula não encontrada
    """
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Aula não encontrada"}), 404

    data = request.json
    if 'title' in data:
        lesson.title = data['title']
    if 'description' in data:
        lesson.description = data['description']
    if 'order' in data:
        lesson.order = data['order']

    db.session.commit()
    return jsonify(lesson.to_dict())


# DELETE - Remover aula
@lessons_bp.route('/<int:lesson_id>', methods=['DELETE'])
def delete_lesson(lesson_id):
    """
    Remove uma aula e todas suas perguntas
    ---
    tags:
      - Aulas
    parameters:
      - name: lesson_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Aula removida com sucesso
      404:
        description: Aula não encontrada
    """
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Aula não encontrada"}), 404

    db.session.delete(lesson)
    db.session.commit()
    return jsonify({"message": f"Aula {lesson_id} removida com sucesso"}), 200


# GET - Listar perguntas de uma aula
@lessons_bp.route('/<int:lesson_id>/perguntas', methods=['GET'])
def get_questions_by_lesson(lesson_id):
    """
    Lista perguntas de uma aula
    ---
    tags:
      - Aulas
    parameters:
      - name: lesson_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Lista de perguntas da aula
      404:
        description: Aula não encontrada
    """
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Aula não encontrada"}), 404

    questions = Question.query.filter_by(lesson_id=lesson_id).order_by(Question.order).all()
    return jsonify([q.to_dict() for q in questions])