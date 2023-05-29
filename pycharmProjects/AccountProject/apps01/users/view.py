import hashlib
from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy import or_
from exts import db
from apps01.users.models import User

user_bp = Blueprint("user",__name__)

@user_bp.route("/register",methods = ["GET","POST"])
def register():
    if request.method == "POST":
        #獲取post提交的數據
        username =request.form.get("username")
        password =request.form.get("password")
        repassword =request.form.get("repassword")
        phone =request.form.get("phone")
        email = request.form.get("email")
        if password == repassword:
            #註冊用戶
            user = User()
            user.username = username
            user.password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            user.phone = phone
            user.email = email
            #添加並提交
            db.session.add(user)
            db.session.commit()
            return redirect("/")
    return render_template("user01/register.html")

@user_bp.route("/")
def user_center():
    #查詢數據庫中的數據
    users = User.query.filter(User.isdelete == False).all() #select * from user;
    return render_template("user01/center.html",users=users)

@user_bp.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username =request.form.get("username")
        password =request.form.get("password")
        #關鍵 select * from user where username ="XXX"
        new_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        #查詢
        user_list = User.query.filter_by(username=username)
        for u in user_list:
            if u.password == new_password:
                return "用戶登錄成功"
            else:
                return render_template("user01/login.html",msg="用戶或密碼有誤！")
    return render_template("user01/login.html")
#搜尋
@user_bp.route("/search")
def search():
    keyword = request.args.get("search")
    #查詢
    user_list = User.query.filter(User.isdelete == False).filter(or_(User.username.contains(keyword),User.phone.contains(keyword)))
    return render_template("user01/center.html",users = user_list)
 
#用戶刪除
#邏輯刪除
@user_bp.route("/delete")
def delete():
    #獲取用戶id
    id = request.args.get("id") #主鍵
    #獲取該id的用戶
    user = User.query.get(id)
    #邏輯刪除
    user.isdelete = True
    #提交
    db.session.commit()
    return redirect(url_for('user.user_center'))

#物理刪除
@user_bp.route("/tdelete")
def tdelete():
    #獲取用戶id
    id = request.args.get("id") #主鍵
    #獲取該id的用戶
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user.user_center'))

@user_bp.route("/update",methods=["GET","POST"])
def update():
    if request.method == "POST":
        username = request.form.get("username")
        phone = request.form.get("phone")
        id = request.form.get("id")
        #找用戶
        user = User.query.get(id)
        #改用戶信息
        user.username = username
        user.phone = phone
        #提交
        db.session.commit()
        return redirect(url_for('user.user_center'))
    else:
        id = request.args.get("id")
        user = User.query.get(id)
        return render_template("user01/update.html",user = user)

@user_bp.route("/select")
def user_select():
    user = User.query.get(3) #根據主鍵查詢用戶
    user01 = User.query.filter(User.username == "q").all() #user01[1:5]列表可切片
    user_list = User.query.filter(User.username.startswith("q")).all()
    return render_template("user01/select.html",user=user,user01=user01,user_list=user_list)