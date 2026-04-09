from flask import Blueprint, jsonify, request
from database import db
from models import Question, QuestionAttempt

questions_bp = Blueprint('questions', __name__)


# GET - Listar todas as perguntas
@questions_bp.route('/', methods=['GET'])
def get_all_questions():
    """
    Lista todas as perguntas
    ---
    tags:
      - Perguntas
    responses:
      200:
        description: Lista de todas as perguntas
    """
    questions = Question.query.all()
    return jsonify([q.to_dict() for q in questions])


# GET - Buscar pergunta por ID
@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_question_details(question_id):
    """
    Obtém detalhes de uma pergunta
    ---
    tags:
      - Perguntas
    parameters:
      - name: question_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Detalhes da pergunta
      404:
        description: Pergunta não encontrada
    """
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Pergunta não encontrada"}), 404
    return jsonify(question.to_dict())


# POST - Criar nova pergunta
@questions_bp.route('/', methods=['POST'])
def create_question():
    """
    Cria uma nova pergunta
    ---
    tags:
      - Perguntas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            lesson_id:
              type: integer
            question:
              type: string
            code:
              type: string
            options:
              type: array
            correct_answer:
              type: integer
            order:
              type: integer
    responses:
      201:
        description: Pergunta criada com sucesso
      400:
        description: Dados inválidos
    """
    data = request.json
    if not data or 'lesson_id' not in data or 'question' not in data:
        return jsonify({"error": "lesson_id e question são obrigatórios"}), 400

    question = Question(
        lesson_id=data['lesson_id'],
        question=data['question'],
        code=data.get('code'),
        options=data.get('options', []),
        correct_answer=data.get('correct_answer', 0),
        order=data.get('order', 0)
    )
    db.session.add(question)
    db.session.commit()
    return jsonify(question.to_dict()), 201


# PUT - Atualizar pergunta
@questions_bp.route('/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    """
    Atualiza uma pergunta existente
    ---
    tags:
      - Perguntas
    parameters:
      - name: question_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            question:
              type: string
            code:
              type: string
            options:
              type: array
            correct_answer:
              type: integer
            order:
              type: integer
    responses:
      200:
        description: Pergunta atualizada
      404:
        description: Pergunta não encontrada
    """
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Pergunta não encontrada"}), 404

    data = request.json
    if 'question' in data:
        question.question = data['question']
    if 'code' in data:
        question.code = data['code']
    if 'options' in data:
        question.options = data['options']
    if 'correct_answer' in data:
        question.correct_answer = data['correct_answer']
    if 'order' in data:
        question.order = data['order']

    db.session.commit()
    return jsonify(question.to_dict())


# DELETE - Remover pergunta
@questions_bp.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """
    Remove uma pergunta
    ---
    tags:
      - Perguntas
    parameters:
      - name: question_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Pergunta removida com sucesso
      404:
        description: Pergunta não encontrada
    """
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Pergunta não encontrada"}), 404

    # Remove também as tentativas associadas
    QuestionAttempt.query.filter_by(question_id=question_id).delete()
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": f"Pergunta {question_id} removida com sucesso"}), 200