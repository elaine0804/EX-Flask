from datetime import datetime
from exts import db

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    bdatetime = db.Column(db.DateTime, default=datetime.now)
    accountname = db.Column(db.String(15),nullable = False)
    password = db.Column(db.String(64),nullable = False)
    phone = db.Column(db.String(10),unique = True,nullable = False)
    email = db.Column(db.String(60))
    icon = db.Column(db.String(100))
    isdelete = db.Column(db.Boolean,default = False) #邏輯刪除

    #增加一個字段
    articles = db.relationship("Article",backref="user")

    def __str__(self):
        return self.username
    