from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps01.users.models import User
from apps01.article.models import Article
from apps01.goods.models import *
from apps01 import create_app
from exts import db

app = create_app()
manager = Manager(app=app)
migrate = Migrate(app=app,db=db)
manager.add_command("db",MigrateCommand)

@manager.command
def init():
    print("初始化")
    
if __name__ == "__main__" :
    manager.run()


