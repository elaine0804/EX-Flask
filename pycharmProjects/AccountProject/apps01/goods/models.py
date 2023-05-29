from exts import db

class Good(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    gname = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float,nullable=False)

    def __str__(self):
        return self.gname

#關係表： user和goods之間的關係
class User_goods(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    goods_id = db.Column(db.Integer,db.ForeignKey("good.id"))
    number = db.Column(db.Integer, default=1)