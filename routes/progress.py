from flask import Blueprint, jsonify, request
from database import db
from models import Question, QuestionAttempt, LessonProgress, User, Lesson

progress_bp = Blueprint('progress', __name__)


# GET - Listar todo progresso
@progress_bp.route('/', methods=['GET'])
def get_all_progress():
    """
    Lista todo o progresso dos usuários
    ---
    tags:
      - Progresso
    responses:
      200:
        description: Lista de progresso
    """
    progresses = LessonProgress.query.all()
    return jsonify([p.to_dict() for p in progresses])


# GET - Histórico do usuário
@progress_bp.route('/historico/<int:user_id>', methods=['GET'])
def get_history(user_id):
    """
    Retorna o histórico completo do aluno
    ---
    tags:
      - Progresso
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Histórico do aluno
      404:
        description: Usuário não encontrado
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    completed = LessonProgress.query.filter_by(
        user_id=user_id, is_completed=True
    ).all()

    recent = QuestionAttempt.query.filter_by(
        user_id=user_id
    ).order_by(QuestionAttempt.timestamp.desc()).limit(10).all()

    return jsonify({
        "user_id": user_id,
        "username": user.username,
        "completed_lessons": [p.to_dict() for p in completed],
        "recent_attempts": [a.to_dict() for a in recent],
        "total_score": len(completed)
    })


# POST - Submeter resposta
@progress_bp.route('/', methods=['POST'])
def submit_answer():
    """
    Submete uma resposta e registra a tentativa no banco
    ---
    tags:
      - Progresso
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: integer
            question_id:
              type: integer
            selected_option:
              type: integer
    responses:
      200:
        description: Resultado da submissão
      400:
        description: Dados inválidos
      404:
        description: Pergunta ou usuário não encontrado
    """
    data = request.json
    if not data:
        return jsonify({"error": "Dados não fornecidos"}), 400

    user_id = data.get('user_id')
    question_id = data.get('question_id')
    selected_option = data.get('selected_option')

    if not user_id or not question_id or selected_option is None:
        return jsonify({"error": "user_id, question_id e selected_option são obrigatórios"}), 400

    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Pergunta não encontrada"}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    is_correct = (selected_option == question.correct_answer)

    attempt = QuestionAttempt(
        user_id=user_id,
        question_id=question_id,
        selected_option=selected_option,
        is_correct=is_correct,
    )
    db.session.add(attempt)
    db.session.commit()

    # Verifica se a lição foi concluída
    lesson_id = question.lesson_id
    lesson_questions = Question.query.filter_by(lesson_id=lesson_id).all()

    all_correct = True
    for q in lesson_questions:
        has_correct = QuestionAttempt.query.filter_by(
            user_id=user_id,
            question_id=q.id,
            is_correct=True,
        ).first() is not None
        if not has_correct:
            all_correct = False
            break

    if all_correct:
        progress = LessonProgress.query.filter_by(
            user_id=user_id, lesson_id=lesson_id
        ).first()
        if not progress:
            progress = LessonProgress(
                user_id=user_id,
                lesson_id=lesson_id,
                is_completed=True,
                completed_at=db.func.now(),
            )
            db.session.add(progress)
        elif not progress.is_completed:
            progress.is_completed = True
            progress.completed_at = db.func.now()
        db.session.commit()

    return jsonify({
        "is_correct": is_correct,
        "correct_answer": question.correct_answer,
        "message": "Resposta correta!" if is_correct else "Tente novamente."
    })


# PUT - Atualizar progresso da lição
@progress_bp.route('/<int:user_id>/aula/<int:lesson_id>', methods=['PUT'])
def update_lesson_progress(user_id, lesson_id):
    """
    Atualiza manualmente o progresso de uma lição
    ---
    tags:
      - Progresso
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
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
            is_completed:
              type: boolean
    responses:
      200:
        description: Progresso atualizado
      404:
        description: Usuário ou lição não encontrados
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({"error": "Lição não encontrada"}), 404

    data = request.json
    is_completed = data.get('is_completed', False)

    progress = LessonProgress.query.filter_by(
        user_id=user_id, lesson_id=lesson_id
    ).first()

    if not progress:
        progress = LessonProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            is_completed=is_completed,
            completed_at=db.func.now() if is_completed else None,
        )
        db.session.add(progress)
    else:
        progress.is_completed = is_completed
        progress.completed_at = db.func.now() if is_completed else None

    db.session.commit()
    return jsonify(progress.to_dict())


# DELETE - Resetar progresso do usuário
@progress_bp.route('/<int:user_id>', methods=['DELETE'])
def reset_user_progress(user_id):
    """
    Reseta todo o progresso de um usuário
    ---
    tags:
      - Progresso
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Progresso resetado com sucesso
      404:
        description: Usuário não encontrado
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    QuestionAttempt.query.filter_by(user_id=user_id).delete()
    LessonProgress.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return jsonify({"message": f"Progresso do usuário {user_id} resetado com sucesso"}), 200