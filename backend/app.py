from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from extensions import db, migrate, bcrypt, jwt 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Import models after db.init_app
    from models import user, personal_details

    # Import blueprints after db is initialized
    from routes.user_routes import user_bp
    from routes.personal_details_routes import personal_bp

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(personal_bp, url_prefix='/api/personal')

    @app.route('/')
    def index():
        return {"message": "Flask API running!"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5005)
