from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health Check Endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: API is running
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
            message:
              type: string
              example: MergeSkills API is running
    """
    return jsonify({
        "status": "ok",
        "message": "MergeSkills API is running"
    })