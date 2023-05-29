from flask import Blueprint,render_template,request
from apps01.users.models import User
from apps01.goods.models import *

goods_bp = Blueprint("goods",__name__)


#用戶找商品（ＸＸＸ用戶買了哪些傷品）
@goods_bp.route("/findgoods")
def find_goods():
    pass

#根據商品找用戶（ＸＸＸ商品哪些人買了）
@goods_bp.route("/finduser")
def find_user():
    pass

#用戶買商品
@goods_bp.route("/show")
def show():
    users = User.query.filter(User.isdelete==False).all()
    good_list =Good.query.all()
    return render_template("goods/show.html",users=users,good_list=good_list)

@goods_bp.route("/buy")
def buy():
    uid = request.args.get("uid")
    gid = request.args.get("gid")
    ug = User_goods()
    ug.user_id = uid
    ug.goods_id = gid
    db.session.add(ug)
    db.session.commit()
    return "購買成功"