from flask import Blueprint, jsonify, request
from database import db
from models import Course, Lesson

courses_bp = Blueprint('courses', __name__)


# GET - Listar todos os cursos
@courses_bp.route('/', methods=['GET'])
def get_courses():
    """
    Lista todos os cursos disponíveis
    ---
    tags:
      - Cursos
    responses:
      200:
        description: Lista de cursos
    """
    courses = Course.query.all()
    return jsonify([c.to_dict() for c in courses])


# GET - Buscar curso por ID
@courses_bp.route('/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    """
    Obtém detalhes de um curso específico
    ---
    tags:
      - Cursos
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Detalhes do curso
      404:
        description: Curso não encontrado
    """
    course = Course.query.get(course_id)
    if course:
        return jsonify(course.to_dict())
    return jsonify({"error": "Curso não encontrado"}), 404


# POST - Criar novo curso
@courses_bp.route('/', methods=['POST'])
def create_course():
    """
    Cria um novo curso
    ---
    tags:
      - Cursos
    parameters:
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
            icon:
              type: string
            color:
              type: string
    responses:
      201:
        description: Curso criado com sucesso
      400:
        description: Dados inválidos
    """
    data = request.json
    if not data or 'title' not in data:
        return jsonify({"error": "Título é obrigatório"}), 400

    course = Course(
        title=data['title'],
        description=data.get('description', ''),
        icon=data.get('icon', ''),
        color=data.get('color', '#000000'),
        total_lessons=0
    )
    db.session.add(course)
    db.session.commit()

    return jsonify(course.to_dict()), 201


# PUT - Atualizar curso
@courses_bp.route('/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """
    Atualiza um curso existente
    ---
    tags:
      - Cursos
    parameters:
      - name: course_id
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
            icon:
              type: string
            color:
              type: string
    responses:
      200:
        description: Curso atualizado
      404:
        description: Curso não encontrado
    """
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Curso não encontrado"}), 404

    data = request.json
    if 'title' in data:
        course.title = data['title']
    if 'description' in data:
        course.description = data['description']
    if 'icon' in data:
        course.icon = data['icon']
    if 'color' in data:
        course.color = data['color']

    db.session.commit()
    return jsonify(course.to_dict())


# DELETE - Remover curso
@courses_bp.route('/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """
    Remove um curso e todas suas lições
    ---
    tags:
      - Cursos
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Curso removido com sucesso
      404:
        description: Curso não encontrado
    """
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Curso não encontrado"}), 404

    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": f"Curso {course_id} removido com sucesso"}), 200


# GET - Listar aulas de um curso
@courses_bp.route('/<int:course_id>/aulas', methods=['GET'])
def get_lessons_by_course(course_id):
    """
    Lista aulas de um curso específico
    ---
    tags:
      - Cursos
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Lista de aulas do curso
      404:
        description: Curso não encontrado
    """
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Curso não encontrado"}), 404

    lessons = Lesson.query.filter_by(course_id=course_id).order_by(Lesson.order).all()
    return jsonify([l.to_dict() for l in lessons])