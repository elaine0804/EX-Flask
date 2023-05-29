import os

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session,g
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from apps01.users.models import User
from apps01.users.sendemail import sendmail
from apps01.settings import Config
from exts import db
import random


user_bp1 = Blueprint("user", __name__, url_prefix="/user")

required_login_list = ["/user/center","/user/change"]

#@user_bp1.before_app_first_request
#@user_bp1.after_app_request
#@user_bp1.teardown_app_request

#權限
@user_bp1.before_app_request
def before_request1():
    print("before_app_request1",request.path)
    if request.path in required_login_list:
        id = session.get("uid")
        if not id:
            return render_template("user01/login.html")
        else:
            user = User.query.get(id)
            #g對象,本次請求的對象
            g.user = user

#首頁
@user_bp1.route("/")
def index():
    #1.cookie獲取方式
    #uid = request.cookies.get("uid", None)
    #2.session的獲取,session底層默認獲取
    uid = session.get("uid",None)
    if uid:
        user = User.query.get(uid)
        return render_template("user01/index.html",user=user)
    else:
        return render_template("user01/index.html")

#用戶註冊
@user_bp1.route("/register", methods=["GET","POST"])
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
    return render_template("user01/register.html")

#手機號碼驗證
@user_bp1.route("/checkphone", methods=["GET","POST"])
def check_phone():
    phone = request.args.get("phone")
    user = User.query.filter(User.phone == phone).all()
    #code: 400 不能用 200 可以用
    if len(user)>0:
        return jsonify(code=400, msg="此號碼已被註冊")
    else:
        return jsonify(code=200, msg="此號碼可用")

#信箱驗證
@user_bp1.route("/checkemail", methods=["GET","POST"])
def check_email():
    email = request.args.get("email")
    user = User.query.filter(User.email == email).all()
    if len(user)>0:
        return jsonify(code=400, msg="此信箱已被註冊")
    else:
        return jsonify(code=200, msg="此信箱可用")

#用戶登入
@user_bp1.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        f = request.args.get("f")
        if f == "1":
            username =request.form.get("username")
            password =request.form.get("password")
            users = User.query.filter(User.username == username).all()
            for user in users:
                #如果flag=True表示匹配，否則密碼不匹配
                flag = check_password_hash(user.password,password)
                if flag: #帳號密碼
                    #1.cookie實現機制
                    #response = redirect(url_for("user.index"))
                    #response.set_cookie("uid", str(user.id), max_age=1800)
                    #return response
                    #2.session機制,session當成字典用
                    session["uid"] =user.id
                    return redirect(url_for("user.index"))
                else:
                    return render_template("user01/login.html", msg="用戶名或密碼有誤")
        elif f == "2": #信箱驗證碼
            print("----->2222")
            email =request.form.get("email")
            code = request.form.get("code")
            #先驗證驗證碼
            vailid_code = session.get(email)
            print("vailid_code:"+str(vailid_code))
            if code == vailid_code:
                #查詢數據庫
                user = User.query.filter(User.email == email).first()
                print(user)
                if user:
                    #登入成功
                    session["uid"] = user.id
                    return render_template("user.index")
                else:
                    return render_template("user/login.html",msg = "此信箱未註冊")
            else:
                return render_template("user/login.html",msg = "驗證碼有誤！")

    return render_template("user01/login.html")

#發送信箱驗證
@user_bp1.route("/sendMsg")
def send_message():
    email = request.args.get("email")
    #驗證email是否註冊,去數據庫查詢
    check_email = User.query.filter(User.email).all()
    pwd = random.randrange(00000,99999)
    if check_email == True:
        sendmail(check_email,pwd)
        return ("信箱驗證發送成功")
    else:
        return ("信箱驗證失敗")

#用戶登出
@user_bp1.route("/logout")
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
@user_bp1.route("/center")
def user_center():
    id = session.get("uid")
    user = User.query.get(id)
    return render_template("user01/center.html",user=g.user)

#可支持上傳的圖片檔案
ALLOWED_EXTENSIONS = ["jpg","png","gif","bmp"]

@user_bp1.route("/change", methods=["GET","POST"])
def user_change():
    if request.post == "POST":
        username = request.form.get("username")
        phone = request.form.get("phone")
        email = request.form.get("email")
        #只要有文件、圖片,獲取方式必須使用request.files.get(name)
        icon = request.files.get("icon")
        #print(icon) #FileStorage
        #屬性： filename 用戶獲取文件的名字
        #方法：save(保存路徑)
        icon_name = icon.filename #3312.jpg
        suffix = icon_name.split("."[-1])
        if suffix in ALLOWED_EXTENSIONS:
            icon_name = secure_filename(icon_name)
            file_path = os.path.join(Config.UPLOAD_ICON_DIR,icon_name)
            icon.save(file_path)
            #保存成功
            user = g.user
            user.username = username
            user.phone = check_phone
            user.email = email
            path = "upload/icon/"
            user.icon = os.path.join(path,icon_name)
            db.session.commit()
            return redirect(url_for("user.user_center"))
        else:
            return render_template("user01/center.html", user=g.user,msg="可支持上傳的圖片檔案:jpg,png,gif,bmp")
        #查詢手機號碼
        #phone_ = User.query.filter(and_(g.user.phone == phone, g.user.id != User.id))
        users = User.query.all()
        for user in users:
            if user.phone == phone:
                return render_template("user01/center.html", user=g.user,msg="此手機號碼已被註冊")
    return render_template("user01/center.html",user=g.user)