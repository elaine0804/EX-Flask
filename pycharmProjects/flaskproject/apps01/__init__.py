from exts import db
from flask import Flask
from apps01.users.view import user_bp
from apps01.article.view import article_bp
from apps01.goods.view import goods_bp
from apps01.settings import DevelopmentConfig

def create_app():
    app = Flask(__name__,template_folder = "../templates",static_folder = "../static")
    app.config.from_object(DevelopmentConfig)
    #初始化db
    db.init_app(app=app)
    app.register_blueprint(user_bp)
    app.register_blueprint(article_bp)
    app.register_blueprint(goods_bp)
    return app