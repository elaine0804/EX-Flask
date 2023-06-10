from exts import db, bootstrap
from flask import Flask
from app.user.view import user_bp
#from app.bookkeeping.view import article_bp1
from settings import DevelopmentConfig

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(DevelopmentConfig)
    #初始化db
    db.init_app(app=app)
    #初始化bootstrap
    bootstrap.init_app(app=app)
    app.register_blueprint(user_bp)
    #app.register_blueprint(article_bp)
    return app