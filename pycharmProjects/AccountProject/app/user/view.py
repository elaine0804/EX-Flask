from flask import Blueprint, render_template, request, url_for, jsonify, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from app.user.model import User
from exts import db

user_bp = Blueprint("user", __name__, url_prefix="/user")

required_login_list = ["/user/center"]

#權限
@user_bp.before_app_request
def before_request1():
    print("before_app_request1",request.path)
    if request.path in required_login_list:
        id = session.get("uid")
        if not id:
            return render_template("user/login.html")
        else:
            user = User.query.get(id)
            #g對象,本次請求的對象
            g.user = user

#首頁
@user_bp.route("/")
def index():
    # 1.cookie獲取方式
    # uid = request.cookies.get("uid", None)
    # 2.session的獲取,session底層默認獲取
    uid = session.get("uid", None)
    if uid:
        user = User.query.get(uid)
        return render_template("user/index.html",user=user)
    else:
        return render_template("user/index.html")


#用戶註冊
@user_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        # 獲取post提交的數據
        username = request.form.get("username")
        password = request.form.get("password")
        repassword = request.form.get("repassword")
        phone = request.form.get("phone")
        email = request.form.get("email")
        if password == repassword:
            # 註冊用戶
            user = User()
            user.username = username
            #使用自帶的函數實現加密：generate_password_hash
            user.password = generate_password_hash(password)
            user.phone = phone
            user.email = email
            # 添加並提交
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.index"))
    return render_template("user/register.html")

#手機號碼驗證
@user_bp.route("/checkphone", methods=["GET","POST"])
def check_phone():
    phone = request.args.get("phone")
    user = User.query.filter(User.phone == phone).all()
    #code: 400 不能用 200 可以用
    if len(user)>0:
        return jsonify(code=400, msg="此號碼已被註冊")
    else:
        return jsonify(code=200, msg="號碼可用")

#信箱驗證
@user_bp.route("/checkemail", methods=["GET","POST"])
def check_email():
    email = request.args.get("email")
    user = User.query.filter(User.email == email).all()
    if len(user) > 0:
        return jsonify(code=400, msg="此信箱已被註冊")
    else:
        return jsonify(code=200, msg="信箱可用")

#用戶登入
@user_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username =request.form.get("username")
        password =request.form.get("password")
        users = User.query.filter(User.username == username).all()
        for user in users:
            #如果flag=True表示匹配，否則密碼不匹配
            flag = check_password_hash(user.password, password)
            if flag: #帳號密碼
                #1.cookie實現機制
                #response = redirect(url_for("user.index"))
                #response.set_cookie("uid", str(user.id), max_age=1800)
                #return response
                #2.session機制,session當成字典用
                session["uid"] = user.id
                return redirect(url_for("user.index"))
            else:
                return render_template("user/login.html", msg="用戶名或密碼有誤")
    return render_template("user/login.html")

#用戶登出
@user_bp.route("/logout")
def logout():
    #1.cookie的方式:
    #response = redirect(url_for("user.index"))
    #通過response對象的delete_cookie(key),key就是要刪除的cookie的key
    #response.delete_cookie("uid")
    #return response
    #2.session的方式
    #del session["uid"] #空間還留存
    session.clear()
    return redirect(url_for("user.index"))

#用戶中心
@user_bp.route("/center")
def user_center():
    return render_template("user/center.html",user=g.user)
