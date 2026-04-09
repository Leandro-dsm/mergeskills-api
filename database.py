from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Configura e inicia o SQLAlchemy com Flask app"""
    import os

    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError("DATABASE_URL não configurada!")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    # Cria as tabelas se não existirem
    with app.app_context():
        db.create_all()